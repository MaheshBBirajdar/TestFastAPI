from fastapi import HTTPException, status
from db.model import User

def validate_user_input(user: dict, db):
    # Check required fields
    required_fields = ["username", "email", "role"]
    for field in required_fields:
        if not user.get(field) or str(user.get(field)).strip() == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{field} cannot be empty"
            )

    # Check email format
    email = user.get("email")
    if "@" not in email or not email.endswith(".com"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email must contain '@' and end with '.com'"
        )

    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.username == user.get("username")) | (User.email == email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username or email already exists"
        )
