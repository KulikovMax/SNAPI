from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from models import PostLike


class PostLikeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PostLike
        include_fk = True
