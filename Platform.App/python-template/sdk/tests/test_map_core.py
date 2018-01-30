
from sdk.map_core import MapCore

def test_get_map_from_apicore():
    map = MapCore()
    maps_loaded = map.find_by_system_id("ec498841-59e5-47fd-8075-136d79155705")
    assert len(maps_loaded) == 1

def test_returns_empty_when_not_exist():
    map = MapCore()
    maps_loaded = map.find_by_system_id("ec498841-59e5-47fd-8075-136d79155706")
    assert len(maps_loaded) == 0
