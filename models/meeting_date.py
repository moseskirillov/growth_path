from peewee import Model, PrimaryKeyField, DateTimeField, ForeignKeyField

from database.db_connect import connection
from models.meeting_model import Meeting


class MeetingDate(Model):
    id = PrimaryKeyField(null=False)
    date = DateTimeField(null=False)
    meeting = ForeignKeyField(Meeting, backref='meeting_id', null=False)

    class Meta:
        db_table = 'meetings_dates'
        database = connection
        schema = 'growth'
