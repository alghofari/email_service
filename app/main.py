from fastapi import FastAPI, Depends
from slowapi.middleware import SlowAPIMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from app.routes import router as email_router

# Initialize the limiter with the FastAPI app
limiter = Limiter(key_func=get_remote_address)

app = FastAPI()

# Add rate-limiting middleware
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Include routes
app.include_router(email_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
