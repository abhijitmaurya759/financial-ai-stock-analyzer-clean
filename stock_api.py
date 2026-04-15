import yfinance as yf

def get_stock_data(symbol):
    try:
        # 🔹 Auto-add .NS if not present
        symbol = symbol.strip().upper()
        if "." not in symbol:
            symbol = symbol + ".NS"

        stock = yf.Ticker(symbol)
        data = stock.history(period="6mo")

        if data.empty:
            return None, None

        company = stock.info.get("longName", symbol)

        return data, company

    except Exception as e:
        print("Error:", e)
        return None, None