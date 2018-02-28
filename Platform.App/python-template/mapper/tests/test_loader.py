from mapper.loader import Loader
from mock import patch

from utils.http import HttpClient, ExecutionResult


def apicore_map():
    res = ExecutionResult(200)
    r = dict()
    r["name"] = "Conta"
    r["systemId"] = "ec498841-59e5-47fd-8075-136d79155705"
    r["processId"] = "61728cac-a576-4643-8e58-82a83b304053"
    r["content"] = "Conta:\r\n  model: conta\r\n  fields:\r\n    saldo:\r\n      column: saldo\r\n    titular:\r\n      column: titular\r\n  filters:\r\n    transferencia:\r\n      id:\r\n        $in:\r\n          - \":origem\"\r\n          - \":destino\""
    r["id"] = "3bc8b1b3-cd79-480b-99ca-c63de74c4f65"
    r["_metadata"] = dict()
    r["_metadata"]["type"] = "map"
    r["_metadata"]["instance_id"] = "62141389-2ef2-4715-8675-a670ad7a00cc"
    r["_metadata"]["branch"] = "master"
    res.data = [r]
    return res


def test_get_files_to_load():
    l = Loader(local_source="fixtures/maps")
    files = l.get_local_map_file_names()
    assert len(files) == 1


def test_build_local_maps():
    l = Loader(local_source="fixtures/maps")
    m = l.build_local_maps()
    assert len(m) == 1
    assert m[0]['app_name'] == "Conta"


def test_build_remote_maps():
    with patch.object(HttpClient, 'get', return_value=apicore_map()) as mock_method:
        l = Loader(local_source="fixtures/maps")
        m = list(l.build_remote_maps())
    assert len(m) == 1
    assert m[0]['app_name'] == "Conta"


def test_build_maps():
    with patch.object(HttpClient, 'get', return_value=apicore_map()) as mock_method:
        l = Loader(local_source="fixtures/maps")
        m = list(l.build())
    assert len(m) == 2
