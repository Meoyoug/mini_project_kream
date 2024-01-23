from flask import Flask , redirect, url_for, Blueprint, jsonify
from datetime import datetime
import subprocess
update_bp = Blueprint('update', __name__)


@update_bp.route('/update', methods = ['GET'])
def operate_crawlFile():
    try:
        # kream.py 파일을 subprocess를 통해 실행하도록 하는 부분
        subprocess.Popen(["python", "kream/crawling.py"])
        return redirect(url_for('main.index'))

    except :
        return jsonify({'success' : False, 'massage' : '업데이트 실패'})