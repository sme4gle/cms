from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from flask_migrate import Migrate

from config.database import db
from controllers import app
from models import *


def create_app(test=False) -> Flask:
    cms = Flask(__name__)
    cms.register_blueprint(app, url_prefix='/')
    cms.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://cmsdemo:pw@localhost:5432/cmsdemo"
    cms.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(cms)
    cms.secret_key = 'QWxzIGplIGRpdCBsZWVzdCBoZWIgamUgZWVuIGVhc3RlcmVnZyBnZXZvbmRlbi4='
    migrate = Migrate(cms, db)


    return cms

if __name__ == '__main__':
    create_app().run(debug=True)

