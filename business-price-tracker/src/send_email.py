import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from utils import EMAIL_USER, EMAIL_PASS, log_info, log_error
from pathlib import Path

def send_email(to_email, subject, body, attachment_path):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = to_email
        msg['Subject'] = subject

        # Add body
        from email.mime.text import MIMEText
        msg.attach(MIMEText(body, 'plain'))

        # Add attachment
        with open(attachment_path, "rb") as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            f'attachment; filename="{Path(attachment_path).name}"')
            msg.attach(part)

        # Connect & send
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()

        log_info(f"Email sent successfully to {to_email}")

    except Exception as e:
        log_error(f"Failed to send email: {e}")

if __name__ == "__main__":
    send_email(
        to_email="recipient@example.com",
        subject="Daily Business Insights Report",
        body="Hi, please find the daily report attached.",
        attachment_path="reports/daily_report.pdf"
    )

