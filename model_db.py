from peewee import *

db = SqliteDatabase('telegram.db')


class BaseModel(Model):
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = db
        order_by = 'id'


class Person(BaseModel):
    time_of_creation = DateTimeField()
    telegram_id = IntegerField()
    discord_id = IntegerField(null=True)
    nick = CharField(null=True)
    garik_relationship = BooleanField(null=True)

    class Meta:
        db_table = 'people'


class Ban(BaseModel):
    time_of_creation = DateTimeField()
    nick = CharField()
    description = CharField()
    is_paid = BooleanField()

    class Meta:
        db_table = 'bans'


class Payment(BaseModel):
    time_of_creation = DateTimeField()
    amount = DecimalField()
    description = CharField()
    is_completed = BooleanField()

    class Meta:
        db_table = 'payments'
        