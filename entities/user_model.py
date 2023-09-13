from datetime import datetime

from peewee import Model, PrimaryKeyField, CharField, DateTimeField, BooleanField

from database.db_connect import connection


class User(Model):
    id = PrimaryKeyField(null=False)
    first_name = CharField(max_length=255, null=True)
    last_name = CharField(max_length=255, null=True)
    phone_number = CharField(max_length=255, null=True)
    telegram_login = CharField(max_length=255, null=True)
    telegram_id = CharField(max_length=255, null=False)
    date_of_creation = DateTimeField(default=datetime.now())
    last_login_date = DateTimeField(default=datetime.now())
    is_admin = BooleanField(default=False)

    class Meta:
        db_table = 'users'
        database = connection
        schema = 'growth_path_bot'
