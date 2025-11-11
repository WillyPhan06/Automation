import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
DATA_SOURCE_URL = os.getenv("DATA_SOURCE_URL")

# Logging setup
logging.basicConfig(
    filename="logs/automation.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_info(message):
    logging.info(message)
    print(f"[INFO] {message}")

def log_error(message):
    logging.error(message)
    print(f"[ERROR] {message}")
