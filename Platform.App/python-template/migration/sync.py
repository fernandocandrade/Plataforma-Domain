import os
import glob

import sqlalchemy as sa
import yaml

from settings.loader import Loader
from model.domain import MigrationHistory
from database import db_name as DB_NAME

env = Loader().load()

DB_HOST = env["database"]["host"]
DB_USER = env["database"]["user"]
DB_PORT = 5432
DB_PASSWORD = env["database"]["password"]

# create a session
engine = sa.create_engine(
    f'postgresql+psycopg2://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}',
    echo=False)
session_factory = sa.orm.sessionmaker(bind=engine)
session = session_factory()


def diff_migrations():
    """
    diff how migrations should be executed or not
    """
    files = set(f[0] for f in get_migration_files())
    migrations = set(m[0] for m in session.query(MigrationHistory.name))
    return files - migrations


def read_migration(filename):
    with open(filename, 'r') as _file:
        return (
            os.path.basename(filename).rstrip('.yaml'),
            yaml.load(_file.read())
        )


def get_migration_files(source='./migrations'):
    """
    returns all migration files.
    """
    return [read_migration(m) for m in glob.glob(f"{source}/*.yaml")]
