''' Main Module starts all domain app components '''
import api.server as server
from migration.sync import sync_db
from flask_sqlalchemy import SQLAlchemy
from settings.loader import Loader
from model.domain import get_db_name
env = Loader().load()
db_host = env["database"]["host"]
app = server.get_app()
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+pyscopg2://postgres@{db_host}:5432/{get_db_name()}'
db = SQLAlchemy(app)
sync_db(db)
server.run()