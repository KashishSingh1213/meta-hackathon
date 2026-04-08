"""Main FastAPI application for ClinIQ."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file FIRST
load_dotenv()

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.routes import router

# Create FastAPI app
app = FastAPI(
    title="ClinIQ - Clinical Intelligence Query Environment",
    description="AI-powered medical simulation platform for clinical decision-making",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom exception handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors with detailed logging."""
    print(f"❌ Validation error on {request.method} {request.url.path}")
    print(f"📊 Request body: {await request.body()}")
    errors = exc.errors()
    print(f"🔴 Validation errors: {errors}")
    
    return JSONResponse(
        status_code=422,
        content={
            "detail": errors,
            "message": "Request validation failed",
            "path": str(request.url.path),
        },
    )

# Include routes
app.include_router(router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to ClinIQ",
        "docs": "/docs",
        "api_version": "1.0.0",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
    )
