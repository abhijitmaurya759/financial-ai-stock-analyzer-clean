import plotly.graph_objects as go

def plot_chart(data, symbol):
    try:
        # 🔹 Safety checks
        if data is None or data.empty:
            return None

        if "Close" not in data.columns:
            return None

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=data.index,
            y=data["Close"],
            mode='lines',
            name='Close Price'
        ))

        fig.update_layout(
            title=f"{symbol} Stock Price",
            xaxis_title="Date",
            yaxis_title="Price (₹)",
            hovermode="x unified",
            template="plotly_dark"
        )

        return fig  # ✅ always return figure

    except Exception as e:
        print("Chart Error:", e)
        return None  # ✅ fail safely