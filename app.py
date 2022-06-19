from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)
api = Api(app)
login_manager = LoginManager(app)



SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': 'StarNavi API'})
app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)

import routes


if __name__ == '__main__':
    app.run()
