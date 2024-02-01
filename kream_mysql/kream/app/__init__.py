from flask import Flask
from kream.app.search_data import search_bp
from kream.app.update import update_bp
from kream.app.delete import delete_bp
from kream.app.main import main_bp
from kream.app.info import info_bp

def create_app():
    app = Flask(__name__)

    # 블루프린트 등록
    app.register_blueprint(main_bp)
    app.register_blueprint(update_bp)
    app.register_blueprint(delete_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(info_bp)

    return app