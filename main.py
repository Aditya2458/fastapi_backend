
from routes import subject_routes
from routes.auth_routes import router as auth_router
from routes import marks_routes
from routes import teacher_subject_routes
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from core.rate_limiter import limiter
from routes.user_routes import router as user_router
from prometheus_fastapi_instrumentator import Instrumentator
from routes.class_routes import router as class_router
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from error import (
    validation_exception_handler,
    http_exception_handler,
    general_exception_handler,
)

app = FastAPI()
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.include_router(class_router)
app.include_router(auth_router)
app.include_router(user_router)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)
#new rate limit handler
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests. Slow down."},
    )
app.include_router(subject_routes.router)
app.include_router(marks_routes.router)
app.include_router(teacher_subject_routes.router)
Instrumentator().instrument(app).expose(app)