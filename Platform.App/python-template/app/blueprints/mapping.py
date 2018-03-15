import json

from flask import Blueprint, request, jsonify

from mapper.builder import MapBuilder
from app.services import QueryService
from app.controllers import QueryController, CommandController
import log

mapping = Blueprint('simple_page', __name__)


@mapping.route("/<app_id>/<entity>", methods=['GET'])
def query_map(app_id, entity):
    """ Query data on domain """
    try:
        mapper = MapBuilder().build()
        reference_date = request.headers.get('Reference-Date')
        version = request.headers.get('Version')

        query_service = QueryService(reference_date, version, request.session)
        controller = QueryController(app_id, entity, request.args.to_dict(), mapper,
                                     query_service)

        r = controller.query()
        return jsonify(r)
    except Exception as excpt:
        log.critical(str(excpt))
        resp = dict()
        resp["message"] = str(excpt)
        resp["code"] = 400
        return jsonify(resp), resp["code"]


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

@mapping.route("/<app_id>/<instance_id>/persist_async", methods=['POST'])
def persist_async(app_id, instance_id):
    """ Persist data on domain based on process memory last commit"""
    return jsonify([])