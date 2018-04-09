from datetime import datetime, timezone

from sqlalchemy import orm
from sqlalchemy import text
from sqlalchemy import bindparam
from core.temporal.tests.integration.mocks import User


def test_create_new_model_creates_model_clock(session, create_model, query_by_entity):
    # act
    user = create_model(User, name='Foo', age=20)

    # retrieve
    clock = query_by_entity(User._clock, user.id).one()

    # assert
    assert clock.ticks == 1


def test_update_model_increases_model_clock(session, create_model, update_model, query_by_entity):
    # act
    user = create_model(User, name='Foo', age=20)
    update_model(user, name='Bar')

    # retrieve one and only one clock.
    clock = query_by_entity(User._clock, user.id).one()

    # assert
    assert clock.ticks == 2


def test_create_new_model_creates_fields_history(session, create_model, query_by_entity):
    # act
    user = create_model(User, name="Foo", age=20)

    # retrieve
    age_history = query_by_entity(user._history['age'], user.id).one()
    name_history = query_by_entity(user._history['name'], user.id).one()

    # assert
    assert age_history.value == 20
    assert age_history.ticks.lower == 1

    assert name_history.value == 'Foo'
    assert name_history.ticks.lower == 1


def test_update_model_creates_fields_history(session, create_model, update_model, query_entity_history):
    # act
    user = create_model(User, name='Foo', age=20,)
    update_model(user, name='Bar', age=10,)

    # retrieve
    name_history = query_entity_history(user, 'name')
    age_history = query_entity_history(user, 'age')

    # assert
    assert len(name_history) == 2

    assert name_history[0].value == 'Bar'
    assert name_history[0].ticks.lower == 2
    assert name_history[0].ticks.upper is None

    assert name_history[1].value == 'Foo'
    assert name_history[1].ticks.lower == 1
    assert name_history[1].ticks.upper == 2

    assert len(age_history) == 2

    assert age_history[0].value == 10
    assert age_history[0].ticks.lower == 2
    assert age_history[0].ticks.upper is None

    assert age_history[1].value == 20
    assert age_history[1].ticks.lower == 1
    assert age_history[1].ticks.upper == 2


def test_update_model_does_not_duplicate_unchanged_fields(session, create_model, update_model, query_entity_history):
    # act
    user = create_model(User, name='Foo', age=20,)
    update_model(user, name='Bar',)

    # retrieve
    age_history = query_entity_history(user, 'age')

    # assert
    assert len(age_history) == 1
    assert age_history[0].value == 20
    assert age_history[0].ticks.lower == 1
    assert age_history[0].ticks.upper is None


def test_delete_model_mark_clock_as_deleted(session, create_model, delete_model, query_entity_clock):
    # mock
    user = create_model(User, name='Foo', age=20,)

    # act
    delete_model(user)
    user_clock = query_entity_clock(user, period=datetime.now(tz=timezone.utc))

    # assert
    assert user_clock.one().deleted == True


def test_get_model_history(session, create_model, update_model):
    # mock
    user = create_model(User, name='Foo', age=20,)
    update_model(user, name='Bar')

    # act
    user_db = session.query(User).history().one()

    # assert
    assert user_db.name == 'Bar' and user_db.age == 20


def test_get_model_history_with_filter(session, create_model, update_model):
    # mock
    user = create_model(User, name='Foo', age=21,)
    user = create_model(User, name='Bar', age=20,)

    # act
    user = session.query(User).history().filter(text('name=:name', bindparams=[
        bindparam('name', value='Foo')
    ])).one()

    # assert
    assert user.name == 'Foo' and user.age == 21


def test_get_model_history_at_specific_version(session, create_model, update_model):
    #  mock
    user = create_model(User, name='Foo', age=20,)
    update_model(user, name='Bar')

    # act
    user = session.query(User).history(version=1).one()

    # assert
    assert user.name == 'Foo' and user.age == 20


def test_create_1k_models(session):
    users = [User(name=f'Foo {i}', age=i) for i in range(2000)]
    import time
    start = time.time()
    session.add_all(users)
    session.commit()
    stop = time.time() - start
    print(f'\n\n*** Execution time: {stop}')

