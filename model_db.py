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


class FSMForm(BaseModel):
    time_of_creation = DateTimeField()
    nick = CharField(null=True)
    telegram_id = IntegerField()

    about_player = CharField(null=True)
    is_about_player_text = BooleanField(null=True)

    what_to_do = CharField(null=True)
    is_what_to_do_text = BooleanField(null=True)

    game_experience = CharField(null=True)
    is_game_experience_text = BooleanField(null=True)

    garik_relationship = CharField(null=True)
    is_filled = BooleanField()
    verdict = BooleanField(null=True)

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


'''
class FormTransaction(BaseModel):
    time_of_creation = DateTimeField()
    telegram_id = IntegerField()
    form_item = CharField()
    current_state = CharField()

    class Meta:
        db_table = 'form_transactions'
'''


# db.create_tables([FSMForm, Ban, Payment])
