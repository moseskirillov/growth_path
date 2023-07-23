from peewee import Model, PrimaryKeyField, DateField, ForeignKeyField

from database.db_connect import connection
from entities.meeting_date import MeetingDate
from entities.user_model import User


class Registration(Model):
    id = PrimaryKeyField(null=False)
    date = DateField(null=False)
    user = ForeignKeyField(User, backref='user_id', null=False)
    meeting_date = ForeignKeyField(MeetingDate, backref='meeting_date', null=False)

    class Meta:
        db_table = 'registration'
        database = connection
        schema = 'growth'
