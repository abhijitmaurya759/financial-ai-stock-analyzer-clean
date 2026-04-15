import streamlit as st
from stock_api import get_stock_data
from news_api import get_news
from ai_analysis import analyze_news
from report import create_report

# Page config
st.set_page_config(page_title="AI Stock Analyzer")

st.title("📊 AI Financial Stock Analyzer")
st.write("Analyze Indian & Global stocks with AI")
st.write("Try: Reliance, TCS, Infosys, AAPL, TSLA")

# -----------------------------
# Smart Stock Mapping
# -----------------------------
company_map = {
    "reliance": "RELIANCE.NS",
    "tcs": "TCS.NS",
    "infosys": "INFY.NS",
    "infy": "INFY.NS",
    "hdfc": "HDFCBANK.NS",
    "sbi": "SBIN.NS",
    "tata motors": "TATAMOTORS.NS"
}

# -----------------------------
# Caching for speed
# -----------------------------
@st.cache_data
def cached_stock(symbol):
    return get_stock_data(symbol)

@st.cache_data
def cached_news(company):
    return get_news(company)

# -----------------------------
# User Input
# -----------------------------
user_input = st.text_input("Enter Stock Name or Symbol")

if st.button("Analyze"):

    if not user_input:
        st.warning("Please enter a stock name or symbol")

    else:
        # -----------------------------
        # Smart Symbol Handling
        # -----------------------------
        symbol_input = user_input.lower()

        if symbol_input in company_map:
            symbol = company_map[symbol_input]
        elif "." not in user_input:
            symbol = user_input.upper() + ".NS"
        else:
            symbol = user_input.upper()

        st.info(f"Using symbol: {symbol}")

        # -----------------------------
        # Fetch Stock Data
        # -----------------------------
        with st.spinner("Fetching stock data..."):
            data, company = cached_stock(symbol)

        if data is None:
            st.error("Invalid stock symbol")
        else:
            st.success(f"Company: {company}")

            # -----------------------------
            # Show Chart
            # -----------------------------
            st.subheader("📈 Stock Chart")
            st.line_chart(data["Close"])

            # -----------------------------
            # Fetch News
            # -----------------------------
            with st.spinner("Fetching news..."):
                news = cached_news(company)

            if news:
                st.subheader("📰 Latest News")
                for n in news:
                    st.write("-", n)
            else:
                st.warning("No news found")

            # -----------------------------
            # AI Analysis
            # -----------------------------
            with st.spinner("Running AI analysis..."):
                analysis = analyze_news(news)

            st.subheader("🤖 AI Analysis")
            st.write(analysis)

            # -----------------------------
            # Generate Report
            # -----------------------------
            with st.spinner("Generating PDF report..."):
                filename = create_report(symbol, data, analysis, news)

            with open(filename, "rb") as f:
                st.download_button(
                    "📄 Download PDF Report",
                    f,
                    file_name=filename
                )