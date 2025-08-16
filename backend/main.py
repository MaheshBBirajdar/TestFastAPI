from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel
from typing import Optional
from db.database import engine, Base, get_db, create_tables
from api.git import router as git_router
from api.file import router as file_router
from api.email import router as email_router
from api.user import router as user_router

# Call this function at startup (for example, in main.py or here)
create_tables()

app = FastAPI()

# Include your router
app.include_router(git_router, prefix="/api/v1", tags=["Git Operations"])
app.include_router(file_router, prefix="/api/v1", tags=["File Operations"])
app.include_router(email_router, prefix="/api/v1", tags=["Email Operations"])
app.include_router(user_router, prefix="/api/v1", tags=["User Operations"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)