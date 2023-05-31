from peewee import PostgresqlDatabase

connection = PostgresqlDatabase(
    'growth_path',
    host='localhost',
    port=5432,
    user='postgres',
    password='password',
    autoconnect=False
)
