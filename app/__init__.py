from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret_key')
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(app.root_path), 'uploads')

    from .routes import main
    app.register_blueprint(main)

    return app
