"""
Database Configuration for Entrix Banking API

This module handles the database setup, connection management, and ORM initialization.

Database:
- Uses SQLite for local development (`bank.db`).
- Can be easily switched to PostgreSQL for production.

Components:
1. `engine` - Establishes a connection to the database.
2. `SessionLocal` - Provides a session factory for database interactions.
3. `Base` - Declarative base class for SQLAlchemy models.
4. `get_db()` - Dependency function to manage database sessions.

Author: Sandhankrishnan Ravichandran
Version: 1.0
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL (Change to PostgreSQL in production)
DATABASE_URL = "sqlite:///./bank.db"

# Create the database engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy ORM models
Base = declarative_base()


def get_db():
    """
    Dependency function to provide a database session.

    - Ensures a new session is created for each request.
    - Closes the session after use to prevent resource leaks.

    Yields:
        Session: A SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()