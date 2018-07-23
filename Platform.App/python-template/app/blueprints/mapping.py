import json

from flask import Blueprint, request, jsonify

from mapper.builder import MapBuilder
from app.services import QueryService
from app.controllers import QueryController, CommandController
from model.batch import BatchPersistence
import log


mapping = Blueprint('simple_page', __name__)


def error(exception, code=400):
    log.critical(str(exception))
    resp = {
        "message": str(exception),
        "code": code,
    }
    return jsonify(resp), code


def http_handler(func):
    def _handler(*args, **kwargs):
        try:
            ret = func(*args, **kwargs)
            return jsonify(ret)
        except Exception as ex:
            return error(ex)
    return _handler


@mapping.route("/<app_id>/<entity>", methods=['GET'])
@http_handler
def query_map(app_id, entity,):
    """ Query data on domain """
    mapper = MapBuilder().build()
    reference_date = request.headers.get('Reference-Date')
    version = request.headers.get('Version')
    branch = request.headers.get('Branch', 'master')

    query_service = QueryService(
        reference_date, version, request.session, branch)
    controller = QueryController(
        app_id, entity, request.args.to_dict(), mapper, query_service)

    return controller.query()


@mapping.route("/<app_id>/<entity>/history/<entity_id>", methods=['GET'])
def query_history(app_id, entity, entity_id):
    """ Query data on domain """
    try:
        mapper = MapBuilder().build()
        reference_date = request.headers.get('Reference-Date')
        version = request.args.get('version')
        query_service = QueryService(
            reference_date, version=None, session=request.session)
        controller = QueryController(
            app_id, entity, request.args.to_dict(), mapper, query_service)

        r = list(controller.history(entity_id, version))
        return jsonify(r)
    except Exception as excpt:
        return error(excpt)


@mapping.route("/<app_id>/persist", methods=['POST'])
def persist_map(app_id):
    """ Persist data on domain """
    instance_id = request.headers.get('Instance-Id')
    process_id = request.headers.get('Process-Id')
    reference_date = request.headers.get('Reference-Date')
    body = json.loads(request.data)
    controller = CommandController(app_id, body, instance_id, reference_date, process_id)
    try:
        return jsonify(controller.persist())
    except Exception as excpt:
        r = {"status_code": 400, "message": str(excpt)}
        return jsonify(r), 400

@mapping.route("/instance/<process_instance>/persist", methods=['POST'])
def persist_entities_by_process_instance(process_instance):
    controller = CommandController(None, None, None, None, None)
    ok = controller.persist_by_instance(process_instance)
    resp = {"message":ok}
    return jsonify(resp)


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


@mapping.route("/instance/<process_instance>/entities", methods=['GET'])
def entities_by_process_instance(process_instance):
    bat = BatchPersistence(None)
    entities = bat.get_entities(process_instance)
    return jsonify(entities)
