from flask import Flask
import os
from flask_login import LoginManager

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.secret_key = "super sekvert key!!"

    UPLOAD_FOLDER = os.path.join("static", "zdjecia")
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

    login_manager.init_app(app)
    login_manager.login_view = "login"



    return app