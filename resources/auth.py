from datetime import datetime, timedelta
from functools import wraps

import jwt
from flask import request, jsonify, session
from flask_login import login_required, logout_user, login_user
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash

from app import db, app
from models import User
from schemas.user import UserSchema


class AuthRegister(Resource):
    user_schema = UserSchema()

    def post(self):
        try:
            user = self.user_schema.load(request.json, session=db.session)
        except ValidationError as e:
            return {"message": str(e)}
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {"message": "User with such username or email already exists. Please, try again."}, 409
        return self.user_schema.dump(user), 201


class AuthLogin(Resource):
    def get(self):
        auth = request.authorization
        if not auth:
            data = request.data
            print(data)
            return "", 401, {"WWW-Authenticate": "Basic realm='Authentication required'"}
        user = db.session.query(User).filter_by(username=(auth.get('username', ''))).first()
        if not user or not check_password_hash(user.password, auth.get('password', '')):
            return "", 401, {"WWW-Authenticate": "Basic realm='Authentication required'"}
        login_user(user)
        token = jwt.encode(
            {
                "user_id": user.uuid,
                "exp": datetime.now() + timedelta(hours=1)
            }, app.config['SECRET_KEY']
        )
        user.last_login = datetime.now()
        user.last_request = datetime.now()
        db.session.commit()
        return jsonify(
            {
                "token": token
            }
        )


def token_required(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        token = request.headers.get('x-api-key')
        if not token:
            return "Not Token", 401, {"WWW-Authenticate": "Basic realm='Authentication required'"}
        try:
            user_id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])['user_id']
        except (KeyError, jwt.ExpiredSignatureError):
            return "EXCEPT", 401, {"WWW-Authenticate": "Basic realm='Authentication required'"}
        user = db.session.query(User).filter_by(uuid=user_id).first()

        if not user:
            return "Not User", 401, {"WWW-Authenticate": "Basic realm='Authentication required'"}
        user.update_last_request()
        return func(self, *args, **kwargs)

    return wrapper


def get_user_by_token():
    token = request.headers.get('x-api-key')
    user_uuid = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])['user_id']
    user = db.session.query(User).filter_by(uuid=user_uuid).first()
    return user


class AuthLogout(Resource):
    def get(self):
        logout_user()
        return {'message': 'Logged Out'}, 200


class UserActivity(Resource):
    @token_required
    def get(self):
        user = get_user_by_token()
        return {'Last Login': str(user.last_login), 'Last Request': str(user.last_request)}, 200
