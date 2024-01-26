from flask import Flask, render_template, Blueprint
from flask_paginate import Pagination, get_page_args
from datetime import datetime
import pymysql

main_bp = Blueprint('main', __name__)

db = pymysql.connect(
        host='localhost',
        user='root',
        password='eodyd456@',
        database='kream_new_product'
)

def execute_query(query, args=None):
    with db.cursor() as cursor:
        cursor.execute(query, args or ())
        if query.strip().upper().startswith('SELECT'):
            return cursor.fetchall()
        else:
            db.commit()

update_date = datetime.now().strftime("%Y-%m-%d    %H시 %M분")

@main_bp.route('/')
def index():
    #MySQL에서 데이터 가져오기
    datas = []
    sql = "SELECT category, brand, product, price, gender, img, product_link, kr_description FROM products"
    try : 
        datas = execute_query(sql)

    except Exception as e :
        print(f"Error: {e}")

    # 페이지 네이션 설정
    page, per_page, offset = get_page_args()
    total = len(datas)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap5')

    # 현재 페이지에 해당하는 데이터만 보여주기
    start = offset
    end = offset + per_page
    current_datas = datas[start:end]

    return render_template('index.html', datas=current_datas, update_date=update_date, pagination=pagination)
 





