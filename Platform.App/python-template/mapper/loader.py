
""" Loader loads maps from api core and from Mapas directory """
import yaml
from os import listdir
from env.loader import Loader as EnvLoader
from sdk.map_core import MapCore


class Loader:
    def __init__(self):
        self.config = EnvLoader().load()
        self.map_core = MapCore()
        self.local_source = "maps"

    def get_local_map_file_names(self):
        """ return local files to load """
        files = list(filter(lambda f: f.endswith(
            ".yaml"), listdir(self.local_source)))
        return files

    def get_map_from_api_core(self):
        """ get maps from core api """
        print(self.config["core_services"])
        return self.map_core.find_by_system_id(self.config['solution']['id'])

    def build_local_maps(self):
        files = self.get_local_map_file_names()
        maps = []
        for current_file in files:
            content = open(f"{self.local_source}/{current_file}", "r").read()
            item = {
                "app_name": current_file.replace(".yaml", ""),
                "map": yaml.load(content)
            }
            maps.append(item)
        return maps

    def build_remote_maps(self):
        maps_to_build = self.get_map_from_api_core()
        maps = []
        for current_map in maps_to_build:
            item = {
                "app_name": current_map['name'],
                "map": yaml.load(current_map['content'])
            }
            maps.append(item)
        return maps

    def build(self):
        local_maps = self.build_local_maps()
        remote_maps = self.build_remote_maps()
        return local_maps + remote_maps
