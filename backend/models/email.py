from pydantic import BaseModel, Field

class EmailRequest(BaseModel):
    recipient: str = Field(..., description="Recipient Gmail address")
    subject: str = Field(..., description="Email subject")
    body: str = Field(..., description="Email body (HTML or plain text)")

