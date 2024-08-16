from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# Define email credentials (replace with your own or load from environment variables)
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = os.getenv("SMTP_PORT", 587)
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "your-email@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "your-password")

app = FastAPI()

class EmailSchema(BaseModel):
    email: EmailStr
    subject: str
    message: str

def send_email(to_email: str, subject: str, message: str, from_alias: str = "noreply-analytics@id.ey.com"):
    try:
        # Setup the MIME
        msg = MIMEMultipart()
        msg['From'] = f"{from_alias} <{EMAIL_ADDRESS}>"
        msg['To'] = to_email
        msg['Subject'] = subject

        # Attach the message to the MIME message
        msg.attach(MIMEText(message, 'plain'))

        # Create SMTP session for sending the mail
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        # Send the email
        server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        server.quit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {e}")

@app.post("/send-email/")
def send_email_api(email_data: EmailSchema):
    send_email(email_data.email, email_data.subject, email_data.message)
    return {"message": "Email sent successfully"}

@app.get('/')
def main():
    return "Hello World"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
