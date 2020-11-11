from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.BigIntField(pk=True)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=100)

    def __str__(self):
        return self.email

    def dict(self):
        return {
            'id': self.id,
            'email': self.email
        }
