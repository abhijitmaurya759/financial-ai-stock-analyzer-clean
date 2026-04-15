from fpdf import FPDF
import matplotlib.pyplot as plt

def create_report(symbol, data, analysis, news):

    # Create chart image
    plt.figure()
    plt.plot(data["Close"])
    plt.title(symbol + " Stock Price (6 Months)")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.savefig("chart.png")
    plt.close()

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=16)
    pdf.cell(200,10,"Financial Analysis Report",ln=True,align="C")

    pdf.set_font("Arial", size=12)
    pdf.cell(200,10,"Stock: " + symbol,ln=True)

    pdf.cell(200,10,"Stock Chart:",ln=True)
    pdf.image("chart.png", x=10, w=180)

    pdf.ln(10)

    pdf.cell(200,10,"Latest News:",ln=True)
    for n in news:
        pdf.multi_cell(0,8,"- " + n)

    pdf.ln(5)

    analysis = analysis.encode("latin-1","replace").decode("latin-1")

    pdf.cell(200,10,"AI Analysis:",ln=True)
    pdf.multi_cell(0,8,analysis)

    filename = f"{symbol}_report.pdf"
    pdf.output(filename)

    return filename