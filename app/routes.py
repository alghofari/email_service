from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.schemas import EmailSchema
from app.email_sender import EmailSender
from app.config import settings

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)
security = HTTPBasic()

def authenticate(credentials: HTTPBasicCredentials):
    if credentials.username != settings.API_USERNAME or credentials.password != settings.API_PASSWORD:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
# Authentication dependency
def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    authenticate(credentials)
    
@router.get("/")
def index():
    return {"message": "Hello, World!"}

@router.post("/send-email/")
@limiter.limit("5/15minutes")  # Rate limit: max 5 requests per 15 minute
def send_email_api(request: Request, email_data: EmailSchema, user: HTTPBasicCredentials = Depends(get_current_user)):
    email_sender = EmailSender()
    
    try:
        email_sender.send_email(email_data.to_email, email_data.subject, email_data.message, email_data.cc_email, email_data.bcc_email)
        return {"message": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
