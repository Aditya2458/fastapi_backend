from routes import subject_routes
from routes.auth_routes import router as auth_router
from routes import marks_routes
from routes import teacher_subject_routes
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
app.include_router(class_router)
app.include_router(auth_router)
app.include_router(user_router)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)
app.include_router(subject_routes.router)
app.include_router(marks_routes.router)
app.include_router(teacher_subject_routes.router)
Instrumentator().instrument(app).expose(app)