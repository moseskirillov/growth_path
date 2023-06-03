from database.db_connect import connection
from models.completed_meeting_model import CompletedMeeting
from models.completed_step_model import CompletedStep
from models.meeting_date import MeetingDate
from models.meeting_model import Meeting
from models.registration_model import Registration
from models.step_model import Step
from models.user_model import User


def database_init():
    tables = [User, Step, Meeting, MeetingDate, Registration, CompletedMeeting, CompletedStep]
    with connection:
        for table in tables:
            table.create_table(safe=True)
