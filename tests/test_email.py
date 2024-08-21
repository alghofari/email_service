import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.email_sender import EmailSender
from app.config import settings

client = TestClient(app)

@pytest.mark.asyncio
@patch.object(EmailSender, 'send_email', return_value=None)
async def test_send_email(mock_send_email):
    # Mock data
    data = {
        "to_email": ["recipient1@example.com"],
        "subject": "Test Email",
        "message": "This is a test email"
    }

    # Test the endpoint
    response = client.post("/send-email", json=data, auth=(settings.API_USERNAME, settings.API_PASSWORD))

    # Assert the response
    assert response.status_code == 200
    assert response.json() == {"message": "Email sent successfully"}

@pytest.mark.asyncio
@patch.object(EmailSender, 'send_email', return_value=None)
async def test_send_email_with_cc_bcc(mock_send_email):
    # Mock data
    data = {
        "to_email": ["recipient1@example.com"],
        "subject": "Test Email with CC and BCC",
        "message": "<p>This is a test email</p>",
        "cc_email": ["cc1@example.com"],
        "bcc_email": ["bcc1@example.com"]
    }

    # Test the endpoint
    response = client.post("/send-email", json=data, auth=(settings.API_USERNAME, settings.API_PASSWORD))

    # Assert the response
    assert response.status_code == 200
    assert response.json() == {"message": "Email sent successfully"}

@pytest.mark.asyncio
@patch.object(EmailSender, 'send_email', side_effect=Exception("SMTP Error"))
async def test_send_email_failure(mock_send_email):
    # Mock data
    data = {
        "to_email": ["recipient1@example.com"],
        "subject": "Test Email Failure",
        "message": "This is a test email"
    }

    # Test the endpoint
    response = client.post("/send-email", json=data, auth=(settings.API_USERNAME, settings.API_PASSWORD))

    # Assert the response
    assert response.status_code == 500
    assert "SMTP Error" in response.json()["detail"]

    # Assert that the send_email method was called once and raised an exception
    mock_send_email.assert_called_once()
