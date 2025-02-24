
"""
Pytest configuration for setting up the test database.

This module:
    - Creates a fresh test database before running tests.
    - Ensures that all models from `models.py` are properly loaded.
    - Provides reusable fixtures for database access.
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import sqlalchemy
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db
from app.models import Base, Account # Import models to ensure table definitions are loaded
from app.main import app
from fastapi.testclient import TestClient
import pytest
import warnings
# Test database configuration
TEST_DATABASE_URL = "sqlite:///./test_bank.db"

# Create an engine for the test database
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    """
    Provides a test database session override for FastAPI.

    This function replaces the standard database session
    with a test database session to ensure test isolation.

    Yields:
        Session: A SQLAlchemy session connected to the test database.
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Override FastAPI's dependency injection to use the test database
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """
    Pytest fixture to initialize the test database.

    This fixture:
    - Drops all tables before tests run to ensure a clean state.
    - Creates tables based on models defined in `models.py`.
    - Runs once before all tests.

    Returns:
        None
    """
    Base.metadata.drop_all(bind=engine)  # Drop tables before creating new ones
    Base.metadata.create_all(bind=engine)  # Create tables from models.py

@pytest.fixture(scope="function")
def db():
    """
    Pytest fixture to provide a clean database session for each test.

    This fixture:
    - Resets the database schema before each test.
    - Provides an isolated database session for testing.

    Returns:
        Session: A SQLAlchemy session connected to the test database.
    """
    Base.metadata.drop_all(bind=engine)  # Reset database schema before each test
    Base.metadata.create_all(bind=engine)  # Recreate tables

    db = TestingSessionLocal()
    yield db
    db.close()

@pytest.fixture(scope="module")
def client():
    """
    Pytest fixture to create a FastAPI test client.

    This client allows sending HTTP requests to the API
    without starting an actual server.

    Returns:
        TestClient: A FastAPI test client.
    """
    return TestClient(app)

