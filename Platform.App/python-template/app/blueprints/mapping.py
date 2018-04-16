import json

from flask import Blueprint, request, jsonify

from mapper.builder import MapBuilder
from app.services import QueryService
from app.controllers import QueryController, CommandController
import log

mapping = Blueprint('simple_page', __name__)


def error(exception, code=400):
    log.critical(str(exception))
    resp = {
        "message": str(exception),
        "code": code,
    }
    return jsonify(resp), code


@mapping.route("/<app_id>/<entity>", methods=['GET'])
def query_map(app_id, entity):
    """ Query data on domain """
    try:
        mapper = MapBuilder().build()
        reference_date = request.headers.get('Reference-Date')
        version = request.headers.get('Version')

        query_service = QueryService(reference_date, version, request.session)
        controller = QueryController(
            app_id, entity, request.args.to_dict(), mapper, query_service)

        r = controller.query()
        return jsonify(r)
    except Exception as excpt:
        return error(excpt)

@mapping.route("/<app_id>/<entity>/history/<entity_id>", methods=['GET'])
def query_history(app_id, entity, entity_id):
    """ Query data on domain """
    try:
        mapper = MapBuilder().build()
        reference_date = request.headers.get('Reference-Date')

        query_service = QueryService(
            reference_date, version=None, session=request.session)
        controller = QueryController(
            app_id, entity, request.args.to_dict(), mapper, query_service)

        r = list(controller.history(entity_id))
        return jsonify(r)
    except Exception as excpt:
        return error(excpt)

@mapping.route("/<app_id>/persist", methods=['POST'])
def persist_map(app_id):
    """ Persist data on domain """
    instance_id = request.headers.get('Instance-Id')
    reference_date = request.headers.get('Reference-Date')
    body = json.loads(request.data)
    controller = CommandController(app_id, body, instance_id, reference_date)
    try:
        return jsonify(controller.persist())
    except Exception as excpt:
        r = {"status_code": 400, "message": str(excpt)}
        return jsonify(r), 400

@mapping.route("/mapper/cache", methods=['PUT'])
def enable_cache():
    MapBuilder.cache_enable = True
    return jsonify({"message":f"Cache enabled={MapBuilder.cache_enable}"})

@mapping.route("/mapper/cache", methods=['GET'])
def show_mapper_cache():
    return jsonify({"message":f"Cache enabled={MapBuilder.cache_enable}"})

@mapping.route("/mapper/cache", methods=['DELETE'])
def disable_cache():
    MapBuilder.cache_enable = False
    return jsonify({"message":f"Cache enabled={MapBuilder.cache_enable}"})
