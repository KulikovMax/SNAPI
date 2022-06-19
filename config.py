import pathlib

BASE_DIR = pathlib.Path(__file__).parent

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(BASE_DIR) + "/db.sqlite3"
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = 'secret_key'