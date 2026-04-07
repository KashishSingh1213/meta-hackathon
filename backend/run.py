"""
Production server startup script.
Run this to start the ClinIQ backend in production mode.
"""

if __name__ == "__main__":
    import os
    import uvicorn
    from app.main import app

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    environment = os.getenv("ENVIRONMENT", "development")

    print(f"🏥 ClinIQ Backend Server")
    print(f"Environment: {environment}")
    print(f"Server: {host}:{port}")
    print("")

    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info" if environment == "production" else "debug",
    )
