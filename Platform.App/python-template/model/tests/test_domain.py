from model.domain import MigrationHistory, Conta


def test_save_migration_history(session):
    m = MigrationHistory(name="teste")

    session.add(m)
    session.commit()

    assert session.query(MigrationHistory).count() == 1

def test_save_conta(session):
    c = Conta(saldo=1, titular="Teste")
    session.add(c)
    session.commit()

    assert session.query(Conta).count() == 1
