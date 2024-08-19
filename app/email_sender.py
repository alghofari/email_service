import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.config import settings

class EmailSender:
    def __init__(self, from_alias: str = "noreply-analytics@id.ey.com"):
        self.from_alias = from_alias
        self.server = settings.SMTP_SERVER
        self.port = settings.SMTP_PORT
        self.email_address = settings.EMAIL_ADDRESS
        self.email_password = settings.EMAIL_PASSWORD

    def send_email(self, to_email: str, subject: str, message: str):
        try:
            # Setup the MIME
            msg = MIMEMultipart()
            msg['From'] = f"{self.from_alias} <{self.email_address}>"
            msg['To'] = to_email
            msg['Subject'] = subject

            # Attach the message to the MIME message
            msg.attach(MIMEText(message, 'plain'))

            # Create SMTP session for sending the mail
            with smtplib.SMTP(self.server, self.port) as server:
                server.starttls()
                server.login(self.email_address, self.email_password)
                server.sendmail(self.email_address, to_email, msg.as_string())
        except smtplib.SMTPException as e:
            raise Exception(f"SMTP error occurred: {e}")
        except Exception as e:
            raise Exception(f"Failed to send email: {e}")
