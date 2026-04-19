# 📈 Financial AI Stock Analyzer

An AI-powered stock analysis dashboard that provides real-time stock data, news sentiment analysis, and downloadable reports — built using **Streamlit, Python, and OpenAI**.

---

## 🚀 Live App

👉 https://financial-ai-stock-analyzer-clean-ic8na3egzz3y2sdrpsqgrn.streamlit.app/

---

## 🧠 Features

* 🔍 **Smart Stock Search**

  * Search from a list of NSE stocks (expandable to NIFTY 500)

* 📊 **Interactive Stock Chart**

  * Plotly-based dynamic charts with hover insights

* 📰 **Latest News Integration**

  * Fetches real-time news using GNews & NewsAPI
  * Built-in fallback system for reliability

* 🤖 **AI Sentiment Analysis**

  * Uses OpenAI to analyze news sentiment
  * Provides **BUY / SELL / HOLD** suggestions

* 📄 **Downloadable PDF Report**

  * Includes:

    * Stock chart
    * News headlines
    * AI analysis

* 🔄 **Retry & Error Handling**

  * Handles API failures gracefully with retry logic

* 🧩 **Modular Architecture**

  * Clean separation of APIs, AI logic, charting, and UI

---

## 🛠️ Tech Stack

* **Frontend/UI**: Streamlit
* **Data**: yFinance
* **News APIs**: GNews, NewsAPI
* **AI**: OpenAI API
* **Charts**: Plotly
* **PDF Generation**: FPDF
* **Language**: Python

---

## 📁 Project Structure

```
financial-ai-stock-analyzer/
│
├── main.py              # Streamlit app (UI + logic)
├── stock_api.py         # Stock data fetching (yfinance)
├── news_api.py          # News fetching with fallback
├── ai_analysis.py       # AI sentiment analysis
├── chart.py             # Plotly chart generation
├── report.py            # PDF report creation
├── stocks.py / csv      # Stock list (NIFTY 100/500)
├── utils.py             # Retry logic
├── config.py            # API keys (env-based)
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/abhijitmaurya759/financial-ai-stock-analyzer-clean.git
cd financial-ai-stock-analyzer-clean
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add API Keys

Create a `.env` file:

```
OPENAI_API_KEY=your_openai_key
GNEWS_API_KEY=your_gnews_key
NEWS_API_KEY=your_newsapi_key
```

---

### 5. Run the app

```bash
streamlit run main.py
```

---

## ☁️ Deployment

Deployed on **Streamlit Cloud**:

* Connect GitHub repo
* Add environment variables
* Deploy in one click

---

## ⚠️ Limitations

* News APIs may sometimes return limited results
* Stock data depends on Yahoo Finance availability
* Shareholding data currently simulated (can be integrated with real APIs)

---

## 🔮 Future Enhancements

* 📊 Candlestick charts
* 📉 RSI & Moving Averages
* 🥧 Real shareholding pattern integration
* 🌙 Dark/Light mode toggle
* 📈 Portfolio tracking

---

## 🤝 Contributing

Feel free to fork this repo and improve features!

---

## 📌 Author

**Abhijit Maurya**
GitHub: https://github.com/abhijitmaurya759

---

## ⭐ If you like this project

Give it a ⭐ on GitHub — it helps a lot!
