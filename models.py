import uuid
from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from app import db, login_manager


class PostLike(db.Model):
    __tablename__ = 'post_like'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    created_at = db.Column(db.Date, default=datetime.now())


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, index=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime(), nullable=False)
    last_request = db.Column(db.DateTime(), nullable=False)
    uuid = db.Column(db.String(36), unique=True)
    post = db.relationship('Post')
    liked = db.relationship(
        'PostLike',
        foreign_keys='PostLike.user_id',
        backref='user', lazy='dynamic')

    def __init__(self, username, email, password, is_admin=False):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.is_admin = is_admin
        self.uuid = str(uuid.uuid4())
        self.last_login = datetime(1970, 1, 1, 0, 0, 1, 1)
        self.last_request = datetime(1970, 1, 1, 0, 0, 1, 1)

    def __repr__(self):
        return f'User: {self.username}, Email: {self.email}'

    def update_last_request(self):
        self.last_request = datetime.now()
        db.session.commit()

    def make_admin(self):
        self.is_admin = True

    def like_post(self, post):
        if not self.has_liked_post(post):
            like = PostLike(user_id=self.id, post_id=post.id)
            db.session.add(like)
            db.session.commit()
            return like

    def unlike_post(self, post):
        if self.has_liked_post(post):
            PostLike.query.filter_by(
                user_id=self.id,
                post_id=post.id).delete()
            db.session.commit()

    def has_liked_post(self, post):
        return PostLike.query.filter(PostLike.user_id == self.id, PostLike.post_id == post.id).count() > 0

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).filter_by(id=user_id).first()

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), unique=True, index=True, nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime)
    created_by = db.Column(db.String(128), db.ForeignKey('users.id'))
    uuid = db.Column(db.String(36), unique=True)

    def __init__(self, title, text):
        self.title = title
        self.text = text
        self.created_at = datetime.now()
        self.uuid = str(uuid.uuid4())

    def __repr__(self):
        return f'Post: {self.title} by {self.created_by}. Created at:{self.created_at}'
