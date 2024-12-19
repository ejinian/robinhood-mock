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
        print("logged in")
        session['user_id'] = user.id
        print(session)
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'message': 'Login failed'}), 401

@api_blueprint.route('/logout')
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out successfully'}), 200


@api_blueprint.route('/buy', methods=['POST'])
def buy_stock():
    print("got here")
    print(session)
    if 'user_id' not in session:
        print("happened")
        return jsonify({'message': 'Please log in'}), 401

    data = request.get_json()
    ticker = data['ticker']
    shares = int(data.get('shares', 1))
    price = float(data['price'])
    print("got here2")

    transaction = Transaction(
        user_id=session['user_id'],
        stock_ticker=ticker,
        shares=shares,
        price_per_share=price,
        transaction_type='buy'
    )
    db.session.add(transaction)
    db.session.commit()
    return jsonify({'message': 'Stock purchased'}), 200

@api_blueprint.route('/portfolio', methods=['GET'])
def get_portfolio():
    if 'user_id' not in session:
        return jsonify({'message': 'Please log in'}), 401

    user_id = session['user_id']
    transactions = Transaction.query.filter_by(user_id=user_id).all()
    portfolio_data = [
        {
            'ticker': transaction.stock_ticker,
            'shares': transaction.shares,
            'price_per_share': transaction.price_per_share,
            'transaction_type': transaction.transaction_type,
            'timestamp': transaction.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'cost_of_purchase': transaction.price_per_share * transaction.shares
        }
        for transaction in transactions
    ]
    return jsonify(portfolio_data), 200
