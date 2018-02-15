from model.domain import MigrationHistory, Conta
from migration.sync import sync_db
from database import create_session


def test_save_migration_history():
    sync_db()
    m = MigrationHistory()
    m.name = "teste"

    session = create_session()
    session.add(m)
    session.commit()

def test_save_conta():
    sync_db()
    c = Conta()
    session = create_session()
    c.saldo = 1
    c.titular = "Teste"
    session.add(c)
    session.commit()

    assert "id" in c.dict()
    assert "titular" in c.dict()
    assert "saldo" in c.dict()
    assert c.dict()["saldo"] == 1
    assert c.dict()["titular"] == "Teste"
