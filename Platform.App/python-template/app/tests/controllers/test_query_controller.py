from mock import patch
from utils.http import HttpClient, ExecutionResult

from model.domain import conta


def apicore_map():
    res = ExecutionResult(200)
    r = dict()
    r["name"] = "Conta"
    r["systemId"] = "ec498841-59e5-47fd-8075-136d79155705"
    r["processId"] = "61728cac-a576-4643-8e58-82a83b304053"
    r["content"] = "Conta:\r\n  model: conta\r\n  fields:\r\n    saldo:\r\n      column: saldo\r\n    titular:\r\n      column: titular\r\n  filters:\r\n    transferencia: \"id in (:origem, :destino)\"\n    clientes: \"id in ($ids)\"\n  "
    r["id"] = "3bc8b1b3-cd79-480b-99ca-c63de74c4f65"
    r["_metadata"] = dict()
    r["_metadata"]["type"] = "map"
    r["_metadata"]["instance_id"] = "62141389-2ef2-4715-8675-a670ad7a00cc"
    r["_metadata"]["branch"] = "master"
    res.data = [r]
    return res


def test_query_invalid_params(test_client):
    with patch.object(HttpClient, 'get', return_value=apicore_map()) as mock_method:
        response = test_client.get('/conta/conta')
        assert response.status_code == 400


def test_query_valid_params(test_client):
    with patch.object(HttpClient, 'get', return_value=apicore_map()) as mock_method:
        response = test_client.get('/Conta/Conta')
        assert response.status_code == 200


def test_query_valid_params_and_query(test_client):
    with patch.object(HttpClient, 'get', return_value=apicore_map()) as mock_method:
        origem = '042f54bc-c5a1-4f9b-8ed7-d8e01ca130bf'
        destino = '042f54bc-c5a1-4f9b-8ed7-d8e01ca130bf'
        uri = f'/Conta/Conta?filter=transferencia&origem={origem}&destino={destino}'
        response = test_client.get(uri)
        assert response.status_code == 200


def test_get_data_from_map_paginated(session, test_client):
    contas = [conta(titular="Foo", saldo=i*100) for i in range(20)]
    session.add_all(contas)
    session.commit()

    with patch.object(HttpClient, 'get', return_value=apicore_map()) as mock_method:
        status_code, data = test_client.get_json(f'/Conta/Conta?page=1&page_size=10')
        assert status_code == 200
        assert len(data) == 10


def test_get_data_from_map(session, test_client):
    from mapper.builder import MapBuilder
    MapBuilder.loaded = False
    origem = conta(titular="Fabio", saldo=10000)
    destino = conta(titular="Moneda", saldo=100)
    session.add_all([origem, destino])
    session.commit()

    with patch.object(HttpClient, 'get', return_value=apicore_map()) as mock_method:
        uri = f'/Conta/Conta?filter=transferencia&origem={origem.id}&destino={destino.id}'
        status_code, resp = test_client.get_json(uri)

        assert status_code == 200
        assert len(resp) == 2

        assert resp[0]["titular"] == "Fabio"
        assert resp[0]["_metadata"]["branch"] == "master"
        assert resp[0]["saldo"] == 10000

        assert resp[1]["titular"] == "Moneda"
        assert resp[1]["_metadata"]["branch"] == "master"
        assert resp[1]["saldo"] == 100





