from utils.http import HttpClient
from settings.loader import Loader


class MapCore:
    def __init__(self):
        self.http = HttpClient()
        self.config = Loader().load()

    def find_by_system_id(self, system_id):
        """ get map on api core by system id"""
        core_services = self.config["core_services"]
        url = f"{core_services['scheme']}://{core_services['host']}:{core_services['port']}/core/map?filter=bySystemId&systemId={system_id}"
        result = self.http.get(url)
        if result.status_code == 200:
            return result.data
        return []
