from flask import Blueprint, request, jsonify, session, redirect, url_for
from app.services.stock_service import get_stock_data
from .models import db, User, Transaction

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/search/<ticker>', methods=['GET'])
def search_stock(ticker):
    data = get_stock_data(ticker)
    if data:
        return jsonify(data), 200
    return jsonify({'error': 'Stock not found'}), 404

@api_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if username and password:
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({'message': 'User already exists'}), 400

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'Registered successfully'}), 201
    return jsonify({'message': 'Registration failed'}), 400

@api_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        session['user_id'] = user.id
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'message': 'Login failed'}), 401

@api_blueprint.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@api_blueprint.route('/buy', methods=['POST'])
def buy_stock():
    user_id = session.get('user_id')
    if not user_id:
        return 'Please log in'

    ticker = request.form['ticker']
    shares = int(request.form['shares'])
    price = float(request.form['price'])

    transaction = Transaction(user_id=user_id, stock_ticker=ticker, shares=shares, price_per_share=price, transaction_type='buy')
    db.session.add(transaction)
    db.session.commit()
    return 'Stock purchased'
