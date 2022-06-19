from flask import request, session
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from app import db
from models import Post
from resources.auth import token_required, get_user_by_token
from schemas.like import PostLikeSchema
from schemas.post import PostSchema





class BlogPost(Resource):
    post_schema = PostSchema()

    @token_required
    def get(self, uuid=None):
        if not uuid:
            posts = db.session.query(Post).all()
            return self.post_schema.dump(posts, many=True), 200
        post = db.session.query(Post).filter_by(uuid=uuid).first()
        if not post:
            return 'Not Fount', 404
        return self.post_schema.dump(post), 200

    @token_required
    def post(self):
        print(session.values())
        try:
            user = get_user_by_token()
            post = self.post_schema.load(request.json, session=db.session)
            post.created_by = user.username
        except ValidationError as e:
            return {"message": str(e)}
        try:
            db.session.add(post)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {"message": "Such post exists, change title."}, 409
        return self.post_schema.dump(post), 201


class BlogPostLike(Resource):
    like_schema = PostLikeSchema()

    @token_required
    def post(self, uuid):
        user = get_user_by_token()
        post = db.session.query(Post).filter_by(uuid=uuid).first()
        like = user.like_post(post)
        if like is None:
            return {"message": "You already liked this post."}, 403
        return self.like_schema.dump(like), 201

    @token_required
    def delete(self, uuid):
        user = get_user_by_token()
        post = db.session.query(Post).filter_by(uuid=uuid).first()
        user.unlike_post(post)
        return {'message': 'Deleted'}, 204
