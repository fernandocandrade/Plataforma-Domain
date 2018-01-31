import json
from mapper.index import Index
from mapper.transform import Transform


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


def test_replace_all():
    index = Index()
    assert Transform(index).replace_all("a b a", "a", "c") == "c b c"


def test_replace_all_atributes():
    index = Index()
    assert Transform(index).replace_all_atributes(
        """ {"nome":"elvis"} """, "nome", "nome1") == """ {"nome1":"elvis"} """

def test_apply_runtime_fields_with_instance_none():
    model = {
        "nome":"teste",
        "meta_instance_id": None
    }
    index = Index()
    processed = Transform(index).apply_runtime_fields('BankApp','Conta', [model])
    assert '_metadata' in processed[0]
    assert 'type' in processed[0]['_metadata']
    assert processed[0]['_metadata']['type'] == 'Conta'
    assert not 'meta_instance_id' in processed[0]
    assert not 'instance_id' in processed[0]['_metadata']

def test_apply_runtime_fields_with_instance_id():
    model = {
        "nome":"teste",
        "meta_instance_id":"123"
    }
    index = Index()
    processed = Transform(index).apply_runtime_fields('BankApp','Conta', [model])
    assert '_metadata' in processed[0]
    assert 'type' in processed[0]['_metadata']
    assert processed[0]['_metadata']['type'] == 'Conta'
    assert not 'meta_instance_id' in processed[0]
    assert '123' in processed[0]['_metadata']['instance_id']


def test_apply_function_fields():
    model = {
        "saldo":10,
        "titular":"teste",
        "meta_instance_id":"123",
        "_metadata":{
            "type":"Conta"
        }
    }
    index = Index()
    index.parse(build_map())
    processed = Transform(index).apply_function_fields(model,'BankApp','Conta',{})
    assert "premio" in processed
    assert processed["premio"] == 11

def test_get_filters():
    query = {
        "filter":"transferencia",
        "origem":"teste_origem",
        "destino":"teste_destino"
    }
    index = Index()
    index.parse(build_map())
    _filter = Transform(index).get_filters('BankApp','Conta',query)

    assert 'id' in _filter
    assert '$in' in _filter['id']
    assert _filter['id']['$in'][0] == "teste_origem"
    assert _filter['id']['$in'][1] == "teste_destino"

