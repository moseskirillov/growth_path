from peewee import Model, PrimaryKeyField, ForeignKeyField, DateField

from database.db_connect import connection
from entities.meeting_model import Meeting
from entities.user_model import User


class CompletedMeeting(Model):
    id = PrimaryKeyField(null=False)
    user = ForeignKeyField(User, backref='user_id', null=False)
    meeting = ForeignKeyField(Meeting, backref='meeting_id', null=False)
    date_of_completion = DateField(null=False)

    class Meta:
        db_table = 'completed_meetings'
        database = connection
        schema = 'growth_path_bot'
