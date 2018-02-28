from model.domain import MigrationHistory
from migration.sync import diff_migrations, get_migration_files


def config():
    return {
        "app": {
            "name": "teste"
        }
    }


def test_should_load_migration_files():
    migrations = get_migration_files(source='./fixtures/migrations')
    name, content = migrations[0]

    assert len(migrations) == 2
    assert name == 'A'
    assert 'create_table' in content


def test_should_return_no_migration_to_migrate(session):
    to_migrate = diff_migrations()
    assert len(to_migrate) == 0
    assert "B" in to_migrate

