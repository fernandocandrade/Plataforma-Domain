import pytest
from mock import patch
from utils.http import HttpClient, ExecutionResult
from sdk.map_core import MapCore
from sdk.branch_link import BranchLink
import json

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

def apicore_branch_link():
    res = ExecutionResult(200)
    r = dict()
    r["systemId"] = "ec498841-59e5-47fd-8075-136d79155705"
    r["entity"] = "conta"
    r["branch"] = "cenario-01"
    r["id"] = "3bc8b1b3-cd79-480b-99ca-c63de74c4f65"
    r["_metadata"] = dict()
    r["_metadata"]["type"] = "branchLink"
    r["_metadata"]["instance_id"] = "62141389-2ef2-4715-8675-a670ad7a00cc"
    r["_metadata"]["branch"] = "master"
    res.data = [r]
    return res


def test_valid_system_id():
    with patch.object(HttpClient, 'get', return_value=apicore_map()) as mock_method:
        core = MapCore()
        _map = core.find_by_system_id("1")
        assert "name" in _map[0]

def test_invalid_system_id():
    not_found = apicore_map()
    not_found.status_code = 404
    with patch.object(HttpClient, 'get', return_value=not_found) as mock_method:
        core = MapCore()
        _map = core.find_by_system_id("1")
        assert _map == []


def test_get_branch_link_with_valid_system_id():
    with patch.object(HttpClient, 'get', return_value=apicore_branch_link()) as mock_method:
        core = BranchLink()
        _map = core.get_by_system_id("1")
        assert "systemId" in _map[0]
        assert "branch" in _map[0]
        assert "entity" in _map[0]

