from peewee import Model, PrimaryKeyField, ForeignKeyField, DateField

from database.db_connect import connection
from entities.step_model import Step
from entities.user_model import User


class CompletedStep(Model):
    id = PrimaryKeyField(null=False)
    user = ForeignKeyField(User, backref='user_id', null=False)
    step = ForeignKeyField(Step, backref='step_id', null=False)
    date_of_completion = DateField(null=False)

    class Meta:
        db_table = 'completed_steps'
        database = connection
        schema = 'growth_path_bot'
