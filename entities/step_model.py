from peewee import Model, PrimaryKeyField, CharField

from database.db_connect import connection


class Step(Model):
    id = PrimaryKeyField(null=False)
    title = CharField(max_length=255, null=False)

    class Meta:
        db_table = 'steps'
        database = connection
        schema = 'growth'
