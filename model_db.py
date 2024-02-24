from peewee import SqliteDatabase
from peewee import Model

from peewee import PrimaryKeyField
from peewee import DateTimeField
from peewee import IntegerField
from peewee import CharField
from peewee import BooleanField
from peewee import DecimalField


db = SqliteDatabase('telegram.db')


class BaseModel(Model):
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = db
        order_by = 'id'


class FormTransaction(BaseModel):
    time_of_creation = DateTimeField()
    telegram_id = IntegerField()
    form_item = CharField()
    current_state = CharField()

    class Meta:
        db_table = 'form_transactions'


class FSMForm(BaseModel):
    telegram_id = IntegerField()
    nick = CharField(null=True)
    time_of_creation = DateTimeField()
    about_player = CharField()
    what_to_do = CharField()
    game_experience = CharField()
    garik_relationship = CharField(null=True)
    is_filled = BooleanField()

    class Meta:
        db_table = 'forms'


class Ban(BaseModel):
    time_of_creation = DateTimeField()
    payment_id = IntegerField()
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
