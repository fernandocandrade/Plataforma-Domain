''' Main Module starts all domain app components '''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from settings.loader import Loader


conf = Loader().load()
db_host = conf["database"]["host"]
app = Flask(__name__, instance_relative_config=True)
db = SQLAlchemy(app)
db.init_app(app)
from api.server import api
from model.domain import get_db_name
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+pyscopg2://postgres@{db_host}:5432/{get_db_name()}'
app.register_blueprint(api, url_prefix='/')
