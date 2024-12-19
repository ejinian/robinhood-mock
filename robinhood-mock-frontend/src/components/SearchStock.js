import React, { useState } from 'react';
import axios from 'axios';

function SearchStock() {
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
        } catch (err) {
            setError('Purchase failed');
        }
    };

    return (
        <div>
            <input
                type="text"
                value={ticker}
                onChange={(e) => setTicker(e.target.value.toUpperCase())}
                placeholder="Enter a stock ticker (e.g., AAPL)"
            />
            <button onClick={handleSearch}>Search</button>
            {error && <div className="error">{error}</div>}
            {stockData && (
                <div className="stock-data">
                    <h2>{stockData.name} ({stockData.ticker})</h2>
                    {stockData.price ? (
                        <>
                            <p>Current Price: {stockData.price} {stockData.currency}</p>
                            <input
                                type="number"
                                value={quantity}
                                onChange={(e) => setQuantity(Math.max(1, parseInt(e.target.value, 10)))}
                                min="1"
                            />
                            <button onClick={handleBuy}>Buy</button>
                        </>
                    ) : (
                        <p>Stock price unavailable</p>
                    )}
                </div>
            )}
        </div>
    );
}

export default SearchStock;
