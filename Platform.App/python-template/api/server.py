""" Server API """
from flask import Flask, request
from api.query_controller import QueryController
from api.command_controller import CommandController
app = Flask(__name__)

@app.route("/<app_id>/<entity>", methods=['GET'])
def query_map(app_id, entity):
    """ Query data on domain """
    controller = QueryController(app_id, entity, request)
    return controller.query()


@app.route("/<app_id>/persist", methods=['POST'])
def persist_map(app_id):
    """ Persist data on domain """
    controller = CommandController(app_id, request)
    return controller.persist()

def run():
    """Run Api Server"""
    app.run()
