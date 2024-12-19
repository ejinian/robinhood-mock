import React, { useState, useEffect } from 'react';
import axios from 'axios';
import SearchStock from './SearchStock';

function Home() {
    const [portfolio, setPortfolio] = useState([]);

    useEffect(() => {
        const fetchPortfolio = async () => {
            try {
                const response = await axios.get('http://localhost:5000/portfolio', {
                    withCredentials: true
                });
                setPortfolio(response.data);
            } catch (error) {
                console.error('Error fetching portfolio:', error);
            }
        };

        fetchPortfolio();
    }, []);

    return (
        <div>
            <SearchStock></SearchStock>
            <h2>My Portfolio</h2>
            <table>
                <thead>
                    <tr>
                        <th>Ticker</th>
                        <th>Shares</th>
                        <th>Price per Share</th>
                        <th>Transaction Type</th>
                        <th>Timestamp</th>
                        <th>Cost of Purchase</th>
                    </tr>
                </thead>
                <tbody>
                    {portfolio.map((item, index) => (
                        <tr key={index}>
                            <td>{item.ticker}</td>
                            <td>{item.shares}</td>
                            <td>${item.price_per_share.toFixed(2)}</td>
                            <td>{item.transaction_type}</td>
                            <td>{item.timestamp}</td>
                            <td>{item.cost_of_purchase}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default Home;
