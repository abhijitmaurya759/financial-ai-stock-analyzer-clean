from fpdf import FPDF
import matplotlib.pyplot as plt
import os

# 🔹 Universal text cleaner (fixes ALL encoding issues)
def clean_text(text):
    if not isinstance(text, str):
        text = str(text)
    return text.encode("latin-1", "replace").decode("latin-1")


def create_report(symbol, data, analysis, news):

    # 🔹 Safe filenames
    symbol_clean = clean_text(symbol)
    chart_file = f"{symbol_clean}_chart.png"
    pdf_file = f"{symbol_clean}_report.pdf"

    # 🔹 Create chart
    plt.figure(figsize=(8, 4))
    plt.plot(data["Close"])
    plt.title(f"{symbol_clean} Stock Price (6 Months)")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.tight_layout()
    plt.savefig(chart_file)
    plt.close()

    # 🔹 Create PDF
    pdf = FPDF()
    pdf.add_page()

    # 🔹 Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, clean_text("Financial Analysis Report"), ln=True, align="C")

    pdf.ln(5)

    # 🔹 Stock name
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, clean_text(f"Stock: {symbol_clean}"), ln=True)

    pdf.ln(5)

    # 🔹 Chart
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, clean_text("Stock Chart:"), ln=True)
    pdf.image(chart_file, x=10, w=180)

    pdf.ln(5)

    # 🔹 News
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, clean_text("Latest News:"), ln=True)

    pdf.set_font("Arial", size=10)
    for n in news:
        pdf.multi_cell(0, 8, "- " + clean_text(n))

    pdf.ln(5)

    # 🔹 Analysis
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, clean_text("AI Analysis:"), ln=True)

    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 8, clean_text(analysis))

    # 🔹 Save PDF
    pdf.output(pdf_file)

    # 🔹 Cleanup temp chart
    if os.path.exists(chart_file):
        os.remove(chart_file)

    return pdf_file