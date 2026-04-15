import streamlit as st
from stock_api import get_stock_data
from news_api import get_news
from ai_analysis import analyze_news
from chart import plot_chart
from report import create_report

st.title("📈 Financial AI Stock Analyzer")

symbol = st.text_input("Enter stock symbol (e.g. RELIANCE.NS)")

if st.button("Analyze"):

    if not symbol:
        st.warning("Please enter a stock symbol")
    else:
        st.write("Fetching stock data...")
        stock_data, company = get_stock_data(symbol)

        if stock_data is None:
            st.error("Invalid stock symbol")
        else:
            st.success(f"Company: {company}")

            st.write("Fetching news...")
            news = get_news(company)

            st.subheader("📰 News Headlines")
            for n in news:
                st.write(f"- {n}")

            st.write("Running AI analysis...")
            analysis = analyze_news(news)

            st.subheader("🤖 AI Analysis")
            st.write(analysis)

            st.subheader("📊 Stock Chart")
            plot_chart(stock_data, symbol)

            create_report(symbol, analysis, news)

            st.success("Report generated successfully")