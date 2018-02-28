from flask import url_for
import pytest
from api.server import get_app
from mock import patch
from utils.http import HttpClient, ExecutionResult
import database
import json
#  from migration.sync import sync_db


def apicore_map():
    res = ExecutionResult(200)
    r = dict()
    r["name"] = "Conta"
    r["systemId"] = "ec498841-59e5-47fd-8075-136d79155705"
    r["processId"] = "61728cac-a576-4643-8e58-82a83b304053"
    r["content"] = "Conta:\r\n  model: conta\r\n  fields:\r\n    saldo:\r\n      column: saldo\r\n    titular:\r\n      column: titular\r\n  filters:\r\n    transferencia: \"id in (:origem, :destino)\""
    r["id"] = "3bc8b1b3-cd79-480b-99ca-c63de74c4f65"
    r["_metadata"] = dict()
    r["_metadata"]["type"] = "map"
    r["_metadata"]["instance_id"] = "62141389-2ef2-4715-8675-a670ad7a00cc"
    r["_metadata"]["branch"] = "master"
    res.data = [r]
    return res


@pytest.mark.usefixtures('app')
def test_persist_invalid_params(app):
    with patch.object(HttpClient, 'get', return_value=apicore_map()) as mock_method:
        client = app.test_client()
        obj = {
            "aaaa": 1,
            "_metadata": {
                "type": "wrong",
                "changeTrack": "create"
            }
        }
        response = client.post('/conta/persist', follow_redirects=True, data=json.dumps([obj]),
                               content_type='application/json')
        assert response.status_code == 400


@pytest.mark.usefixtures('app')
def test_query_valid_params(app):
    with patch.object(HttpClient, 'get', return_value=apicore_map()) as mock_method:
        obj = {
            "saldo": 1,
            "_metadata": {
                "type": "Conta",
                "changeTrack": "create"
            }
        }
        client = app.test_client()
        response = client.post('/Conta/persist', follow_redirects=True, data=json.dumps([obj]),
                               content_type='application/json')
        _list = json.loads(response.data)
        assert response.status_code == 200
        assert len(_list) == 1
        assert "id" in _list[0]


@pytest.mark.usefixtures('app')
def test_with_instance_id(app):
    with patch.object(HttpClient, 'get', return_value=apicore_map()) as mock_method:
        obj = {
            "saldo": 1,
            "_metadata": {
                "type": "Conta",
                "changeTrack": "create"
            }
        }
        client = app.test_client()
        response = client.post('/Conta/persist', follow_redirects=True, data=json.dumps([obj]),
                               content_type='application/json',  headers={'Instance-Id': '1'})
        _list = json.loads(response.data)
        assert response.status_code == 200
        assert len(_list) == 1
        assert "id" in _list[0]


@pytest.mark.usefixtures('app')
def test_with_empty_list(app):
    with patch.object(HttpClient, 'get', return_value=apicore_map()) as mock_method:
        client = app.test_client()
        response = client.post('/Conta/persist', follow_redirects=True, data=json.dumps([]),
                               content_type='application/json')
        _list = json.loads(response.data)
        assert response.status_code == 200
        assert len(_list) == 0

@pytest.mark.usefixtures('app')
def test_full_persist(app):
    #  sync_db("app_name")
    with patch.object(HttpClient, 'get', return_value=apicore_map()) as mock_method:
        _list = []
        obj = {
            "saldo": 1,
            "_metadata": {
                "type": "Conta",
                "changeTrack": "create"
            }
        }
        _list.append(obj)

        obj3 = {
            "saldo": 1,
            "id": "3",
            "_metadata": {
                "type": "Conta",
                "changeTrack": "wrong"
            }
        }
        _list.append(obj3)

        obj4 = {
            "saldo": 1,
            "id": "3"
        }
        _list.append(obj4)

        obj5 = {
            "saldo": 1,
            "id": "3",
            "_metadata": {
                "type": "Conta"
            }
        }
        _list.append(obj5)

        client = app.test_client()
        response = client.post('/Conta/persist', follow_redirects=True, data=json.dumps(_list),
                               content_type='application/json')
        _list = json.loads(response.data)
        assert response.status_code == 200
        assert len(_list) == 1
        assert "id" in _list[0]
