# FastAPI Email API with Basic Authentication and Rate Limiting

This project is a FastAPI-based email sending API with features like Basic Authentication and rate limiting. It includes endpoints to send emails and a simple "Hello, World!" endpoint at the root path.

## Features

- **Email Sending API**: Send emails using an SMTP server.
- **Basic Authentication**: Protect API endpoints with username and password authentication.
- **Rate Limiting**: Limit the number of API requests to prevent abuse (5 requests per 15 minutes).
- **Vercel Deployment**: Configuration provided for deploying on Vercel.

## Project Structure

```bash
.
├── app
│   ├── __init__.py
│   ├── main.py            # Entry point for FastAPI application
│   ├── config.py          # Configuration settings for environment variables
│   ├── email_sender.py    # Email sending logic
│   ├── routes.py          # API routes
│   └── schemas.py         # Pydantic models for request validation
├── requirements.txt       # Python dependencies
├── vercel.json            # Vercel deployment configuration
└── README.md              # Project documentation
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/yourproject.git
cd yourproject
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a .env file in the root of your project and add the necessary environment variables:

```bash
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_ADDRESS_ALIAS=your-email-alias@email.com
EMAIL_PASSWORD=your-password
API_USERNAME=admin
API_PASSWORD=password
```

Replace the placeholders with your actual SMTP server details and API credentials.

## Running the Application

To start the FastAPI application locally, use the following command:

```bash
uvicorn app.main:app --reload
```

- The app will run on http://127.0.0.1:8000/.
- You can access the API documentation at http://127.0.0.1:8000/docs.

## API Endpoints

### 1. Root Endpoint

**GET /**

Returns a simple "Hello, World!" message.

```bash
curl http://127.0.0.1:8000/
```

### 2. Send Email Endpoint
**POST /send-email/**

Send an email with the provided email, subject, and message fields.

**Request Body:**

```json
{
  "email": "recipient@example.com",
  "subject": "Test Email",
  "message": "This is a test email sent from FastAPI."
}
```

**Example Request:**

```bash
curl -X POST http://127.0.0.1:8000/send-email/ \
-u user:password \
-H "Content-Type: application/json" \
-d '{
  "email": "recipient@example.com",
  "subject": "Test Email",
  "message": "This is a test email sent from FastAPI."
}'
```

## Rate Limiting

The /send-email/ endpoint is rate-limited to 5 requests per 15 minutes per client IP address. If the limit is exceeded, a 429 status code will be returned.

## Testing

Use curl, Postman, or any HTTP client to test the API endpoints. Ensure that you provide the correct Basic Authentication credentials for accessing the endpoints.

## Contributing

Feel free to submit issues, fork the repository, and send pull requests. Contributions are welcome!

## Acknowledgments

- FastAPI - The web framework used.
- Uvicorn - ASGI server implementation for FastAPI.
- SlowAPI - For implementing rate limiting.
