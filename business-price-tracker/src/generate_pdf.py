from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pandas as pd
from pathlib import Path
from datetime import datetime
from utils import log_info, log_error

def generate_pdf_report(df, output_path):
    try:
        c = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, "Business Insights Daily Report")

        c.setFont("Helvetica", 12)
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        c.drawString(50, height - 70, f"Report generated on: {date_str}")

        # Table headers
        y = height - 100
        for col in df.columns:
            c.drawString(50, y, str(col).title())
            y -= 15

        # Data rows (limit to first 10 rows for readability)
        for idx, row in df.head(10).iterrows():
            y -= 5
            row_str = ", ".join(str(v) for v in row.values)
            c.drawString(50, y, row_str)
            y -= 15

        c.save()
        log_info(f"PDF report saved: {output_path}")
    except Exception as e:
        log_error(f"Error generating PDF: {e}")


if __name__ == "__main__":
    cleaned_csv = Path("data/cleaned/cleaned_data.csv")
    df = pd.read_csv(cleaned_csv)
    log_info(f"Loaded {len(df)} rows from cleaned data")
    generate_pdf_report(df, "reports/daily_report.pdf")
