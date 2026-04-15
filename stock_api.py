import yfinance as yf

def get_stock_data(symbol):
    try:
        symbol = symbol.strip().upper()

        # Auto add .NS
        if "." not in symbol:
            symbol = symbol + ".NS"

        stock = yf.Ticker(symbol)

        # 🔹 Try fetching data
        data = stock.history(period="6mo")

        # 🔹 Fallback if empty
        if data.empty:
            return None, None

        # 🔹 Safe company name
        try:
            company = stock.info.get("longName", symbol)
        except:
            company = symbol

        return data, company

    except Exception as e:
        print("Stock API Error:", e)
        return None, None