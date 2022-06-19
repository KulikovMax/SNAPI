from app import api
from resources.agragation import LikeAggregation
from resources.auth import AuthLogin, AuthRegister, AuthLogout, UserActivity
from resources.blog import BlogPost, BlogPostLike
from resources.smoke import Smoke

api.add_resource(Smoke, '/', strict_slashes=True)
api.add_resource(AuthRegister, '/signup', strict_slashes=True)
api.add_resource(AuthLogin, '/login', strict_slashes=True)
api.add_resource(BlogPost, '/posts', '/posts/<uuid>', strict_slashes=True)
api.add_resource(BlogPostLike, '/posts/<uuid>/like', strict_slashes=True)
api.add_resource(AuthLogout, '/logout', strict_slashes=True)
api.add_resource(LikeAggregation, '/analytics', strict_slashes=True)
api.add_resource(UserActivity, '/user-activity', strict_slashes=True)
