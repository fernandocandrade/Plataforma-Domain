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
               "transferencia": "id in (:origem, :destino)",
               "lista_ids": "id in ($ids)",
               "lista_ids1": "id in ($ids!)",
               "filtro_opcional": "[id = :id] [and titular = :titular]",
               "filtro_opcional_2": "[id in ($ids)] [and titular = :titular]"
            }
         },
         "Pessoa":{
            "model":"pessoa",
            "fields":{
               "nome":{
                  "column":"nome"
               }
            },
            "filters": " nome = :nome"
         }
      }
   }
]
     """
    _map = json.loads(json_map)
    return _map


def test_replace_all_atributes():
    index = Index()
    assert Transform(index).replace_all_atributes(
        """ {"nome":"elvis"} """, "nome", "nome1") == """ {"nome1":"elvis"} """


def test_apply_runtime_fields_with_instance_none():
    model = {
        "nome": "teste",
        "meta_instance_id": None
    }
    index = Index()
    processed = Transform(index).apply_runtime_fields(
        'BankApp', 'Conta', [model])
    assert '_metadata' in processed[0]
    assert 'type' in processed[0]['_metadata']
    assert processed[0]['_metadata']['type'] == 'Conta'
    assert not 'meta_instance_id' in processed[0]
    assert not 'instance_id' in processed[0]['_metadata']


def test_apply_runtime_fields_with_instance_id():
    model = {
        "nome": "teste",
        "meta_instance_id": "123"
    }
    index = Index()
    processed = Transform(index).apply_runtime_fields(
        'BankApp', 'Conta', [model])
    assert '_metadata' in processed[0]
    assert 'type' in processed[0]['_metadata']
    assert processed[0]['_metadata']['type'] == 'Conta'
    assert not 'meta_instance_id' in processed[0]
    assert '123' in processed[0]['_metadata']['instance_id']


def test_apply_function_fields():
    model = {
        "saldo": 10,
        "titular": "teste",
        "meta_instance_id": "123",
        "_metadata": {
            "type": "Conta"
        }
    }
    index = Index()
    index.parse(build_map())
    processed = Transform(index).apply_function_fields(
        model, 'BankApp', 'Conta', {})
    assert "premio" in processed
    assert processed["premio"] == 11


def test_get_filters():
    query = {
        "filter": "transferencia",
        "origem": "teste_origem",
        "destino": "teste_destino"
    }
    index = Index()
    index.parse(build_map())
    _filter = Transform(index).get_filters('BankApp', 'Conta', query)

    assert 'params' in _filter
    assert 'query' in _filter


def test_get_filters_with_in_filters_integer():
    query = {
        "filter": "lista_ids",
        "ids": "1;2;3"
    }
    index = Index()
    index.parse(build_map())
    _filter = Transform(index).get_filters('BankApp', 'Conta', query)
    assert 'params' in _filter
    assert 'query'  in _filter
    assert "ids"    not in _filter["params"]
    assert "ids0"   in _filter["params"]
    assert "ids1"   in _filter["params"]
    assert "ids2"   in _filter["params"]

def test_get_filters_with_in_filters_integer_as_string():
    query = {
        "filter": "lista_ids1",
        "ids": "1;2;3"
    }
    index = Index()
    index.parse(build_map())
    _filter = Transform(index).get_filters('BankApp', 'Conta', query)
    assert 'params' in _filter
    assert 'query'  in _filter
    assert "ids"    not in _filter["params"]
    assert "ids0"   in _filter["params"]
    assert "ids1"   in _filter["params"]
    assert "ids2"   in _filter["params"]
    assert type(_filter["params"]["ids0"]) is str
    assert type(_filter["params"]["ids1"]) is str
    assert type(_filter["params"]["ids2"]) is str


def test_get_filters_with_in_filters_string():
    query = {
        "filter": "lista_ids",
        "ids": "a;b;c"
    }
    index = Index()
    index.parse(build_map())
    _filter = Transform(index).get_filters('BankApp', 'Conta', query)
    assert 'params' in _filter
    assert 'query' in _filter
    assert "ids"    not in _filter["params"]
    assert "ids0"   in _filter["params"]
    assert "ids1"   in _filter["params"]
    assert "ids2"   in _filter["params"]


def test_get_filters_with_in_filters_double():
    query = {
        "filter": "lista_ids",
        "ids": "1.5;2.0;3.1"
    }
    index = Index()
    index.parse(build_map())
    _filter = Transform(index).get_filters('BankApp', 'Conta', query)
    assert 'params' in _filter
    assert 'query' in _filter
    assert "ids"    not in _filter["params"]
    assert "ids0"   in _filter["params"]
    assert "ids1"   in _filter["params"]
    assert "ids2"   in _filter["params"]


def test_get_filters_with_optional_params():
    query = {
        "filter": "filtro_opcional",
        "id": "1"
    }
    index = Index()
    index.parse(build_map())
    _filter = Transform(index).get_filters('BankApp', 'Conta', query)
    assert 'params' in _filter
    assert 'query' in _filter
    assert _filter['query'] == "id = :id"

def test_get_filters_with_optional_params_with_no_first_param():
    query = {
        "filter": "filtro_opcional",
        "titular": "1"
    }
    index = Index()
    index.parse(build_map())
    _filter = Transform(index).get_filters('BankApp', 'Conta', query)
    assert 'params' in _filter
    assert 'query' in _filter
    assert _filter['query'] == "titular = :titular"

def test_get_filters_with_optional_params_all_not_passed():
    query = {
        "filter": "filtro_opcional"
    }
    index = Index()
    index.parse(build_map())
    _filter = Transform(index).get_filters('BankApp', 'Conta', query)
    assert 'params' in _filter
    assert 'query' in _filter
    assert _filter['query'] == ""

def test_get_filters_with_optional_params_list():
    query = {
        "filter": "filtro_opcional_2",
        "ids":"1;2"
    }
    index = Index()
    index.parse(build_map())
    _filter = Transform(index).get_filters('BankApp', 'Conta', query)
    assert 'params' in _filter
    assert 'query' in _filter
    assert _filter['query'] == "id in (:ids0,:ids1)"

def test_get_filters_with_wrong_filter_name():
    query = {
        "filter": "wrong",
        "ids": "1.5;2.0;3.1"
    }
    index = Index()
    index.parse(build_map())
    _filter = Transform(index).get_filters('BankApp', 'Conta', query)
    assert _filter == {}


def test_get_filters_with_empty_params():
    query = dict()
    index = Index()
    index.parse(build_map())
    _filter = Transform(index).get_filters('BankApp', 'Conta', query)
    assert _filter == dict()


def test_get_filters_with_wrong_app():
    query = dict()
    index = Index()
    index.parse(build_map())
    _filter = Transform(index).get_filters('WApp', 'donta', query)
    assert _filter == dict()
