from database.db_connect import connection
from models.event_model import Event
from models.step_model import Step
from models.user_model import User


def database_init():
    tables = [User, Step, Event]
    with connection:
        for table in tables:
            table.create_table(safe=True)
