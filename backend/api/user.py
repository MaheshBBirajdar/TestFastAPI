from services.user import create_user, get_user, get_users, update_user, delete_user
from fastapi import FastAPI, Depends, HTTPException, APIRouter, status
from models.user import UserCreate, UserUpdate, UserOut, UserResponse, UserGet
from db.database import get_db
from sqlalchemy.orm import Session
import logging
from models.response import SuccessResponse
from utils.user import validate_user_input

router = APIRouter()

logger = logging.getLogger("user_api")
logger.setLevel(logging.INFO)
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


# Create User
@router.post("/user_create", response_model=SuccessResponse)
async def create_user_api(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user in the database."""
    try: 
        logger.info(f"Creating user: {user}")

        validate_user_input(user.dict(), db)
        result = create_user(db=db, user=user)

        return SuccessResponse(
            status="success",
            message="New user created successfully",
            data={
                "user": UserResponse.model_validate(result)
            }
        )
    except HTTPException as e:
        logger.error(f"Error creating user: {e.detail}")
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{e}"
            )


# Read all users
@router.get("/users_get", response_model=SuccessResponse)
async def get_users_api(db: Session = Depends(get_db)):
    logger.info(f"Fetching users: {db}")

    users = get_users(db)
    users_response = [UserResponse.model_validate(u) for u in users]

    return SuccessResponse(
        status="success",
        message="Users fetched successfully",
        data={
            "user": users_response
        }
    )


# Read single user
@router.post("/user_get_by_id", response_model=SuccessResponse)
async def get_user_by_id_api(user_req: UserGet, db: Session = Depends(get_db)):
    logger.info(f"Fetching user with ID: {user_req.user_id}")

    db_user = get_user(db, user_id=user_req.user_id)
    if not db_user:
        logger.warning(f"User not found: {user_req.user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    
    return SuccessResponse(
        status="success",
        message="User fetched successfully",
        data={
            "user": UserResponse.model_validate(db_user)
        }
    )


# Update user
@router.put("/user_update", response_model=SuccessResponse)
async def update_user_api(user_req: UserUpdate, db: Session = Depends(get_db)):
    logger.info(f"Updating user ID: {user_req.user_id} with data: {user_req}")

    db_user = update_user(db, user_req)
    if not db_user:
        logger.warning(f"User not found for update: {user_req.user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    
    return SuccessResponse(
        status="success",
        message="User updated successfully",
        data={
            "user": UserResponse.model_validate(db_user)
        }
    )


# Delete user
@router.delete("/user_delete", response_model=SuccessResponse)
async def delete_user_api(user_req: UserOut, db: Session = Depends(get_db)):
    logger.info(f"Deleting user with ID: {user_req.user_id}")

    db_user = delete_user(db, user_req.user_id)
    if not db_user:
        logger.warning(f"User not found for delete: {user_req.user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    
    return SuccessResponse(
        status="success",
        message="User deleted successfully",
        data={
            "user": UserResponse.model_validate(db_user)
        }
    )