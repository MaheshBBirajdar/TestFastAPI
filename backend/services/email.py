import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import SMTP_SERVER, SMTP_PORT , GMAIL_USER, GMAIL_APP_PASSWORD
import re

def format_name_from_email(email: str) -> str:
    """Extract name from email before @, remove digits, keep only alphabetic words."""
    name_part = email.split("@")[0]

    # Replace dots/underscores with spaces
    name_part = name_part.replace(".", " ").replace("_", " ")
    
    # Remove digits from each part and keep only alphabetical characters
    words = []
    for part in name_part.split():
        cleaned = re.sub(r'[^a-zA-Z]', '', part)  # remove non-alphabet chars
        if cleaned:  # only keep non-empty words
            words.append(cleaned.capitalize())
    return " ".join(words)


def format_email_body(recipient_email: str, body_text: str) -> str:
    """Format the email with greeting and regards automatically."""
    recipient_name = format_name_from_email(recipient_email).upper()
    
    return f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f9f9f9;
                padding: 20px;
                color: #333;
            }}
            .container {{
                max-width: 600px;
                margin: left;
                background: #ffffff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .header {{
                border-bottom: 2px solid #eee;
                padding-bottom: 10px;
                margin-bottom: 20px;
            }}
            .footer {{
                font-size: 12px;
                color: #777;
                margin-top: 20px;
                border-top: 1px solid #eee;
                padding-top: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div>
                <p>Dear {recipient_name},</p>
                <p>{body_text}</p>
                <p>Regards,<br>{recipient_name.capitalize()}</p>
            </div>
            <div class="footer">
                <p>This is for testing purposes. Please do not reply directly to this email.</p>
                <p>If you have any queries, contact our support team at 
                <a href="mailto:maheshbirajdar37346@gmail.com">maheshbirajdar37346@gmail.com</a></p>
            </div>
        </div>
    </body>
    </html>
    """


def send_mail(recipient: str, subject: str, body: str):
    try:
        body = format_email_body(recipient, body)

        msg = MIMEMultipart()
        msg["From"] = GMAIL_USER
        msg["To"] = recipient
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "html"))

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_USER, recipient, msg.as_string())
    except Exception as e:
        raise RuntimeError(f"Failed to send email: {str(e)}")
