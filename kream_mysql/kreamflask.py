from flask import Flask, render_template, request, jsonify, url_for
import mysql.connector
from mysql.connector import Error
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from flask_paginate import Pagination, get_page_args
import subprocess
import time
from search_data import search_bp
import logging

# Flask 객체 인스턴스 생성
app = Flask(__name__)
# 검색부분 블루프린터 등록
app.register_blueprint(search_bp)
# MySQL 연결 설정
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='eodyd456@',
    database='kream_new_product'
)
def read_crawlFile():
    # kream.py 파일을 subprocess를 통해 실행
    crawl_file = subprocess.Popen(["python", "crawling.py"])

 # 스케줄러를 통해서 Flask가 살행되는 동안 하루마다 db를 업데이트 하도록 설정
def crawling_scahduler():
    # 스케줄러 설정
    scheduler = BackgroundScheduler()
    scheduler.add_job(read_crawlFile, 'interval', minutes =60)  # 매일 아침 9시에 db가 업데이트 되도록 설정

    # Flask 애플리케이션 실행 전에 스케줄러 시작
    scheduler.start()
crawling_scahduler()

@app.route('/')
def index():
    #MySQL에서 데이터 가져오기
    datas = []
    try : 
        cursor = db.cursor()
        cursor.execute("SELECT category, brand, product, price, gender FROM products")
        datas = cursor.fetchall()

    except Exception as e :
        print(f"Error: {e}")

    finally:
        if cursor:
            cursor.close()

    # 페이지 네이션 설정
    per_page =15
    page, _, offset = get_page_args(per_page=per_page)
    total = len(datas)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap5ç')
    # 현재 페이지에 해당하는 데이터만 보여주기
    start = offset
    end = offset + per_page
    current_datas = datas[start:end]
    return render_template('index.html', datas = current_datas, pagination=pagination)

@app.route('/delete_data', methods=['POST'])
def delete_data():
    cursor = db.cursor()
    request_data = request.get_json()
    products = request_data.get('products', [])
    print(products)
    if products:
        # MySQL db에서 선택된 product 이름에 해당하는 데이터를 제거
        for product in products:
            sql = "DELETE FROM products WHERE product = %s"
            cursor.execute(sql, (product,))
            db.commit()
        return jsonify({'success' : True})
    else : 
        return jsonify({'success' : False, 'message' : '선택된 데이터가 없습니다.' })
    
if __name__ == "__main__":
    app.run(debug=True)




if db:
    db.close()