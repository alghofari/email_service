from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "your-email@gmail.com")
    EMAIL_ADDRESS_ALIAS = os.getenv("EMAIL_ADDRESS_ALIAS", "your-email-alias@email.com")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "your-password")
    API_USERNAME = os.getenv("API_USERNAME", "admin")
    API_PASSWORD = os.getenv("API_PASSWORD", "password")

settings = Settings()
