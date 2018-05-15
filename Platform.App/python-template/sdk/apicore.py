from utils.http import HttpClient
from settings.loader import Loader
from core.component import Component
import log

class ApiCore(Component):

    def __init__(self):
        super().__init__()
        self.http = HttpClient()

    def mount_get_url(self, entity, params):
        core_services = self.config["core_services"]
        url = f"{core_services['scheme']}://{core_services['host']}:{core_services['port']}/core/{entity}"

        query_string = ""
        if params:
            query_string = "?"
            for k,v in params.items():
                query_string += str(k) + "=" + str(v) + "&"

        url += query_string
        return url

    def get(self, entity, params):
        """ get on api core"""
        url = self.mount_get_url(entity, params)
        result = self.http.get(url)
        if result.status_code == 200:
            return result.data
        raise Exception(result.error_message)


    def get_by_system_id(self, entity):
        params = {
            "filter":"bySystemId",
            "systemId": self.system_id()
        }
        return self.get(entity, params)

    def persist(self, items):
        if len(items) == 0:
            return
        core_services = self.config["core_services"]
        url = f"{core_services['scheme']}://{core_services['host']}:{core_services['port']}/core/persist"
        result = self.http.post(url, items)
        if result.status_code == 200:
            return result.data
        raise Exception(result.error_message)

    def parse_array(self, lst):
        return ";".join(lst)
