from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel
from typing import Optional
from api.git import router as git_router
from api.file import router as file_router
from api.email import router as email_router

app = FastAPI()

# Include your router
app.include_router(git_router, prefix="/api/v1", tags=["Git Operations"])
app.include_router(file_router, prefix="/api/v1", tags=["File Operations"])
app.include_router(email_router, prefix="/api/v1", tags=["Email Operations"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)