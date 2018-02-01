""" Server API """
from flask import Flask, request
from api.query_controller import QueryController
from api.command_controller import CommandController
from mapper.builder import MapBuilder, Loader
from app.query_service import QueryService

app = Flask(__name__)


@app.route("/<app_id>/<entity>", methods=['GET'])
def query_map(app_id, entity):
    """ Query data on domain """
    mapper = MapBuilder().build()
    query_service = QueryService()
    controller = QueryController(app_id, entity, request,mapper,query_service)
    return controller.query()


@app.route("/<app_id>/persist", methods=['POST'])
def persist_map(app_id):
    """ Persist data on domain """
    mapper = MapBuilder().build()
    controller = CommandController(app_id, request, mapper)
    return controller.persist()

def run():
    """Run Api Server"""
    app.run()
