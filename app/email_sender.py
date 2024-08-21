import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List
from app.config import settings

class EmailSender:
    def __init__(self):
        self.from_alias = settings.EMAIL_ADDRESS_ALIAS
        self.server = settings.SMTP_SERVER
        self.port = settings.SMTP_PORT
        self.email_address = settings.EMAIL_ADDRESS
        self.email_password = settings.EMAIL_PASSWORD

    def send_email(self, to_emails: List[str], subject: str, message: str, cc_emails: List[str] = None, bcc_emails: List[str] = None):
        try:
            # Determine if the message is HTML by looking for HTML tags
            is_html = self._is_html_content(message)

            # Setup the MIME
            msg = MIMEMultipart("alternative")
            msg['From'] = f"{self.from_alias} <{self.email_address}>"
            msg['To'] = ", ".join(to_emails)  # Join the emails with a comma for the To header

            # Add CC and BCC headers if provided
            if cc_emails:
                msg["Cc"] = ", ".join(cc_emails)
            if bcc_emails:
                bcc_emails = bcc_emails  # BCC is not added to the headers but is included in sendmail

            msg['Subject'] = subject

            # Attach the message to the MIME message
            part = MIMEText(message, "html" if is_html else "plain")
            msg.attach(part)

            # Combine all recipients (To + CC + BCC) for sending
            all_recipients = to_emails + (cc_emails if cc_emails else []) + (bcc_emails if bcc_emails else [])

            # Create SMTP session for sending the mail
            with smtplib.SMTP(self.server, self.port) as server:
                server.starttls()
                server.login(self.email_address, self.email_password)
                server.sendmail(self.email_address, all_recipients, msg.as_string())
        except smtplib.SMTPException as e:
            raise Exception(f"SMTP error occurred: {e}")
        except Exception as e:
            raise Exception(f"Failed to send email: {e}")
        
    def _is_html_content(self, message: str) -> bool:
        # Basic check for HTML tags in the message
        html_pattern = re.compile(r'<[a-z][\s\S]*>', re.IGNORECASE)
        return bool(html_pattern.search(message))
