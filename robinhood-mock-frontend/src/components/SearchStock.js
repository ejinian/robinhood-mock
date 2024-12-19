import React, { useState } from 'react';
import axios from 'axios';

function SearchStock({ onTransactionComplete }) {
    const [ticker, setTicker] = useState('');
    const [stockData, setStockData] = useState(null);
    const [quantity, setQuantity] = useState(1);
    const [error, setError] = useState('');

    const handleSearch = async () => {
        try {
            const response = await axios.get(`http://localhost:5000/search/${ticker}`);
            setStockData(response.data);
            setError('');
        } catch (err) {
            setError('Stock not found');
            setStockData(null);
        }
    };

    const handleBuy = async () => {
        if (!stockData) {
            setError('No stock data available for buying');
            return;
        }
        try {
            const response = await axios.post('http://localhost:5000/buy', {
                ticker: stockData.ticker,
                shares: quantity,
                price: stockData.price
            });
            alert('Purchase successful');
            setError('');
            onTransactionComplete();
        } catch (err) {
            setError(`Purchase failed. ${err['response']['data']['message']}`);
        }
    };

    const handleSell = async () => {
        try {
            const response = await axios.post('http://localhost:5000/sell', {
                ticker: stockData.ticker,
                shares: quantity,
                price: stockData.price
            });
            alert('Sale successful');
            setError('');
            onTransactionComplete();
        } catch (err) {
            setError(`Purchase failed. ${err['response']['data']['message']}`);
            console.error(err);
        }
    };

    return (
        <div className="container mt-5">
            <div className="input-group mb-3">
                <input
                    type="text"
                    className="form-control"
                    value={ticker}
                    onChange={(e) => setTicker(e.target.value.toUpperCase())}
                    placeholder="Enter a stock ticker (e.g., AAPL)"
                />
                <div className="input-group-append">
                    <button className="btn btn-outline-secondary" onClick={handleSearch}>Search</button>
                </div>
            </div>
            {error && <div className="alert alert-danger">{error}</div>}
            {stockData && (
                <div className="card text-white bg-success mb-3">
                    <div className="card-header">{stockData.name} ({stockData.ticker})</div>
                    <div className="card-body">
                        <h5 className="card-title">Current Price: {stockData.price} {stockData.currency}</h5>
                        <input
                            type="number"
                            className="form-control mb-3"
                            value={quantity}
                            onChange={(e) => setQuantity(Math.max(1, parseInt(e.target.value, 10)))}
                            min="1"
                        />
                        <button className="btn btn-light mr-2" onClick={handleBuy}>Buy</button> &nbsp; &nbsp;
                        <button className="btn btn-light" onClick={handleSell}>Sell</button>
                    </div>
                </div>
            )}
        </div>
    );
}

export default SearchStock;
