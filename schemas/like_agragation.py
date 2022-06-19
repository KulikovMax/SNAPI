from flask_marshmallow import Schema
from flask_marshmallow.fields import fields


class LikeAggregationSchema(Schema):
    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True)
