from core.mapper import User, UserClock, UserNameHistory, session


def test_create_new_user():
    user = User(name='Foo')
    session.add(user)
    session.commit()

    assert session.query(UserClock).\
        filter(UserClock.entity_id == user.id).\
        count() == 1

    assert session.query(UserNameHistory).\
        filter(UserNameHistory.entity_id == user.id).\
        count() == 1

    user.name = 'Bar'
    session.commit()

    assert session.query(UserClock).\
        filter(UserClock.entity_id == user.id).\
        count() == 1

    assert session.query(UserNameHistory).\
        filter(UserNameHistory.entity_id == user.id).\
        count() == 2
#
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
#  def test_instance_clock_entity():
    #  u = User(name="Foo")
    #  assert isinstance(u.get_clock_entity(), UserClock)
#
#
#  def test_build_entity_history():
    #  u = User(name="Foo")
    #  clock = u.get_clock_entity()
    #  history = u.get_entity_history("name", clock)
#
    #  assert history.value == "Foo"
#
#
#  def test_can_get_specific_tick():
    #  query = session.query(UserNameHistory).filter(
        #  UserNameHistory.ticks.contains(2))
#
    #  assert query.count() > 1
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
