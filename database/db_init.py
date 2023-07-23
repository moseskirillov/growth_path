from database.db_connect import connection
from entities.completed_meeting_model import CompletedMeeting
from entities.completed_step_model import CompletedStep
from entities.meeting_date import MeetingDate
from entities.meeting_model import Meeting
from entities.registration_model import Registration
from entities.step_model import Step
from entities.user_model import User


def database_init():
    tables = [User, Step, Meeting, MeetingDate, Registration, CompletedMeeting, CompletedStep]
    with connection:
        for table in tables:
            table.create_table(safe=True)
