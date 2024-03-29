import logging
from datetime import datetime, date

from peewee import JOIN
from telegram.ext import ContextTypes

from database.db_connect import connection
from entities.completed_meeting_model import CompletedMeeting
from entities.completed_step_model import CompletedStep
from entities.meeting_date import MeetingDate
from entities.meeting_model import Meeting
from entities.registration_model import Registration
from entities.step_model import Step
from entities.user_model import User
from models.meeting_request import MeetingRequest


def get_or_create_user(telegram_id, first_name, last_name, telegram_login):
    with connection.atomic():
        user, created = User.get_or_create(
            telegram_id=telegram_id,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'telegram_login': telegram_login
            }
        )
        if created:
            logging.info(f'Создан новый пользователь: {first_name} {last_name}')
        else:
            user.last_login_date = datetime.now()
            user.save()
            logging.info(f'Вошел пользователь: {first_name} {last_name}')
        return user


def get_next_meeting(user_id, context: ContextTypes.DEFAULT_TYPE):
    with connection.atomic():
        next_step = (
            Step
            .select(Step.id)
            .join(CompletedStep, JOIN.LEFT_OUTER, on=(
                    (Step.id == CompletedStep.step_id) &
                    (CompletedStep.user_id == user_id)
            ))
            .where(CompletedStep.id.is_null(False))
            .order_by(Step.id.desc())
            .first()
        )

        next_step_id = next_step.id + 1 if next_step else 1

        next_meeting = (
            Meeting
            .select(Meeting, MeetingDate)
            .join(MeetingDate)
            .join(CompletedMeeting, JOIN.LEFT_OUTER, on=(
                    (Meeting.id == CompletedMeeting.meeting_id) &
                    (CompletedMeeting.user_id == user_id)
            ))
            .join(Step, on=(Meeting.step_id == Step.id))
            .join(CompletedStep, JOIN.LEFT_OUTER, on=(
                    (Step.id == CompletedStep.step_id) &
                    (CompletedStep.user_id == user_id)
            ))
            .where(
                CompletedMeeting.id.is_null(True),
                MeetingDate.date >= datetime.now(),
                CompletedStep.id.is_null(True),
                Step.id == next_step_id
            )
            .order_by(MeetingDate.date)
            .first()
        )

        response_message = None

        if next_meeting:
            formatted_date = next_meeting.meetingdate.date.strftime('%d.%m.%Y %H:%M')
            response_message = f'<b>Ближайшая встреча</b>: {next_meeting.title}\n' \
                               f'<b>Дата проведения</b>: {formatted_date}'
            context.user_data['next_meeting_id'] = next_meeting.meetingdate.id
            context.user_data['next_meeting_number'] = next_meeting.meetingdate.meeting.order
            context.user_data['next_meeting_title'] = next_meeting.title
            context.user_data['next_meeting_date'] = next_meeting.meetingdate.date.strftime('%d.%m.%Y')
            context.user_data['next_meeting_step'] = next_meeting.step.id

        return response_message


def register_to_meeting(user_id, meeting_id):
    with connection.atomic():
        register, created = Registration.get_or_create(
            date=datetime.today(),
            user=user_id,
            meeting_date=meeting_id
        )
        return register, created


def mark_a_visitor(registration_id):
    with connection.atomic():
        logging.info('Получаю данные о регистрации')
        registration = (Registration
                        .select()
                        .where(Registration.id == registration_id)
                        .prefetch(User, MeetingDate, Meeting))
        if len(registration) > 0:
            for register in registration:
                logging.info('Получил данные о регистрации')
                logging.info('Создаю запись о посещенной встрече')
                _, created = CompletedMeeting.get_or_create(
                    user=register.user_id,
                    meeting=register.meeting_date.meeting_id,
                    date_of_completion=datetime.now()
                )
                logging.info('Создал запись о посещенной встрече')
                if created:
                    completed_meetings = (
                        CompletedMeeting
                        .select()
                        .join(Registration, on=(CompletedMeeting.user == Registration.user))
                        .join(MeetingDate, on=(Registration.meeting_date == MeetingDate.id))
                        .join(Meeting, on=(MeetingDate.meeting == Meeting.id))
                        .where(CompletedMeeting.user == register.user_id,
                               Meeting.step == register.meeting_date.meeting.step)
                        .distinct()
                        .count()
                    )
                    if completed_meetings == 4:
                        CompletedStep.get_or_create(
                            user=register.user,
                            step=register.meeting_date.meeting.step,
                            date_of_completion=date.today()
                        )
                    request = MeetingRequest(
                        date=register.meeting_date.date.strftime('%d.%m.%Y'),
                        step_number=register.meeting_date.meeting.step.id,
                        meeting_number=register.meeting_date.meeting.order,
                        meeting_title=register.meeting_date.meeting.title,
                        first_name=register.user.first_name,
                        last_name=register.user.last_name if register.user.last_name else '',
                        telegram_login=register.user.telegram_login
                    )
                    return request, f'{register.user.first_name} {register.user.last_name} ' \
                                    f'успешно отмечен на встрече\n"{register.meeting_date.meeting.title}"'
                else:
                    return None, 'Посетитель уже прошел эту встречу'
        else:
            return None, 'Такая встреча не найдена'


def find_user_by_id(user_id):
    with connection.atomic():
        return User.get(id=user_id)


def cancel_registration(user_id):
    with connection:
        result = (Registration
                  .delete()
                  .where(Registration.user == user_id)
                  .execute())
        if result > 0:
            return 'Регистрация отменена'
        else:
            return 'Сейчас вы не зарегистрированы ни на одну из встреч'


def check_registration(user_id):
    with connection.atomic():
        registration = Registration.get_or_none(user=user_id)
        if registration is not None:
            meeting_date = registration.meeting_date
            title = meeting_date.meeting.title
            event_date = meeting_date.date
            formatted_date = event_date.strftime('%d.%m.%Y %H:%M')
            return f'Вы зарегистрированы на встречу:\n{title}\nДата проведения: {formatted_date}'
        else:
            return None


def get_completed_first_step(user_id):
    """
    На данный момент не используется, позже можно будет
    проверять, прошел ли юзер первый шаг
    :param user_id: id пользователя
    :return: пройденный шаг из таблицы шагов
    """
    with connection.atomic():
        return CompletedStep.get_or_none(user=user_id)


def get_current_registration(user_id):
    with connection.atomic():
        return Registration.get_or_none(user=user_id)


def delete_registration(registration_id):
    with connection:
        result = (Registration
                  .delete()
                  .where(Registration.id == registration_id)
                  .execute())
        if result > 0:
            logging.info('Регистрация удалена')
