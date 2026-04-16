import streamlit as st
from datetime import datetime
from stock_api import get_stock_data
from news_api import get_news
from ai_analysis import analyze_news
from chart import plot_chart
from report import create_report

st.set_page_config(page_title="Financial AI Stock Analyzer", layout="wide")

st.title("📈 Financial AI Stock Analyzer")

# 🔹 Market Status
now = datetime.now()
if 9 <= now.hour < 16:
    st.success("🟢 Market is Open")
else:
    st.info("🔴 Market is Closed (Data may be delayed)")

# User input
symbol_input = st.text_input("Enter stock name (e.g. RELIANCE, TCS, INFY)")

# Retry button
if st.button("🔄 Retry"):
    st.rerun()

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
            st.error("⚠️ Unable to fetch stock data right now. Please try again later.")
        else:
            st.success(f"🏢 Company: {company}")

            # 📰 Fetch news
            with st.spinner("Fetching latest news..."):
                news = get_news(company)

            # 🤖 AI Analysis
            analysis = None
            with st.spinner("Running AI analysis..."):
                try:
                    if news:
                        analysis = analyze_news(news)
                except Exception as e:
                    st.error(f"AI Error: {e}")

            # 🔹 Layout (Chart + Analysis side by side)
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📊 Stock Price Chart")
                try:
                    plot_chart(stock_data, symbol)
                except Exception as e:
                    st.error(f"Chart Error: {e}")

            with col2:
                st.subheader("🤖 AI Sentiment Analysis")
                if analysis:
                    st.write(analysis)

                    # 🔥 Buy/Sell Signal
                    if "positive" in analysis.lower():
                        st.success("📈 Suggestion: BUY")
                    elif "negative" in analysis.lower():
                        st.error("📉 Suggestion: SELL")
                    else:
                        st.warning("⚖️ Suggestion: HOLD")
                else:
                    st.warning("AI analysis not available")

            # 📰 News Section
            st.subheader("📰 News Headlines")
            if news:
                for n in news:
                    st.write(f"- {n}")
            else:
                st.warning("No news found.")

            # 📄 Report
            if analysis and news:
                try:
                    create_report(symbol_input, stock_data, analysis, news)
                    st.success("📄 Report generated successfully")
                except Exception as e:
                    st.error(f"Report Error: {e}")
            else:
                st.warning("Skipping report generation due to missing data")