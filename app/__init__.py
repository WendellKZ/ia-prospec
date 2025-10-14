from flask import Flask
from .db import init_db
from .routes import bp
from .celery_app import make_celery
from config import Config

celery = None

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    init_db()
    app.register_blueprint(bp)
    global celery
    celery = make_celery(app, eager=Config.CELERY_TASK_ALWAYS_EAGER)
    return app
