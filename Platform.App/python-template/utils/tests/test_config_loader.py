
from utils.config_loader import load_config_file
import json
import os
import pytest
def test_load_app_config_file():
    config = {
        "app":{
            "type":"domain",
            "name":"app_name",
            "id":"a2ce149c-ab61-499b-a0d0-14594b2e9ea3"
        },
        "solution":{
            "name":"solution name",
            "id":"ec498841-59e5-47fd-8075-136d79155705"
        }
    }
    file = open("plataforma.json", "w")
    file.write(json.dumps(config))
    file.close()
    conf = load_config_file()
    assert conf["app"]["id"] == config["app"]["id"]
    assert conf["app"]["type"] == config["app"]["type"]
    assert conf["solution"]["id"] == config["solution"]["id"]
    assert  "database" in conf and "http" in conf and "core_services" in conf
