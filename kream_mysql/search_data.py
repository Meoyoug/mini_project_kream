from flask import Flask, Blueprint, render_template, request, jsonify, url_for, redirect
import mysql.connector
from mysql.connector import Error
import pymysql
from flask_paginate import Pagination, get_page_args

search_bp = Blueprint('main',__name__)

# MySQL 연결 설정
db = mysql.connector.connect(
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

# 검색어를 전달받으면 실행될 부분
def add_sql(sql, arg):
    if len(arg) == 1 :
        sql += ' = %s'
    else :
        sql += ' in '
        for i in range(len(arg)):
            if i == 0:
                sql += '(%s'
            else:
                sql += ', %s'
        sql += ')'
    return sql

# cursor.excute() 에 들어갈 데이터 튜플화
def add_searchData(search_data):
    sql_data = []
    if search_data['search_word']:
        sql_data.append('%' + search_data['search_word'] + '%')
    if search_data['category']:
        for i in search_data['category']:
            sql_data.append(i)
    if search_data['gender']:
        for i in search_data['gender']:
            sql_data.append(i)
    return tuple(sql_data)

def join_sql(arg,base):
    if len(arg) == 1 :
        search_sql = base + arg[0]
    elif len(arg) == 2 :
        search_sql = base + arg[0] + ' AND' + arg[1]
    elif len(arg) == 3 :
        search_sql = base + arg[0] + ' AND' + arg[1] + ' AND' + arg[2]
    else :
        search_sql = base

    return search_sql

@search_bp.route('/search_data', methods=['POST'])
def search():
    cursor = db.cursor()
    request_data = request.get_json()
    search_data = request_data.get('search_data', [])
    base_sql = "SELECT category, brand, product, price, gender FROM products WHERE"

    

    # SQL 문 동적 생성
    sql_conditions = []
    if search_data['search_word']:
        sql_conditions.append(" product LIKE %s")

    if search_data['category']:
        ctg_sql = ' category'
        ctg_sql = add_sql(ctg_sql, search_data['category'])
        sql_conditions.append(ctg_sql)

    if search_data['gender']:
        gender_sql = ' gender'
        gender_sql = add_sql(gender_sql, search_data['gender'])
        sql_conditions.append(gender_sql)

    if sql_conditions:
        search_sql = join_sql(sql_conditions, base_sql)
        excute_tuple = add_searchData(search_data)
        search_result = execute_query(search_sql, excute_tuple)
        print(search_result)
        if search_result :
            
            # 페이지 네이션 설정
            per_page =15
            page, _, offset = get_page_args(per_page=per_page)
            total = len(search_result)
            pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap5')
            # 현재 페이지에 해당하는 데이터만 보여주기
            start = offset
            end = offset + per_page
            current_datas = search_result[start:end]
            return jsonify(success=True, current_datas=current_datas, pagination={
                'page': pagination.page,
                'per_page': pagination.per_page,
                'total': pagination.total,
                'pages': list(pagination.pages),
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev,
            })
            # return render_template('search_result.html', current_datas=current_datas, pagination=pagination)
        else:
            page, per_page, offset = get_page_args()
            pagination = Pagination(page=page, per_page=per_page, total=0, css_framework='bootstrap5')
            current_datas = []
            # return render_template('search_result.html', current_datas=current_datas, pagination=pagination)
            return jsonify(success=True, current_datas=current_datas, pagination={
                'page': pagination.page,
                'per_page': pagination.per_page,
                'total': pagination.total,
                'pages': list(pagination.pages),
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev,
            })
    
    else:
        return jsonify({'success': False})

    
    