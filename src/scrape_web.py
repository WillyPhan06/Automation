import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
from .utils import log_info, log_error
import time
from models.book import Book

BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"

def scrape_books(start: int = 1, finish: int = 5):
    all_books = []
    for page in range(start, finish+1):
        try:
            url = BASE_URL.format(page)
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            for book in soup.select("article.product_pod"):
                title = book.h3.a['title']
                raw_price = book.select_one(".price_color").text.strip()
                price = raw_price.translate(str.maketrans("", "", "£$€Â"))

                rating = book.p['class'][1]  # e.g., 'Three'
                all_books.append(Book(title=title, price=float(price), rating=rating))

            log_info(f"Scraped page {page} successfully")
            return all_books
        except Exception as e:
            log_error(f"Error scraping page {page}: {e}")

def scrape_with_retry(retries=3, delay=5, start=1, finish=5):
    for attempt in range(1, retries + 1):
        log_info(f"Starting scrape attempt: {attempt}")
        books = scrape_books(start, finish)
        if books:
            log_info(f"Succeeded scrape attempt: {attempt}")
            return books
        log_error(f"Failed scrape attempt: {attempt}")
        sleep_time = max(delay * attempt, 1)
        time.sleep(sleep_time)

    log_error(f"Failed all {retries} scrape attempts")
    return None

if __name__ == "__main__":
    print(Book(title="Sample Book", price=19.99, rating="Five"))


