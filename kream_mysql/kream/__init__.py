from flask import Flask
from kream.search_data import search_bp
from kream.update import update_bp
from kream.delete import delete_bp
from kream.main import main_bp
from kream.info import info_bp

def create_app():
    app = Flask(__name__)

    # 블루프린트 등록
    app.register_blueprint(main_bp)
    app.register_blueprint(update_bp)
    app.register_blueprint(delete_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(info_bp)

    return app