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
    return jsonify({'message': 'Logged out successfully'}), 200


@api_blueprint.route('/buy', methods=['POST'])
def buy_stock():
    if 'user_id' not in session:
        print('here')
        return jsonify({'message': 'Please log in'}), 401

    data = request.get_json()
    ticker = data['ticker']
    shares = int(data.get('shares', 1))
    price = float(data['price'])

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

@api_blueprint.route('/sell', methods=['POST'])
def sell_stock():
    if 'user_id' not in session:
        return jsonify({'message': 'Please log in'}), 401

    data = request.get_json()
    ticker = data['ticker']
    shares_to_sell = int(data.get('shares', 1))
    price = float(data['price'])

    transactions = Transaction.query.filter_by(user_id=session['user_id'], stock_ticker=ticker).all()
    total_shares_bought = sum(t.shares for t in transactions if t.transaction_type == 'buy')
    total_shares_sold = sum(t.shares for t in transactions if t.transaction_type == 'sell')

    net_shares = total_shares_bought - abs(total_shares_sold)

    if net_shares < shares_to_sell:
        return jsonify({'message': 'Not enough shares to sell'}), 400

    transaction = Transaction(
        user_id=session['user_id'],
        stock_ticker=ticker,
        shares=-shares_to_sell,
        price_per_share=price,
        transaction_type='sell'
    )
    db.session.add(transaction)
    db.session.commit()
    return jsonify({'message': 'Stock sold successfully'}), 200
