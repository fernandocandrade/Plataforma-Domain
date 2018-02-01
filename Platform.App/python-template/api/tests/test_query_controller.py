from flask import url_for
import pytest
from api.server import get_app
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


@pytest.mark.usefixtures('app')
def test_query_invalid_params(app):
    with patch.object(HttpClient, 'get', return_value=apicore_map()) as mock_method:
        client = app.test_client()
        response = client.get('/conta/conta', follow_redirects=True)
        assert response.status_code == 400


@pytest.mark.usefixtures('app')
def test_query_valid_params(app):
    with patch.object(HttpClient, 'get', return_value=apicore_map()) as mock_method:
        client = app.test_client()
        response = client.get('/Conta/Conta', follow_redirects=True)
        print(response.data)
        assert response.status_code == 200

@pytest.mark.usefixtures('app')
def test_query_valid_params_and_query(app):
    with patch.object(HttpClient, 'get', return_value=apicore_map()) as mock_method:
        client = app.test_client()
        response = client.get('/Conta/Conta?filter=transferencia&origem=1&destino=2', follow_redirects=True)
        print(response.data)
        assert response.status_code == 200
