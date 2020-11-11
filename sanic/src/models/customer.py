from tortoise import fields
from tortoise.models import Model


class Customer(Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=255)

    def __str__(self):
        return self.name

    def dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
