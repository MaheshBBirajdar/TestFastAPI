import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import SMTP_SERVER, SMTP_PORT , GMAIL_USER, GMAIL_APP_PASSWORD
import re
from db.model import User, Email
from datetime import datetime
from utils.email import sender_info
from models.email import EmailRequest, EmailUpdate, EmailDelete


def format_email_body(sender_name, body_text: str) -> str:
    """Format the email with greeting and regards automatically."""
    
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
                <p>Dear Recipient,</p>
                <p>{body_text}</p>
                <p>Regards,<br>{sender_name}</p>
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


def send_mail(user_id, recipient_email: str, subject: str, body: str, db):
    try:
        # Validate sender & recipient email
        sender_name = sender_info(db, user_id, recipient_email)

        # Format the email body
        body_format = format_email_body(sender_name, body)

        msg = MIMEMultipart()
        msg["From"] = GMAIL_USER
        msg["To"] = recipient_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body_format, "html"))

        # Send the email using SMTP
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_USER, recipient_email, msg.as_string())

        # Log the email in the database
        email_record = Email(
            user_id=user_id,
            sender=sender_name,
            recipient=recipient_email,
            subject=subject,
            body=body,
            status="SENT",
            sent_at=datetime.utcnow()
        )
        db.add(email_record)
        db.commit()

        return email_record

    except Exception as e:
        raise RuntimeError(f"Failed to send email: {str(e)}")


def retrive_emails(db):
    """
    Retrieve all emails sent by a user.
    """
    try:
        emails = db.query(Email).all()
        return emails
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve emails: {str(e)}")


async def update_email(email_req: EmailUpdate, db):
    """
    Update an email's details by ID.
    """
    email = db.query(Email).filter(Email.id == email_req.email_id).first()
    if not email:
        return None
    
    email.subject = email_req.subject
    email.body = email_req.body
    email.status = email_req.status
    email.sent_at = datetime.utcnow()

    db.commit()
    db.refresh(email)
    return email


async def delete_email(email_id, db):
    """
    Delete an email by ID.
    """
    email = db.query(Email).filter(Email.id == email_id).first()
    if not email:
        return None
    
    db.delete(email)
    db.commit()
    return email

