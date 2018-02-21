""" Server API """
import json
from flask import Flask, request, jsonify
from api.query_controller import QueryController
from api.command_controller import CommandController
from mapper.builder import MapBuilder
from app.query_service import QueryService
from settings.loader import Loader as SettingsLoader
from database import create_session

env = SettingsLoader().load()
app = Flask(__name__, instance_relative_config=True)
app.debug = False


@app.route("/<app_id>/<entity>", methods=['GET'])
def query_map(app_id, entity):
    """ Query data on domain """
    req_session = create_session()
    try:
        mapper = MapBuilder().build()
        reference_date = request.headers.get('Reference-Date')
        version = request.headers.get('Version')
        query_service = QueryService(reference_date, version, req_session)
        controller = QueryController(app_id, entity, request.args.to_dict(), mapper,
                                     query_service)
        return jsonify(controller.query())
    except Exception as excpt:
        resp = dict()
        resp["message"] = str(excpt)
        resp["code"] = 400
        return jsonify(resp), resp["code"]


@app.route("/<app_id>/persist", methods=['POST'])
def persist_map(app_id):
    """ Persist data on domain """
    instance_id = request.headers.get('Instance-Id')
    reference_date = request.headers.get('Reference-Date')
    body = json.loads(request.data)
    print(body)
    controller = CommandController(app_id, body, instance_id, reference_date)
    try:
        return jsonify(controller.persist())
    except Exception as excpt:
        r = {"status_code": 400, "message": str(excpt)}
        return jsonify(r), 400
    finally:
        controller.session.close()


@app.route("/ping", methods=['GET'])
def ping():
    return "pong"


def get_app():
    return app
