import os
import datetime
from fpdf import FPDF

class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "📘 Stock Technical & Fundamental Snapshot", ln=True, align="C")
        self.ln(10)

    def section_title(self, title):
        self.set_font("Arial", "B", 10)
        self.set_text_color(30, 30, 30)
        self.cell(0, 8, title, ln=True)

    def section_body(self, body):
        self.set_font("Arial", "", 9)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 6, body)
        self.ln()

def generate_pdf_report(symbol, report_data):
    try:
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        pdf = PDFReport()
        pdf.add_page()

        # Title
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, f"📘 {symbol.upper()} – TECHNICAL & FUNDAMENTAL SNAPSHOT", ln=True)
        pdf.cell(0, 10, f"🗓️ {today}", ln=True)
        pdf.ln(5)

        # Add sections from report_data
        section_map = {
            "price": "Price",
            "support_zone": "Support Zone",
            "resistance_zone": "Resistance Zone",
            "trend": "Trend",
            "rsi": "RSI",
            "ema_21": "EMA 21",
            "ema_50": "EMA 50",
            "ema_200": "EMA 200",
            "volume": "Volume",
            "volume_avg": "Volume Avg",
            "volume_signal": "Volume Signal",
            "breakout_signal": "Breakout Signal",
            "candlestick": "Candlestick Pattern",
            "structure_daily": "Structure – Daily",
            "structure_weekly": "Structure – Weekly"
        }

        for key, title in section_map.items():
            if key in report_data:
                value = report_data[key]
                pdf.section_title(f"📌 {title}")
                pdf.section_body(str(value))

        # Disclaimer
        pdf.set_text_color(150, 0, 0)
        pdf.set_font("Arial", "I", 8)
        pdf.multi_cell(0, 6, "\n⚠️ Disclaimer: This is an auto-generated report for informational purposes only. Please consult your financial advisor before making any investment decisions.")

        # Save file
        filename = f"{symbol.upper()}_{today}.pdf"
        output_path = os.path.join("reports", filename)
        os.makedirs("reports", exist_ok=True)
        pdf.output(output_path.encode('latin-1'))  # Avoid unicode errors in filename
        return output_path

    except Exception as e:
        print("❌ PDF GENERATION FAILED:")
        print(e)
        return None
