from uuid import uuid4
from core.mapper import User, UserClock, UserNameHistory,UserAgeHistory, session


#
#  def test_create_new_user():
    #  user = User(name='Foo')
    #  session.add(user)
    #  session.commit()
#
    #  assert session.query(UserClock).\
        #  filter(UserClock.entity_id == user.id).\
        #  count() == 1
#
    #  assert session.query(UserNameHistory).\
        #  filter(UserNameHistory.entity_id == user.id).\
        #  count() == 1
#
    #  user.name = 'Bar'
    #  session.commit()
#
    #  assert session.query(UserClock).\
        #  filter(UserClock.entity_id == user.id).\
        #  count() == 1
#
    #  assert session.query(UserNameHistory).\
        #  filter(UserNameHistory.entity_id == user.id).\
        #  count() == 2

#
#  def test_get_class_name():
    #  u = User(name="Foo")
    #  assert u.get_classname() == "User"
#
#
#  def test_get_clock_name():
    #  u = User(name="Foo")
    #  assert u.get_clock_name() == "UserClock"
#
#
#  def test_get_history_field_name():
    #  u = User(name="Foo")
    #  assert u.get_history_name(field="name") == "UserNameHistory"
#
#
#  def test_can_get_specific_tick():
    #  query = session.query(UserNameHistory).filter(
        #  UserNameHistory.ticks.contains(2))
#
    #  assert query.count() == 1
#
#
#  def test_can_join_entity_and_history():
#
    #  def build_sql(entity):
        #  cols = "public.user.id "
        #  joins = ""
#
        #  for c in entity.temporal:
            #  cols += f', public.user{c}history.value as {c}'
            #  joins += f'inner join public.user{c}history on public.user.id = public.user{c}history.entity_id '
#
        #  return cols, joins
#
    #  cols, joins = build_sql(User)
#
    #  rows = session.execute(f"""
        #  select
        #  {cols}
        #  from public.user
        #  {joins}
        #  where public.usernamehistory.ticks @> 2
    #  """)


def test_parse_dict_to_models():
    mocks = {
        "id": uuid4(),
        "name": "Parsed User",
        "age": 20,
        "_metadata": {
            "type": "User",
            "changeTrack": "create",
        }
    }

    model = session.query(User).filter(User.id == mocks["id"]).one_or_none()
    excluded = {'_metadata', 'id', }

    if not model:
        model = User()
        model.id = mocks["id"]

    has_changes = False

    for k, v in mocks.items():
        if k in excluded:
            continue

        if hasattr(model, k) and getattr(model, k, None) != v:
            has_changes = True
            setattr(model, k, v)

    if has_changes:
        session.add(model)

    session.commit()
#
    new_model = session.query(User).filter(User.id == mocks["id"]).one_or_none()
    assert new_model is not None

    new_clock = session.query(UserClock).filter(UserClock.entity_id == mocks['id']).one_or_none()
    assert new_clock.ticks == 1

    username_history = session.query(UserNameHistory).filter(UserNameHistory.entity_id == mocks['id']).one_or_none()
    assert username_history.value == "Parsed User"
    assert username_history.clock_id == new_clock.id
    assert username_history.ticks.lower == 1
    assert username_history.ticks.upper is None

    userage_history = session.query(UserAgeHistory).filter(UserAgeHistory.entity_id == mocks['id']).one_or_none()
    assert userage_history.value == 20
    assert userage_history.clock_id == new_clock.id
    assert userage_history.ticks.lower == 1
    assert userage_history.ticks.upper is None
