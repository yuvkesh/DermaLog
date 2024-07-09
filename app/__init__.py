from flask import Flask
import os

def create_app():
    app = Flask(__name__, template_folder='../templates')
    app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with a real secret key
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(app.root_path), 'uploads')

    from .routes import main
    app.register_blueprint(main)

    return app
