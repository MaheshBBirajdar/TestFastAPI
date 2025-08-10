from fastapi import APIRouter, HTTPException
from models.response import SuccessResponse
from config import REPO_PATH, repo
from utils.email import validate_email
from models.email import EmailRequest
from services.email import send_mail

router = APIRouter()

@router.post("/send_email", response_model=SuccessResponse)
async def send_email(email_req: EmailRequest):
    """
    Send an email to a Gmail address using SMTP.
    """
    try:
        recipant_email = validate_email(email_req.recipient)

        send_mail(
            recipient=recipant_email,
            subject=email_req.subject,
            body=email_req.body
        )

        return SuccessResponse(
            status="success",
            message=f"Email sent successfully.",
            data={
                "recipient": email_req.recipient,
                "subject": email_req.subject,
                "body": email_req.body  
            }
        )

    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))