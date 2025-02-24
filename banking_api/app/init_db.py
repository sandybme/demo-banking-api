"""
Database Initialization Script for Entrix Banking API

This module initializes the SQLite database (`bank.db`) with predefined test customers and accounts.

Features:
- Ensures database tables exist before inserting data.
- Prevents duplicate data insertion on repeated runs.
- Preloads the database with sample customers and accounts for testing.
- Supports multiple accounts per customer.

Author: Sandhanakrishnan Ravichandran
Version: 1.0
"""

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, Customer, Account


def initialize_db():
    """
    Initializes the SQLite database with predefined test customers and accounts.

    This function:
    - Ensures database tables are created.
    - Prevents duplicate initialization.
    - Inserts test customers and accounts for development and testing.

    Returns:
        None
    """

    # Ensure database tables exist
    Base.metadata.create_all(bind=engine)

    # Open a new database session
    db = SessionLocal()

    # Check if customers already exist to avoid duplicate initialization
    existing_customers = db.query(Customer).count()
    if existing_customers > 0:
        print("Database already initialized. Skipping data insertion.")
        db.close()
        return

    # Define test customers
    customers = [
        Customer(id=1, name="Arisha Barron"),
        Customer(id=2, name="Branden Gibson"),
        Customer(id=3, name="Rhonda Church"),
        Customer(id=4, name="Georgina Hazel"),
    ]

    # Add customers to the database
    db.add_all(customers)
    db.commit()

    # Define test accounts (one customer has multiple accounts)
    accounts = [
        Account(account_number="DE1000000000000001", balance=5000.0, customer_id=1),  # Arisha Barron (Account 1)
        Account(account_number="DE2000000000000002", balance=3000.0, customer_id=2),  # Branden Gibson
        Account(account_number="DE3000000000000003", balance=4000.0, customer_id=3),  # Rhonda Church
        Account(account_number="DE4000000000000004", balance=2500.0, customer_id=1),  # Arisha Barron (Account 2)
        Account(account_number="DE5000000000000005", balance=6000.0, customer_id=4),  # Georgina Hazel
    ]

    # Add accounts to the database
    db.add_all(accounts)
    db.commit()

    # Close the database session
    db.close()
    print("Database initialized successfully with test customers and accounts.")