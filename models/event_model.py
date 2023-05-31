from peewee import Model, PrimaryKeyField, CharField, ForeignKeyField, IntegerField, DateField

from database.db_connect import connection
from models.step_model import Step


class Event(Model):
    id = PrimaryKeyField(null=False)
    title = CharField(max_length=255, null=False)
    order = IntegerField(null=False)
    date = DateField(null=False)
    step = ForeignKeyField(Step, backref='step_id')

    class Meta:
        db_table = 'events'
        database = connection
