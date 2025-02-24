"""
Entrix Banking API - Main Application

This module initializes and configures the FastAPI application.

Features:
- Initializes the database.
- Registers API routes for banking operations.
- Serves as the entry point for the FastAPI server.

Author: Sandhanakrishnan Ravichandran
Version: 1.0
"""

from fastapi import FastAPI
from app.database import engine
from app.models import Base
from routes import accounts
from app.init_db import initialize_db

# Initialize the database schema (Ensures tables are created)
Base.metadata.create_all(bind=engine)

# Populate the database with initial test data (if applicable)
initialize_db()
# Create a FastAPI application instance
app = FastAPI(
    title="Entrix Banking API",
    description="An internal API for a financial institution",
    version="1.0",
    contact={
        "name": "Support Team",
        "email": "support@entrix.com",
        "url": "https://www.entrix.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Register API routes for account management
app.include_router(accounts.router, prefix="/accounts", tags=["Accounts"])

@app.get("/", summary="API Health Check")
def read_root():
    """
    Health check endpoint for the API.

    Returns:
        dict: A message confirming that the API is running.
    """
    return {"message": "Welcome to the Entrix Banking API"}