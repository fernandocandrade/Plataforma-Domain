from flask import Flask, request

from settings.loader import Loader as SettingsLoader
from database import create_session, create_db

from .blueprints.mapping import mapping
from utils.encoders.json import Encoder

def create_app():
    env = SettingsLoader().load()
    app = Flask(__name__, instance_relative_config=True)
    app.json_encoder = Encoder
    app.debug = False
    app.session_factory = create_session

    @app.before_request
    def create_request_session():
        setattr(request, 'session', app.session_factory())

    @app.after_request
    def destroy_request_session(response):
        request.session.close()
        return response

    app.register_blueprint(mapping)
    return app

