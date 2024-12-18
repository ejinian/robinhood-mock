import yfinance as yf

def get_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        return {
            "ticker": ticker,
            "name": stock.info.get('longName'),
            "price": stock.info.get('regularMarketPrice'),
            "currency": stock.info.get('currency')
        }
    except Exception as e:
        return None
