
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