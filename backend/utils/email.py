from db.model import User, Email

def validate_email(email: str) -> str:
    """
    Validate that the email ends with '.com'.
    Raise ValueError if it doesn't.
    """
    if not email:
        raise ValueError("Email cannot be empty")
    
    if "@" not in email or ".com" not in email.lower():
        raise ValueError("Email must contain '@' & '.com' (e.g. user@example.com)")
    
    return email


def sender_info(db, user_id: int, recipient_email):
    # Check if sender exists
    sender = db.query(User).filter(User.id == user_id).first()
    if not sender:
        raise ValueError(f"Sender with ID {user_id} does not exist")

    # Check if recipient exists
    recipient = db.query(User).filter(User.email == recipient_email).first()
    if not recipient:
        raise ValueError(f"Recipient with email {recipient_email} does not exist")

    sender_name = f"{sender.first_name.capitalize()} {sender.last_name.capitalize()}"

    return sender_name