from flask import Flask
import os



def create_app():
    app = Flask(__name__)

    UPLOAD_FOLDER = os.path.join("static", "zdjecia")
    # ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER



    return app