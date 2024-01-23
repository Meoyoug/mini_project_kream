from flask import Blueprint, jsonify, request
from kream.main import execute_query


delete_bp = Blueprint('delete', __name__)

@delete_bp.route('/delete_data', methods=['POST'])
def delete_data():
    request_data = request.get_json()
    products = request_data.get('products', [])
    if products:
        # MySQL db에서 선택된 product 이름에 해당하는 데이터를 제거
        for product in products:
            sql = "DELETE FROM products WHERE product = %s"
            execute_query(sql, (product,))
            
        # 성공적으로 제거됐으면 성공했다고 응답
        return jsonify({'success' : True})
    
    else : 
        # db삭제에 실패했다면 실패에 대한 응답
        return jsonify({'success' : False, 'message' : '선택된 데이터가 없습니다.' })