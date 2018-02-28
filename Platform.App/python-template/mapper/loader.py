
""" Loader loads maps from api core and from Mapas directory """
import yaml
from os import listdir
import os.path
from sdk.map_core import MapCore
from core.component import Component
import log


class Loader(Component):
    def __init__(self, local_source='maps'):
        super().__init__()
        self.map_core = MapCore()
        self.local_source = local_source

    def get_local_map_file_names(self):
        """ return local files to load """
        if not os.path.isdir(self.local_source):
            return []
        files = list(filter(lambda f: f.endswith(
            ".yaml"), listdir(self.local_source)))
        return files

    def get_map_from_api_core(self):
        """ get maps from core api """
        return self.map_core.find_by_system_id(self.config['solution']['id'])

    def build_local_maps(self):
        """ build local maps data structure """
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
        """ build remote maps data structure """
        for current_map in self.get_map_from_api_core():
            yield {
                "app_name": current_map['name'],
                "map": yaml.load(current_map['content'])
            }

    def build(self):
        """ returns all maps available to this application """
        local_maps = self.build_local_maps()
        if self.config["app"]["name"] == "apicore":
            return local_maps
        remote_maps = []
        try:
            remote_maps = self.build_remote_maps()
        except Exception as expt:
            log.info(str(expt))
        return local_maps + list(remote_maps)
