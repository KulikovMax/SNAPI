from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from models import User


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ('id', 'is_admin', 'last_request', 'last_login')
        load_instance = True
        load_only = ('password',)

    email = fields.Email(required=True)
