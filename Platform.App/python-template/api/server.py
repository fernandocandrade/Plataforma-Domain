""" Server API """
import json
from flask import Flask, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from api.query_controller import QueryController
from api.command_controller import CommandController
from mapper.builder import MapBuilder, Loader
from app.query_service import QueryService
from settings.loader import Loader
from database import db_session
env = Loader().load()
app = Flask(__name__, instance_relative_config=True)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route("/<app_id>/<entity>", methods=['GET'])
def query_map(app_id, entity):
    """ Query data on domain """
    try:

        mapper = MapBuilder().build()
        query_service = QueryService()
        controller = QueryController(
            app_id, entity, request, mapper, query_service)
        return jsonify(controller.query())
    except Exception as excpt:
        resp = dict()
        resp["message"] = excpt.args[0]
        resp["code"] = 400
        return jsonify(resp), resp["code"]


@app.route("/<app_id>/persist", methods=['POST'])
def persist_map(app_id):
    """ Persist data on domain """
    try:
        instance_id = request.headers.get('Instance-Id')
        mapper = MapBuilder().build()
        body = json.loads(request.data)
        controller = CommandController(app_id, body, mapper, instance_id)
        return jsonify(controller.persist())
    except Exception as excpt:
        r = {
            "status_code": 400,
            "message": excpt.args[0]
        }
        return jsonify(r), 400
