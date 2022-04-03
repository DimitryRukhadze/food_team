import os

from flask import Flask, send_from_directory

from . import api_user


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'db.json'),
        IMAGES_FOLDER=os.path.join(app.instance_path, './images'),
        JSON_AS_ASCII=False
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    app.register_blueprint(api_user.user_bp)

    @app.route("/images/<path:filename>")
    def download_file(filename):
        return send_from_directory(
            app.config['IMAGES_FOLDER'], filename
        )

    return app
