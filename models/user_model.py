from datetime import datetime

from peewee import Model, PrimaryKeyField, CharField, DateTimeField

from database.db_connect import connection


class User(Model):
    id = PrimaryKeyField(null=False)
    creation_date = DateTimeField(default=datetime.now())
    first_name = CharField(max_length=255, null=True)
    last_name = CharField(max_length=255, null=True)
    phone_number = CharField(max_length=255, null=True)
    telegram_login = CharField(max_length=255, null=True)
    telegram_id = CharField(max_length=255, null=True)

    class Meta:
        db_table = 'users'
        database = connection
