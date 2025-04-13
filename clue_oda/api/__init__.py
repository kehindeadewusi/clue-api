import os

from flask import Flask, jsonify
from clue_oda.settings import SECRET_KEY
from . import report_api

def create_app(testing=False):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=SECRET_KEY,
    )

    if testing:
        # load the instance config, if it exists, when not testing
        app.config.from_mapping({"DATABASE": "test"})
    else:
        # load the test config if passed in
        app.config.from_mapping({"DATABASE": "default"})

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Assert the API is up, or not
    @app.route('/')
    def hello():
        return jsonify({"message": "Hello."}), 200
    
    app.register_blueprint(report_api.bp)

    return app
