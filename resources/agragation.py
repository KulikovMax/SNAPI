import datetime

from flask import request
from flask_restful import Resource, reqparse
from sqlalchemy import func

from app import db
from models import PostLike, Post
from resources.auth import token_required
from schemas.like_agragation import LikeAggregationSchema


class LikeAggregation(Resource):
    aggregation_schema = LikeAggregationSchema()

    @token_required
    def get(self):
        args = request.args.to_dict()
        print(args)
        date_from = datetime.datetime.strptime(args['date_from'], '%Y-%m-%d')
        print(date_from)
        date_to = datetime.datetime.strptime(args['date_to'], '%Y-%m-%d')
        result = db.session.query(func.count(PostLike.id), PostLike.created_at).filter(
            PostLike.created_at.between(date_from, date_to)).group_by(PostLike.created_at).all()
        data = {str(r.created_at):r[0] for r in result}
        return data, 200
