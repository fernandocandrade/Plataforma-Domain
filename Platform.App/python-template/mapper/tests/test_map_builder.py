import mock
import json
from mapper.builder import MapBuilder
from mapper.loader import Loader
import mock
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




def test_should_build_mapp():
    with mock.patch.object(Loader, 'build', return_value=build_map()) as mock_method:
        _map = MapBuilder().build()
        assert _map.index != None
        assert _map.transform != None
        assert _map.translator != None



