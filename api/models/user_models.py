from tortoise.models import Model
from tortoise.fields import IntField, CharField

class User(Model):
    id = IntField(pk=True)
    username = CharField(max_length=50, unique=True, null=False)
    password = CharField(max_length=128, null=False)
    
    class PydanticMeta:
        exclude = ["password"]
