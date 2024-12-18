from flask import Blueprint, request, jsonify
from app.services.stock_service import get_stock_data

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/search/<ticker>', methods=['GET'])
def search_stock(ticker):
    data = get_stock_data(ticker)
    if data:
        return jsonify(data), 200
    return jsonify({'error': 'Stock not found'}), 404
