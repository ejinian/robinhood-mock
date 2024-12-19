import React, { useState } from 'react';
import axios from 'axios';

function SearchStock() {
    const [ticker, setTicker] = useState('');
    const [stockData, setStockData] = useState(null);
    const [error, setError] = useState('');

    const handleSearch = async () => {
        try {
            const response = await axios.get(`http://localhost:5000/search/${ticker}`);
            setStockData(response.data);
            setError('');
        } catch (err) {
            if (err.response && err.response.status === 404) {
                setError('Stock not found');
                setStockData(null);
            } else {
                setError('An error occurred');
                setStockData(null);
            }
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
                    <p> Current Price: {stockData.price} {stockData.currency}</p>
                    ) : (
                    <p>Stock price unavailable</p>
                    )}
                </div>
            )}
        </div>
    );
}

export default SearchStock;
