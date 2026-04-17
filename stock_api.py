import yfinance as yf


def get_stock_data(symbol):
    try:
        symbol = symbol.strip().upper()

        # 🔹 Ensure NSE format
        if "." not in symbol:
            symbol = symbol + ".NS"

        stock = yf.Ticker(symbol)

        # 🔹 Try multiple periods (fallback strategy)
        data = stock.history(period="6mo")

        if data.empty:
            data = stock.history(period="3mo")

        if data.empty:
            data = stock.history(period="1mo")

        if data.empty:
            return None, None

        # 🔹 Safer company name (avoid stock.info issues)
        company = symbol

        try:
            info = stock.fast_info  # faster & more reliable
            if hasattr(stock, "info"):
                company = stock.info.get("longName", symbol)
        except:
            # fallback: clean symbol
            company = symbol.replace(".NS", "")

        return data, company

    except Exception as e:
        print("Stock API Error:", e)
        return None, None