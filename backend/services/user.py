from sqlalchemy.orm import Session
from db.model import User
from models.user import UserCreate, UserUpdate, UserOut
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_user(db, user_id):
    return db.query(User).filter(User.id == user_id).first()


def get_users(db):
    return db.query(User).all()


def create_user(db, user):
    # Hash the password before saving
    hashed_password = get_password_hash(user.password)

    db_user = User(
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role,
        is_active=user.is_active,
        password_hash=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db, user_req):
    db_user = get_user(db, user_req.user_id)
    if not db_user:
        return None
    
    for key, value in user_req.dict(exclude_unset=True).items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db, user_id):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    db.delete(db_user)
    db.commit()
    return db_user
