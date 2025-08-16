from pydantic import BaseModel, Field

class EmailRequest(BaseModel):
    user_id: int = Field(..., description="ID of the user sending the email")
    recipient: str = Field(..., description="Recipient Gmail address")
    subject: str = Field(..., description="Email subject")
    body: str = Field(..., description="Email body (HTML or plain text)")


class EmailUpdate(BaseModel):
    email_id: int
    subject: str
    body: str
    status: str

class EmailDelete(BaseModel):
    email_id: int