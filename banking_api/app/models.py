"""
Database Models for Entrix Banking API

This module defines the database schema using SQLAlchemy ORM.

Tables:
1. Customer - Stores customer details.
2. Account - Stores bank account details linked to a customer.
3. Transaction - Records all financial transactions between accounts.

Relationships:
- One-to-Many: A customer can have multiple accounts.
- Self-Referencing Foreign Keys: Transactions involve two accounts.

Author: Sandhankrishnan Ravichandran
Version: 1.0
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Base class for SQLAlchemy models
Base = declarative_base()


class Customer(Base):
    """
    Represents a customer in the banking system.

    Attributes:
        id (int): Unique identifier for each customer (Auto-incremented).
        name (str): Customer's full name (Unique constraint to avoid duplicates).
        accounts (relationship): One-to-Many relationship with `Account`.
    """
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=False)  
    accounts = relationship("Account", back_populates="owner")  # Links customer to multiple accounts


class Account(Base):
    """
    Represents a bank account belonging to a customer.

    Attributes:
        id (int): Unique identifier for each account (Auto-incremented).
        account_number (str): Unique IBAN-like account number.
        balance (float): Current balance in the account.
        customer_id (int): Foreign key linking the account to a customer.
        owner (relationship): Many-to-One relationship with `Customer`.
    """
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_number = Column(String, unique=True, nullable=False)  # Ensures unique account numbers
    balance = Column(Float, default=0.0)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)  # Establishes link to customer
    owner = relationship("Customer", back_populates="accounts")  # Defines relationship with `Customer`


class Transaction(Base):
    """
    Represents a transaction between two bank accounts.

    Attributes:
        id (int): Unique identifier for each transaction (Auto-incremented).
        from_account_number (str): IBAN of the sender's account.
        to_account_number (str): IBAN of the recipient's account.
        amount (float): Amount transferred between accounts.
        status (str): Transaction status (Default: "Completed").
        from_account (relationship): Self-referential relationship with `Account`.
        to_account (relationship): Self-referential relationship with `Account`.
    """
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    from_account_number = Column(String, ForeignKey("accounts.account_number"), nullable=False)
    to_account_number = Column(String, ForeignKey("accounts.account_number"), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String, nullable=False, default="Completed")

    from_account = relationship("Account", foreign_keys=[from_account_number])  # Links sender account
    to_account = relationship("Account", foreign_keys=[to_account_number])  # Links receiver account