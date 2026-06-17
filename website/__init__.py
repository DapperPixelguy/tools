from flask import Flask
import os
from dotenv import load_dotenv
load_dotenv()


def create_app():

    app = Flask(__name__)

    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads')

    from .main import main
    app.register_blueprint(main)

    return app