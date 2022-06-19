import datetime

from app import db

from models import PostLike, User, Post

user = User(username='test', email='test@example.com', password='test')
user2 = User(username='test2', email='test2@example.com', password='test2')
user3 = User(username='test3', email='test3@example.com', password='test3')
user4 = User(username='test4', email='test@example.com4', password='test4')

db.session.add(user)
db.session.add(user2)
db.session.add(user3)
db.session.add(user4)
db.session.commit()

post = Post(title='Title', text='Text')
post.created_by = user.username
post2 = Post(title='Title2', text='Text2')
post2.created_by = user2.username
post3 = Post(title='Title3', text='Text3')
post3.created_by = user3.username
post4 = Post(title='Title4', text='Text5')
post4.created_by = user4.username

db.session.add(post)
db.session.add(post2)
db.session.add(post3)
db.session.add(post4)
db.session.commit()


like = PostLike(user_id=2, post_id=1, created_at=datetime.date(year=2021, month=1, day=1))
like2 = PostLike(user_id=2, post_id=2, created_at=datetime.date(year=2021, month=2, day=1))
like3 = PostLike(user_id=2, post_id=3, created_at=datetime.date(year=2021, month=3, day=1))
like4 = PostLike(user_id=2, post_id=4, created_at=datetime.date(year=2021, month=4, day=1))
like5 = PostLike(user_id=2, post_id=5, created_at=datetime.date(year=2021, month=5, day=1))
like6 = PostLike(user_id=2, post_id=6, created_at=datetime.date(year=2021, month=6, day=1))
like7 = PostLike(user_id=2, post_id=7, created_at=datetime.date(year=2021, month=6, day=1))
like8 = PostLike(user_id=3, post_id=8, created_at=datetime.date(year=2021, month=6, day=1))
like9 = PostLike(user_id=3, post_id=9, created_at=datetime.date(year=2021, month=9, day=1))
like10 = PostLike(user_id=3, post_id=10, created_at=datetime.date(year=2021, month=9, day=1))

db.session.add(like)
db.session.add(like2)
db.session.add(like3)
db.session.add(like4)
db.session.add(like5)
db.session.add(like6)
db.session.add(like7)
db.session.add(like8)
db.session.add(like9)
db.session.add(like10)
db.session.commit()


