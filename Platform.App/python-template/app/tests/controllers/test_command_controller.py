from flask import url_for
import pytest
from mock import patch
from utils.http import HttpClient, ExecutionResult
from sdk.branch_link import BranchLink
import database
from model.domain import conta
import json


def apicore_map():
    res = ExecutionResult(200)
    r = dict()
    r["name"] = "Conta"
    r["systemId"] = "ec498841-59e5-47fd-8075-136d79155705"
    r["processId"] = "61728cac-a576-4643-8e58-82a83b304053"
    r["content"] = "Conta:\r\n  model: conta\r\n  fields:\r\n    _saldo:\r\n      column: saldo\r\n    _titular:\r\n      column: titular\r\n  filters:\r\n    transferencia: \"id in (:origem, :destino)\""
    r["id"] = "3bc8b1b3-cd79-480b-99ca-c63de74c4f65"
    r["_metadata"] = dict()
    r["_metadata"]["type"] = "map"
    r["_metadata"]["instance_id"] = "62141389-2ef2-4715-8675-a670ad7a00cc"
    r["_metadata"]["branch"] = "master"
    res.data = [r]
    return res

def link_branch():
    r = dict()
    r["branch"] = "cenario-01"
    r["entity"] = "conta"
    r["systemId"] = "ec498841-59e5-47fd-8075-136d79155705"
    r["id"] = "3bc8b1b3-cd79-480b-99ca-c63de74c4f65"
    r["_metadata"] = dict()
    r["_metadata"]["type"] = "branchLink"
    r["_metadata"]["instance_id"] = "62141389-2ef2-4715-8675-a670ad7a00cc"
    r["_metadata"]["branch"] = "master"
    return [r]


@pytest.mark.usefixtures('app')
def test_persist_invalid_params(app):
    with patch.object(HttpClient, 'get', return_value=apicore_map()) as mock_method:
        with patch.object(BranchLink, 'get_links', return_value=[]) as mock_method1:
            with patch.object(BranchLink, 'save', return_value=[]) as mock_method2:
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
        with patch.object(BranchLink, 'get_links', return_value=[]) as mock_method1:
            with patch.object(BranchLink, 'save', return_value=[]) as mock_method2:
                obj = {
                    "_saldo": 1,
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
        with patch.object(BranchLink, 'get_links', return_value=[]) as mock_method1:
            with patch.object(BranchLink, 'save', return_value=[]) as mock_method2:
                obj = {
                    "_saldo": 1,
                    "_metadata": {
                        "type": "Conta",
                        "changeTrack": "create"
                    }
                }
                client = app.test_client()
                response = client.post('/Conta/persist', follow_redirects=True, data=json.dumps([obj]),
                                    content_type='application/json',  headers={'Instance-Id': 'fef2e75b-6cdb-46a7-96d4-76c20481c1cb'})
                _list = json.loads(response.data)
                assert response.status_code == 200
                assert len(_list) == 1
                assert "id" in _list[0]


@pytest.mark.usefixtures('app')
def test_with_empty_list(app):
    with patch.object(HttpClient, 'get', return_value=apicore_map()) as mock_method:
        with patch.object(BranchLink, 'get_links', return_value=[]) as mock_method1:
            with patch.object(BranchLink, 'save', return_value=[]) as mock_method2:
                client = app.test_client()
                response = client.post('/Conta/persist', follow_redirects=True, data=json.dumps([]),
                                    content_type='application/json')
                _list = json.loads(response.data)
                assert response.status_code == 200
                assert len(_list) == 0

@pytest.mark.usefixtures('app')
def test_full_persist(app):
    with patch.object(HttpClient, 'get', return_value=apicore_map()) as mock_method:
        with patch.object(BranchLink, 'get_links', return_value=[]) as mock_method1:
            with patch.object(BranchLink, 'save', return_value=[]) as mock_method2:
                _list = []
                obj = {
                    "_saldo": 1,
                    "_metadata": {
                        "type": "Conta",
                        "changeTrack": "create"
                    }
                }
                _list.append(obj)

                obj3 = {
                    "_saldo": 1,
                    "id": "3",
                    "_metadata": {
                        "type": "Conta",
                        "changeTrack": "wrong"
                    }
                }
                _list.append(obj3)

                obj4 = {
                    "_saldo": 1,
                    "id": "3"
                }
                _list.append(obj4)

                obj5 = {
                    "_saldo": 1,
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

def test_destroy_data(session, test_client):
    origem = conta(titular="Fabio", saldo=10000)
    destino = conta(titular="Moneda", saldo=100)
    session.add_all([origem, destino])
    session.commit()

    with patch.object(HttpClient, 'get', return_value=apicore_map()) as mock_method:
        with patch.object(BranchLink, 'get_links', return_value=[]) as mock_method1:
            with patch.object(BranchLink, 'save', return_value=[]) as mock_method2:
                uri = f'/Conta/Conta?filter=transferencia&origem={origem.id}&destino={destino.id}'
                status_code, resp = test_client.get_json(uri)
                destroyed_id = resp[0]["id"]
                resp[0]["_metadata"]["changeTrack"] = "destroy"
                body = json.dumps([resp[0]])
                assert len(resp) == 2
                response = test_client.post('/Conta/persist',follow_redirects=True, data=body,
                                    content_type='application/json')

                assert response.status_code == 200

                status_code, resp = test_client.get_json(uri)
                assert status_code == 200
                assert len(resp) == 1
                assert resp[0]["id"] != destroyed_id

                uri = f'/Conta/Conta'
                status_code, resp = test_client.get_json(uri)
                assert response.status_code == 200
                assert status_code == 200
                assert len(resp) == 1
                assert resp[0]["id"] != destroyed_id


def test_should_not_insert_new_link_branch(app):
     with patch.object(HttpClient, 'get', return_value=apicore_map()) as mock_method:
        with patch.object(BranchLink, 'get_links', return_value=link_branch()) as mock_get_links:
            with patch.object(BranchLink, 'save', return_value=[]) as mock_save:
                obj = {
                    "_saldo": 1,
                    "_metadata": {
                        "type": "Conta",
                        "changeTrack": "create",
                        "branch": "cenario-01"
                    }
                }
                client = app.test_client()
                response = client.post('/Conta/persist', follow_redirects=True, data=json.dumps([obj]),
                                    content_type='application/json')
                assert response.status_code == 200
                mock_save.assert_called_with([])

def test_should_insert_new_link_branch(app):
     with patch.object(HttpClient, 'get', return_value=apicore_map()) as mock_method:
        with patch.object(BranchLink, 'get_links', return_value=[]) as mock_get_links:
            with patch.object(BranchLink, 'save', return_value=[]) as mock_save:
                obj = {
                    "_saldo": 1,
                    "_metadata": {
                        "type": "Conta",
                        "changeTrack": "create",
                        "branch": "cenario-02"
                    }
                }
                client = app.test_client()
                response = client.post('/Conta/persist', follow_redirects=True, data=json.dumps([obj]),
                                    content_type='application/json')
                assert response.status_code == 200
                mock_save.assert_called_with([{"entity":"conta", "branch":"cenario-02"}])