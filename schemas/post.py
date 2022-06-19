from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from models import Post


class PostSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        exclude = ('id',)
        include_fk = True
        load_instance = True
