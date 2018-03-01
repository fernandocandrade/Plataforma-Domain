import json
import os.path
import errno


def read_json(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError(
            errno.ENOENT,
            os.strerror(errno.ENOENT),
            f'config file {filename} must exist.')

    with open(filename, "r") as _file:
        return json.loads(_file.read())


def load_config_file():
    """ Load confiuration file """
    config = read_json("plataforma.json")

    config["database"] = {
        "name": config["app"]["name"],
        "host": os.environ.get("POSTGRES_HOST", "localhost"),
        "user": os.environ.get('POSTGRES_USER', "postgres"),
        "password": os.environ.get('POSTGRES_PASSWORD', ""),
    }

    config["http"] = {
        'port': int(os.environ.get('PORT', 9090)),
    }

    config['core_services'] = {
        "scheme": os.environ.get('COREAPI_SCHEME', "http"),
        "host": os.environ.get('COREAPI_HOST', "apicore"),
        "port": os.environ.get('COREAPI_PORT', "9110"),
    }

    return config
