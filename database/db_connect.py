import os

from peewee import PostgresqlDatabase

connection = PostgresqlDatabase(
    os.getenv('DB_NAME'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    autoconnect=False
)
