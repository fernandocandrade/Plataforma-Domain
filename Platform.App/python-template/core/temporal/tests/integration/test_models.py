
from sqlalchemy import orm
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

