import streamlit as st
from datetime import datetime
from stock_api import get_stock_data
from news_api import get_news
from ai_analysis import analyze_news
from chart import plot_chart
from report import create_report
from stocks import STOCKS
from utils import retry

st.set_page_config(page_title="Financial AI Stock Analyzer", layout="wide")

st.title("📈 Financial AI Stock Analyzer")

# 🔹 Market Status
now = datetime.now()
if 9 <= now.hour < 16:
    st.success("🟢 Market is Open")
else:
    st.info("🔴 Market is Closed (Data may be delayed)")

# 🔍 Stock Search
st.subheader("🔍 Search Stock")

search = st.text_input("Type company name (e.g. Tata, Reliance)")

selected_symbol = None
selected_company = None

if search:
    filtered_stocks = {
        k: v for k, v in STOCKS.items()
        if search.lower() in k.lower()
    }

    if filtered_stocks:
        selected_company = st.selectbox("Select Company", list(filtered_stocks.keys()))
        selected_symbol = filtered_stocks[selected_company]
    else:
        st.warning("No matching stocks found")

# 🔄 Retry button
if st.button("🔄 Retry"):
    st.rerun()

# 🚀 Analyze Button
if st.button("Analyze"):

    if not selected_symbol:
        st.warning("Please search and select a stock")
    else:
        # ✅ Safe symbol formatting
        symbol = selected_symbol if ".NS" in selected_symbol else selected_symbol + ".NS"

        st.write(f"🔍 Analyzing: **{selected_company} ({symbol})**")

        # 📊 Fetch stock data (with retry)
        with st.spinner("Fetching stock data..."):
            result = retry(lambda: get_stock_data(symbol))

        if result:
            stock_data, company = result
        else:
            stock_data, company = None, None

        if stock_data is None:
            st.error("⚠️ Unable to fetch stock data. Please try again.")
        else:
            st.success(f"🏢 Company: {company}")

            # 📰 Fetch news (clean + retry)
            with st.spinner("Fetching latest news..."):
                news = retry(lambda: get_news(company))

            if not news:
                news = ["No major news found. Market may be stable."]

            # 🤖 AI Analysis
            analysis = None
            with st.spinner("Running AI analysis..."):
                try:
                    analysis = analyze_news(news)
                except Exception as e:
                    st.error(f"AI Error: {e}")

            # 🔹 Layout
            col1, col2 = st.columns(2)

            # 📊 Chart
            with col1:
                st.subheader("📊 Stock Price Chart")
                try:
                    if stock_data is not None and not stock_data.empty:
                        fig = plot_chart(stock_data, symbol)

                        if fig:
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.warning("⚠️ Chart could not be generated")
                    else:
                        st.warning("Chart data not available")
                except Exception as e:
                    st.error(f"Chart Error: {e}")

            # 🤖 AI Analysis
            with col2:
                st.subheader("🤖 AI Sentiment Analysis")
                if analysis:
                    st.write(analysis)

                    if "positive" in analysis.lower():
                        st.success("📈 Suggestion: BUY")
                    elif "negative" in analysis.lower():
                        st.error("📉 Suggestion: SELL")
                    else:
                        st.warning("⚖️ Suggestion: HOLD")
                else:
                    st.warning("AI analysis not available")

            # 📰 News
            st.subheader("📰 News Headlines")
            for n in news:
                st.write(f"- {n}")

            # 📄 Report
            if analysis:
                try:
                    report_file = create_report(selected_symbol, stock_data, analysis, news)

                    st.success("📄 Report generated successfully")

                    with open(report_file, "rb") as file:
                        st.download_button(
                            label="📥 Download Report",
                            data=file,
                            file_name=report_file,
                            mime="application/pdf"
                        )

                except Exception as e:
                    st.error(f"Report Error: {e}")
            else:
                st.warning("Skipping report generation due to missing analysis")