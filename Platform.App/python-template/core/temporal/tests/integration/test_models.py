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


#
#  def test_can_get_specific_tick():
    #  query = session.query(UserNameHistory).filter(
        #  UserNameHistory.ticks.contains(2))
#
    #  assert query.count() == 1
#
#
def test_can_retrieve_multiple_models(session, create_model, update_model):
    # act
    user = create_model(User, name='Foo', age=20,)
    update_model(user, name="Bar",age=21)

    #  models = session.query(*[v for v in User._history.values()]).all()
    query = session.query(
        User._history['name'].value,
        User._history['age'].value,
    ).join(
        User._history['name'].entity_id,
        User._history['age'].entity_id
    ).filter(
        User._history['name'].ticks.contains(1),
        User._history['age'].ticks.contains(1)
    )

    #  for m in query.all():
        #  print(m)

    print(query)

    #  for u, hn, ha in query:
        #  print(u.id, hn.value, ha.value)

    #  for m in query.all():
        #  print(m.value)
    #  models = session.query(
        #  User._history['name'].value).\
        #  options(orm.joinedload(
            #  User._history['name'].entity, innerjoin=True))






















#  def test_can_join_entity_and_history(session):

#
    #  for k,v in User._history.items():
        #  print(v)
#
    #  query = session.query([User] + [v for v in User._history.values()])
    #  print(query)

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
#

#  def test_parse_dict_to_models():
    #  mocks = {
        #  "id": uuid4(),
        #  "name": "Parsed User",
        #  "age": 20,
        #  "_metadata": {
            #  "type": "User",
            #  "changeTrack": "create",
        #  }
    #  }
#
    #  model = session.query(User).filter(User.id == mocks["id"]).one_or_none()
    #  excluded = {'_metadata', 'id', }
#
    #  if not model:
        #  model = User()
        #  model.id = mocks["id"]
#
    #  has_changes = False
#
    #  for k, v in mocks.items():
        #  if k in excluded:
            #  continue
#
        #  if hasattr(model, k) and getattr(model, k, None) != v:
            #  has_changes = True
            #  setattr(model, k, v)
#
    #  if has_changes:
        #  session.add(model)
#
    #  session.commit()

    #  new_model = session.query(User).filter(User.id == mocks["id"]).one_or_none()
    #  assert new_model is not None
#
    #  new_clock = session.query(UserClock).filter(UserClock.entity_id == mocks['id']).one_or_none()
    #  assert new_clock.ticks == 1
#
    #  username_history = session.query(UserNameHistory).filter(UserNameHistory.entity_id == mocks['id']).one_or_none()
    #  assert username_history.value == "Parsed User"
    #  assert username_history.clock_id == new_clock.id
    #  assert username_history.ticks.lower == 1
    #  assert username_history.ticks.upper is None
#
    #  userage_history = session.query(UserAgeHistory).filter(UserAgeHistory.entity_id == mocks['id']).one_or_none()
    #  assert userage_history.value == 20
    #  assert userage_history.clock_id == new_clock.id
    #  assert userage_history.ticks.lower == 1
    #  assert userage_history.ticks.upper is None
