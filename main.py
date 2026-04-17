import streamlit as st
from datetime import datetime
from stock_api import get_stock_data
from news_api import get_news
from ai_analysis import analyze_news
from chart import plot_chart
from report import create_report
from stocks import STOCKS
from utils import retry

st.set_page_config(page_title="Stock Analyzer Pro", layout="wide")

# 🔹 Header
st.markdown("""
<h1 style='text-align: center;'>📈 Stock Analyzer Pro</h1>
<p style='text-align: center; color: grey;'>AI-powered stock insights dashboard</p>
""", unsafe_allow_html=True)

# 🔹 Market Status
now = datetime.now()
col_status1, col_status2 = st.columns([3,1])

with col_status1:
    st.markdown("### 🔍 Search Stock")

with col_status2:
    if 9 <= now.hour < 16:
        st.success("🟢 Market Open")
    else:
        st.warning("🔴 Market Closed")

# 🔍 Search
search = st.text_input("Search company (e.g. Tata, Reliance)")

selected_symbol = None
selected_company = None

if search:
    filtered = {k: v for k, v in STOCKS.items() if search.lower() in k.lower()}

    if filtered:
        selected_company = st.selectbox("Select Company", list(filtered.keys()))
        selected_symbol = filtered[selected_company]
    else:
        st.warning("No matching stocks found")

# 🔘 Buttons
col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    analyze_clicked = st.button("🚀 Analyze", use_container_width=True)

with col_btn2:
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()

# 🚀 Main Logic
if analyze_clicked:

    if not selected_symbol:
        st.warning("Please select a stock")
    else:
        symbol = selected_symbol if ".NS" in selected_symbol else selected_symbol + ".NS"

        st.markdown(f"## 📊 {selected_company} ({symbol})")

        # 📊 Fetch data
        with st.spinner("Fetching stock data..."):
            result = retry(lambda: get_stock_data(symbol))

        if result:
            stock_data, company = result
        else:
            stock_data, company = None, None

        if stock_data is None:
            st.error("Failed to fetch stock data")
        else:
            # 🔹 Metrics (NEW - dashboard feel)
            last_price = stock_data["Close"].iloc[-1]
            prev_price = stock_data["Close"].iloc[-2]
            change = last_price - prev_price
            percent = (change / prev_price) * 100

            col1, col2, col3 = st.columns(3)

            col1.metric("💰 Price", f"₹{last_price:.2f}")
            col2.metric("📈 Change", f"{change:.2f}", f"{percent:.2f}%")
            col3.metric("📊 Data Points", len(stock_data))

            # 📰 News
            with st.spinner("Fetching news..."):
                news = retry(lambda: get_news(company))

            if not news:
                news = ["No major news available"]

            # 🤖 AI
            with st.spinner("Analyzing sentiment..."):
                try:
                    analysis = analyze_news(news)
                except:
                    analysis = "AI analysis unavailable"

            # 🔹 Layout
            col_chart, col_ai = st.columns([2,1])

            # 📊 Chart
            with col_chart:
                st.subheader("📊 Price Chart")
                fig = plot_chart(stock_data, symbol)

                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Chart not available")

            # 🤖 AI Panel
            with col_ai:
                st.subheader("🤖 AI Insight")

                if analysis:
                    st.write(analysis)

                    if "positive" in analysis.lower():
                        st.success("📈 BUY")
                    elif "negative" in analysis.lower():
                        st.error("📉 SELL")
                    else:
                        st.warning("⚖️ HOLD")

            # 📰 News Section
            st.subheader("📰 Latest News")

            for n in news:
                st.markdown(f"- {n}")

            # 📄 Report
            if analysis:
                report_file = create_report(selected_symbol, stock_data, analysis, news)

                with open(report_file, "rb") as f:
                    st.download_button(
                        "📥 Download Report",
                        f,
                        file_name=report_file,
                        mime="application/pdf"
                    )