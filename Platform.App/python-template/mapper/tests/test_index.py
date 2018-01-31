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
         }
      }
   }
]
     """
    _map = json.loads(json_map)
    return _map


def test_index_maps():
    """ should index map into many index structure """
    index = Index(build_map())
    assert len(index.maps) == 1

def test_apply_default_attr():
    """ should index map into many index structure """
    index = Index(build_map())
    r = index.apply_default_fields(index.maps[0])
    assert 'BankApp' in r['app_name']
    assert 'id' in r['map']['Conta']['fields']
    assert 'meta_instance_id' in r['map']['Conta']['fields']

def test_parse():
    """ should index map into many index structure """
    index = Index(build_map())
    index.parse(index.maps)
    assert 'BankApp' in index.model_cache
    assert 'Conta' in index.model_cache['BankApp']
    assert 'fields' in index.model_cache['BankApp']['Conta']
    assert 'attributes' in index.projection_cache['BankApp']['Conta']