from .utils import log_info
from .scrape_web import scrape_books, scrape_with_retry, BASE_URL
from .clean_book_data import remove_duplicate_books
import pandas as pd
from pathlib import Path
from .update_sheet import connect_to_sheets, update_sheet
from .generate_pdf import generate_pdf_report
from datetime import datetime
from .send_email import send_email

def main():
    log_info("Starting Business Price Tracker automation...")
    log_info("Step 1: Scraping data from the web...")
    books = scrape_with_retry(retries=3, delay=5, start=1, finish=5)
    if books:
        log_info(f"Scraped {len(books)} books successfully.")
    else:
        log_info("No data scraped. Exiting.")
        return
    log_info("Step 2: Data cleaning...")
    cleaned_books = remove_duplicate_books(books)
    log_info(f"Cleaned data. {len(cleaned_books)} unique books remain after removing duplicates.")
    log_info("Step 3: Saving as DataFrame...")
    df = pd.DataFrame([book.__dict__ for book in cleaned_books])
    log_info("Step 4: Update Google Sheets API...")
    creds_file = "private/credentials.json"
    sheet_name = "Business Tracker Sheet"
    sheet = connect_to_sheets(creds_file, sheet_name)
    if sheet:
        update_sheet(sheet, df)
        log_info("Google Sheet updated successfully.")
    else:
        log_info("Failed to connect to Google Sheets. Exiting.")
        return
    log_info("Step 5: Generate PDF summary report...")
    report_path = f"reports/summary_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    generate_pdf_report(df, str(report_path))
    log_info(f"PDF report generated at {report_path}.")
    log_info("Step 6: Send email report...")
    receiver_email = "resuviketer4@gmail.com"
    subject = "Business Price Tracker - Daily Report"
    body = "Please find attached the daily report for the Business Price Tracker."
    send_email(receiver_email, subject, body, report_path)
    log_info("Finished Automation Series.")
    
if __name__ == "__main__":
    main()
