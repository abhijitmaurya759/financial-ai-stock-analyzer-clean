import matplotlib.pyplot as plt

def plot_chart(df, symbol):

    plt.figure()

    plt.plot(df["Close"])

    plt.title(symbol + " Stock Price (6 Months)")
    plt.xlabel("Date")
    plt.ylabel("Price")

    plt.savefig("stock_chart.png")

    plt.show()