import streamlit as st
from stock_api import get_stock_data
from news_api import get_news
from ai_analysis import analyze_news
from chart import plot_chart
from report import create_report

st.set_page_config(page_title="Financial AI Stock Analyzer", layout="wide")

st.title("📈 Financial AI Stock Analyzer")

# User input
symbol_input = st.text_input("Enter stock name (e.g. RELIANCE, TCS, INFY)")

if st.button("Analyze"):

    if not symbol_input:
        st.warning("Please enter a stock name")
    else:
        # 🔹 Format symbol
        symbol_input = symbol_input.strip().upper()

        if "." not in symbol_input:
            symbol = symbol_input + ".NS"
        else:
            symbol = symbol_input

        st.write(f"🔍 Analyzing: **{symbol_input}**")

        # 📊 Fetch stock data
        with st.spinner("Fetching stock data..."):
            stock_data, company = get_stock_data(symbol)

        if stock_data is None:
            st.error("❌ Invalid stock symbol")
        else:
            st.success(f"🏢 Company: {company}")

            # 📰 Fetch news
            with st.spinner("Fetching latest news..."):
                news = get_news(company)

            st.subheader("📰 News Headlines")
            if news:
                for n in news:
                    st.write(f"- {n}")
            else:
                st.warning("No news found.")

            # 🤖 AI Analysis
            analysis = None
            with st.spinner("Running AI analysis..."):
                try:
                    if news:
                        analysis = analyze_news(news)
                except Exception as e:
                    st.error(f"AI Error: {e}")

            if analysis:
                st.subheader("🤖 AI Sentiment Analysis")
                st.write(analysis)
            else:
                st.warning("AI analysis not available")

            # 📉 Chart
            st.subheader("📊 Stock Price Chart")
            try:
                plot_chart(stock_data, symbol)
            except Exception as e:
                st.error(f"Chart Error: {e}")

            # 📄 Report
            if analysis and news:
                try:
                    create_report(symbol_input, analysis, news)
                    st.success("📄 Report generated successfully")
                except Exception as e:
                    st.error(f"Report Error: {e}")
            else:
                st.warning("Skipping report generation due to missing data")