from fastapi import FastAPI, Depends
from slowapi.middleware import SlowAPIMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from app.routes import router as email_router
from app.routes import get_current_user  # Import the authentication dependency

# Initialize the limiter with the FastAPI app
limiter = Limiter(key_func=get_remote_address)

app = FastAPI()

# Add rate-limiting middleware
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Include the router with global authentication dependency
app.include_router(email_router, dependencies=[Depends(get_current_user)])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
