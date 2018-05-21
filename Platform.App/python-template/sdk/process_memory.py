
from utils.http import HttpClient
from settings.loader import load_config_file

cnf = load_config_file()

def base_url():
    process_memory = cnf["process_memory"]
    return f"{process_memory['scheme']}://{process_memory['host']}:{process_memory['port']}"


def save_document(collection, data):
    url = base_url()
    client = HttpClient()
    resp = client.post(f"{url}/{collection}?app_origin=domainWorker", data)
    if resp.has_error:
        return False
    return True

def head(instance_id):
    url = base_url()
    client = HttpClient()
    resp = client.get(f"{url}/{instance_id}/head?app_origin=domainWorker")
    if resp.has_error:
        return {}
    return resp.data

def first(instance_id):
    url = base_url()
    client = HttpClient()
    resp = client.get(f"{url}/{instance_id}/first?app_origin=domainWorker")
    if resp.has_error:
        return {}
    return resp.data