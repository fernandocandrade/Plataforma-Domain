
from utils.http import HttpClient
from settings.loader import load_config_file

cnf = load_config_file()

def base_url():
    event_manager = cnf["event_manager"]
    return f"{event_manager['scheme']}://{event_manager['host']}:{event_manager['port']}"



def push(event):
    url = base_url()
    client = HttpClient()
    resp = client.put(f"{url}/sendevent?appOrigin=domain_worker",event)
    if resp.has_error:
        return {}
    return resp.data