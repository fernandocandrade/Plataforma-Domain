from model.domain import MigrationHistory, conta
from database import create_session



def test_save_migration_history(session):
    m = MigrationHistory(name="teste")

    session.add(m)
    session.commit()

def test_save_conta():

    c = conta()
    session = create_session()
    c.saldo = 1
    c.titular = "Teste"
    session.add(c)
    session.commit()
    assert session.query(conta).count() == 1
