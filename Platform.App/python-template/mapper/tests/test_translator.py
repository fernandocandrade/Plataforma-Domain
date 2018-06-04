import json
from mapper.index import Index
from mapper.translator import Translator
import pytest

def build_map():
    """ build default test map """
    json_map = """
    [
   {
      "app_name":"BankApp",
      "map":{
         "Conta":{
            "model":"conta",
            "fields":{
               "saldo":{
                  "column":"cl_saldo"
               },
               "titular":{
                  "column":"cl_titular"
               },
               "premio":{
                   "type":"function",
                   "eval": "item['saldo'] * 1.1"
               }
            },
            "filters":{
               "transferencia":{
                  "id":{
                     "$in":[
                        ":origem",
                        ":destino"
                     ]
                  }
               }
            }
         },
         "Pessoa":{
            "model":"pessoa",
            "fields":{
               "nome":{
                  "column":"nome"
               }
            },
            "filters":{
               "byNome":{
                  "nome": ":nome"
               }
            }
         }
      }
   }
]
     """
    _map = json.loads(json_map)
    return _map


def test_to_domain():
    index = Index()
    index.parse(build_map())
    mapped = {
        "saldo":10,
        "titular": "teste",
        "_metadata":{
            "type":"Conta"
        }
    }
    domain = Translator(index).to_domain('BankApp',mapped)
    assert "cl_saldo" in domain
    assert "cl_titular" in domain
    assert domain["cl_saldo"] == mapped["saldo"]
    assert domain["cl_titular"] == mapped["titular"]

def test_to_domain_with_wrong_type():
    index = Index()
    index.parse(build_map())
    mapped = {
        "saldo":10,
        "titular": "teste",
        "_metadata":{
            "type":"conta"
        }
    }
    with pytest.raises(AttributeError):
        Translator(index).to_domain('BankApp',mapped)

def test_to_domain_without_metadata():
    index = Index()
    index.parse(build_map())
    mapped = {
        "saldo":10,
        "titular": "teste"
    }
    domain = Translator(index).to_domain('BankApp',mapped)
    assert "saldo" in domain
    assert "titular" in domain
    assert domain["saldo"] == mapped["saldo"]
    assert domain["titular"] == mapped["titular"]


def test_to_map():
    index = Index()
    index.parse(build_map())
    domain = {
        "id": "13123",
        "meta_instance_id":"1313123",
        "cl_saldo":10,
        "cl_titular": "teste",
        "_metadata": {
            "type":"conta"
        }
    }
    mapped = Translator(index).to_map('BankApp',domain)

    assert "saldo" in mapped
    assert "titular" in mapped
    assert domain["cl_saldo"] == mapped["saldo"]
    assert domain["cl_titular"] == mapped["titular"]


def test_to_map_without_metadata():
    index = Index()
    index.parse(build_map())
    domain = {
        "id": "13123",
        "meta_instance_id":"1313123",
        "cl_saldo":10,
        "cl_titular": "teste"
    }
    mapped = Translator(index).to_map('BankApp',domain)
    assert "cl_saldo" in mapped
    assert "cl_titular" in mapped
