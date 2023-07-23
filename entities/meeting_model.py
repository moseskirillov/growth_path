from peewee import Model, PrimaryKeyField, CharField, ForeignKeyField, IntegerField

from database.db_connect import connection
from entities.step_model import Step


class Meeting(Model):
    id = PrimaryKeyField(null=False)
    title = CharField(max_length=255, null=False)
    order = IntegerField(null=False)
    step = ForeignKeyField(Step, backref='step_id', null=False)

    class Meta:
        db_table = 'meetings'
        database = connection
        schema = 'growth'
