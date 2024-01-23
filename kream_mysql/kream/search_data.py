from flask import Blueprint, render_template, request
from flask_paginate import Pagination, get_page_args
from kream.main import execute_query, update_date

search_bp = Blueprint('search',__name__)

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
def add_searchData(keyword, category, gender):
    sql_data = []
    if keyword:
        sql_data.append('%' + keyword + '%')
    if category:
        for i in category:
            sql_data.append(i)
    if gender:
        for i in gender:
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

@search_bp.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword', '')
    category = request.args.getlist('category')
    gender = request.args.getlist('gender')
    base_sql = "SELECT category, brand, product, price, gender, img, product_link, kr_description FROM products WHERE"

    # SQL 문 동적 생성
    sql_conditions = []
    if keyword:
        sql_conditions.append(" product LIKE %s")

    if category:
        ctg_sql = ' category'
        ctg_sql = add_sql(ctg_sql, category)
        sql_conditions.append(ctg_sql)

    if gender:
        for i, gen in enumerate(gender) :
            if gen == '남성' :
                gender[i] = 'male'
            elif gen == '여성' :
                gender[i] = 'female'
            elif gen == '키즈' :
                gender[i] = 'kids'
            elif gen == '남여공용' :
                gender[i] = 'unisex'
            elif gen == 'N/A' :
                gender[i] = None

        gender_sql = ' gender'
        gender_sql = add_sql(gender_sql, gender)
        sql_conditions.append(gender_sql)

    if sql_conditions:
        search_sql = join_sql(sql_conditions, base_sql)
        excute_tuple = add_searchData(keyword, category, gender)
        search_result = execute_query(search_sql, excute_tuple)
        
        # 검색결과가 있으면 페이지네이션 설정후 해당데이터 출력
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
            return render_template('search.html', results = current_datas, update_date=update_date, pagination=pagination)
        
        # 검색결과가 없으면 비어있는 리스트를 보여줌
        else:
            page, per_page, offset = get_page_args()
            pagination = Pagination(page=page, per_page=per_page, total=0, css_framework='bootstrap5')
            current_datas = []
            return render_template('search.html', results=current_datas, update_date=update_date, pagination=pagination)

    # 입력된 값이 없으면 전체데이터를 보여줌
    else:
        search_result = execute_query('SELECT category, brand, product, price, gender, img, product_link, kr_description FROM products',())
        # 페이지 네이션 설정
        per_page =15
        page, _, offset = get_page_args(per_page=per_page)
        total = len(search_result)
        pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap5')
        # 현재 페이지에 해당하는 데이터만 보여주기
        start = offset
        end = offset + per_page
        current_datas = search_result[start:end]
        return render_template('search.html', results = current_datas, update_date=update_date, pagination=pagination)


    
    