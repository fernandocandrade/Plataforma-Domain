from core.mapper import User, UserClock, UserNameHistory, session



def test_create_new_user():
    user = User(name='Foo')
    session.add(user)
    session.commit()

    assert session.query(UserClock).\
        filter(UserClock.entity_id==user.id).\
        one() is not None

    assert session.query(UserNameHistory).\
        filter(UserNameHistory.entity_id==user.id).\
        one() is not None

#
def test_get_class_name():
    u = User(name="Foo")
    assert u.get_classname() == "User"


def test_get_clock_name():
    u = User(name="Foo")
    assert u.get_clock_name() == "UserClock"


def test_get_history_field_name():
    u = User(name="Foo")
    assert u.get_history_name(field="name") == "UserNameHistory"


def test_instance_clock_entity():
    u = User(name="Foo")
    assert isinstance(u.get_clock_entity(), UserClock)


def test_build_entity_history():
    u = User(name="Foo")
    clock = u.get_clock_entity()
    history = u.get_entity_history("name", clock)

    assert history.value == "Foo"
