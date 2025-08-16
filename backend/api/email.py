from fastapi import APIRouter, HTTPException, Depends
from models.response import SuccessResponse
from config import REPO_PATH, repo
from utils.email import validate_email
from models.email import EmailRequest, EmailUpdate, EmailDelete  # Add these models
from services.email import send_mail, retrive_emails, update_email, delete_email  # Add these service functions
from db.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/email_send", response_model=SuccessResponse)
async def send_email(email_req: EmailRequest, db: Session = Depends(get_db)):
    """
    Send an email to a Gmail address using SMTP.
    """
    try:
        recipant_email = validate_email(email_req.recipient)

        email_records = send_mail(
            user_id=email_req.user_id,
            recipient_email=recipant_email,
            subject=email_req.subject,
            body=email_req.body,
            db=db
        )

        return SuccessResponse(
            status="success",
            message=f"Email sent successfully.",
            data={
                "id": email_records.id,
                "sender_name": email_records.sender,
                "sender_id": email_req.user_id,
                "recipient": email_records.recipient,
                "subject": email_records.subject,   
                "body": email_req.body,
                "sent_at": email_records.sent_at,
                "status": email_records.status,
                
            }
        )

    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/email_get", response_model=SuccessResponse)
async def get_emails(db: Session = Depends(get_db)):
    """
    Retrieve all emails sent by a user.
    """
    try:
        emails = retrive_emails(db)

        return SuccessResponse(
            status="success",
            message="Emails retrieved successfully.",
            data={
                "emails":[
                    {
                        "id": email.id,
                        "sender": email.sender,
                        "sender_id": email.user_id,
                        "recipient": email.recipient,
                        "subject": email.subject,
                        "body": email.body,
                        "sent_at": email.sent_at,
                        "status": email.status
                    }
                for email in emails]
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/email_update", response_model=SuccessResponse)
async def update_email_api(email_req: EmailUpdate, db: Session = Depends(get_db)):
    """
    Update an email's details.
    """
    try:
        updated_email = await update_email(email_req, db)
        if not updated_email:
            raise HTTPException(status_code=404, detail="Email not found")
        
        return SuccessResponse(
            status="success",
            message="Email updated successfully.",
            data={
                "id": updated_email.id,
                "sender": updated_email.sender,
                "sender_id": updated_email.user_id,
                "recipient": updated_email.recipient,
                "subject": updated_email.subject,
                "body": updated_email.body,
                "sent_at": updated_email.sent_at,
                "status": updated_email.status
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/email_delete", response_model=SuccessResponse)
async def delete_email_api(email_req: EmailDelete, db: Session = Depends(get_db)):
    """
    Delete an email by ID.
    """
    try:
        deleted_email = await delete_email(email_req.email_id, db)
        if not deleted_email:
            raise HTTPException(status_code=404, detail="Email not found")
        
        return SuccessResponse(
            status="success",
            message="Email deleted successfully.",
            data={
                "id": email_req.email_id
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

