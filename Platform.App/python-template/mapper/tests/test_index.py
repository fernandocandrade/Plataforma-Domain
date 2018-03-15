""" Map Index Tests """
import json
from mapper.index import Index


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
                  "column":"saldo"
               },
               "titular":{
                  "column":"titular"
               },
               "premio":{
                   "type":"function",
                   "eval": "obj.saldo * 1.1"
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


def test_apply_default_attr():
    """ should index map into many index structure """
    index = Index()
    r = index.apply_default_fields(build_map()[0])
    assert 'BankApp' in r['app_name']
    assert 'id' in r['map']['Conta']['fields']
    assert 'meta_instance_id' in r['map']['Conta']['fields']


def test_parse():
    """ should index map into many index structure """
    index = Index()
    index.parse(build_map())
    assert 'BankApp' in index.model_cache
    assert 'Conta' in index.model_cache['BankApp']
    assert 'fields' in index.model_cache['BankApp']['Conta']
    assert 'attributes' in index.projection_cache['BankApp']['Conta']


def test_get_map_by_app_id():
    index = Index()
    index.parse(build_map())
    assert index.get_map('BankApp') != None


def test_get_map_by_app_id_wrong():
    index = Index()
    index.parse(build_map())
    assert index.get_map('Wrong') == dict()


def test_get_map_by_app_id_and_name():
    index = Index()
    index.parse(build_map())
    assert index.get_map('BankApp', 'Conta') != None


def test_get_map_by_app_id_and_name_wrong_name():
    index = Index()
    index.parse(build_map())
    assert index.get_map('BankApp', 'Wrong') == dict()


def test_get_map_by_app_id_and_name_wrong():
    index = Index()
    index.parse(build_map())
    assert index.get_map('Wrong', 'Wrong') == dict()


def test_get_projection():
    index = Index()
    index.parse(build_map())
    proj = index.get_projection("BankApp")
    assert 'Conta' in proj
    assert 'attributes' in proj['Conta']
    for p in proj['Conta']['attributes']:
        assert p[0] == p[1]


def test_get_filters():
    index = Index()
    index.parse(build_map())
    assert "transferencia" in index.get_filters("BankApp", "Conta")

def test_get_filters_wrong_type():
    index = Index()
    index.parse(build_map())
    assert index.get_filters("w", "conta") == dict()


def test_get_filters_wrong():
    index = Index()
    index.parse(build_map())
    assert index.get_filters("W", "W") == dict()

def test_get_model_name():
    index = Index()
    index.parse(build_map())
    assert index.get_model_name('BankApp','Conta') == "conta"

def test_get_model_name_wrong():
    index = Index()
    index.parse(build_map())
    assert index.get_model_name('AABankApp','Conta') == dict()

def test_get_functions():
    index = Index()
    index.parse(build_map())
    assert "premio" in index.get_functions('BankApp','Conta')

def test_get_functions_without_functions():
    index = Index()
    index.parse(build_map())
    assert index.get_functions('BankApp','Pessoa') == dict()

def test_get_map_type_by_domain_type():
    index = Index()
    index.parse(build_map())
    assert index.get_map_type_by_domain_type('BankApp','conta') == "Conta"

def test_get_map_type_by_domain_type_wrong():
    index = Index()
    index.parse(build_map())
    assert index.get_map_type_by_domain_type('BankApp','wrong') == ""


def test_columns_from_map_type():
    index = Index()
    index.parse(build_map())
    _map = index.columns_from_map_type("BankApp","Conta")
    for col, reference in _map:
        assert col == reference

