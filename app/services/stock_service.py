import yfinance as yf

def get_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1d")
        print(hist)
        if not hist.empty:
            last_close = hist['Close'].iloc[-1]
        else:
            last_close = None
        return {
            "ticker": ticker,
            "name": stock.info.get('longName'),
            "price": last_close,
            "currency": stock.info.get('currency')
        }
    except Exception as e:
        print(e)
        return None
