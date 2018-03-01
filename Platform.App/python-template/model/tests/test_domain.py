from model.domain import conta
from migration.sync import sync_db, drop_database
from database import create_session

def test_save_conta():

    c = conta()
    session = create_session()
    c.saldo = 1
    c.titular = "Teste"
    session.add(c)
    session.commit()
    assert session.query(conta).count() >= 1
