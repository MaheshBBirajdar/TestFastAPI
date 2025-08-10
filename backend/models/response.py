from pydantic import BaseModel

class SuccessResponse(BaseModel):
    status: str
    message: str
    data: dict = {}

class ErrorResponse(BaseModel):
    status: str
    message: str
    data: dict = {}