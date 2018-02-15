
from settings.loader import Loader
import database
from migration.sync import *
import pytest
import os
from uuid import uuid4
from mock import patch
import shutil


def config():
    return {
        "app": {
            "name": "teste"
        }
    }


def test_should_create_and_drop_new_database():
    assert should_create_database("test1") == True

    create_database("test1")

    assert should_create_database("test1") == False

    drop_database("test1")

    assert should_create_database("test1") == True


def test_should_syncronize_model():
    sync_db()
    assert len(raw_sql("app_name", "select * from migrationhistory")) == 0


def test_should_migrate_model():
    if should_create_database("app_name"):
        create_database("app_name")
    sync_db()


def create_migration(name="1-AddTableAddress"):
    migration = open(f"./migrations/{name}.yaml", "w")
    migration.write("""
      create_table:
        name: tb_address
        columns:
            client_id:
            type: string
            street:
            type: string
            number:
            type: integer
            zipCode:
            type: string
    """)
    migration.close()


def delete_migration(name="1-AddTableAddress"):
    os.remove(f"./migrations/{name}.yaml")


def create_migration_folder():
    if not os.path.exists("migrations"):
        os.mkdir("migrations")
    else:
        shutil.rmtree('./migrations')
        os.mkdir("migrations")


def test_should_load_migration_files():
    create_migration_folder()
    create_migration()
    files = get_migration_files()
    assert len(files) == 1
    assert "content" in files[0]
    assert "name" in files[0]


def test_should_return_no_migration_to_migrate():
    create_migration_folder()
    create_migration("A")
    create_migration("B")
    insert_new_migration("1-AddTableAddress")
    insert_new_migration("A")
    to_migrate = diff_migrations()
    _list = list(to_migrate)
    assert len(_list) == 1
    assert _list[0]["name"] == "B"


''' def test_should_migrate_table():
    create_migration_folder()
    name = "TableToMigrate"
    migration = open(f"./migrations/{name}.yaml", "w")
    migration.write("""
      create_table:
        name: teste
        columns:
            name:
                type: string
    """)
    migration.close()
    insert_new_migration("B")
    migrate("app_name")

    raw_execute("app_name", "insert into teste (name) values ('testing')")
    r = raw_sql("app_name", "select * from teste")
    assert len(r) == 1 '''
