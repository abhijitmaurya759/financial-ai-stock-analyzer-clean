import matplotlib.pyplot as plt
import streamlit as st

def plot_chart(data, symbol):
    fig, ax = plt.subplots()
    ax.plot(data.index, data['Close'])
    ax.set_title(f"{symbol} Stock Price")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")

    st.pyplot(fig)   # ✅ THIS is required