"""
Data Validation Schemas for Entrix Banking API

This module defines Pydantic schemas for request validation and API responses.

Schemas:
1. AccountCreate - Validates account creation requests.
2. AccountResponse - Defines the structure of account-related responses.
3. TransactionCreate - Validates money transfer requests.
4. TransactionResponse - Defines the structure of transaction responses.
5. TransferHistoryResponse - Represents a single transaction history record.
6. TransferHistoryListResponse - Encapsulates a list of transaction history records.

Author: Sandhankrishnan Ravichandran
Version: 1.0
"""

from pydantic import BaseModel, Field
from decimal import Decimal
from typing import List


class AccountCreate(BaseModel):
    """
    Schema for creating a new bank account.

    Attributes:
        existing_customer (bool): Indicates whether the customer already exists.
        customer_name (str): Full name of the customer.
        balance (float): Initial deposit amount.
    """
    existing_customer: bool
    customer_name: str
    balance: float


class AccountResponse(BaseModel):
    """
    Schema for returning account details.

    Attributes:
        customer_id (int): Unique identifier for the customer.
        customer_name (str): Full name of the customer.
        account_number (str): IBAN-like unique account identifier.
        balance (float): Current account balance.
    """
    customer_id: int
    account_id: int
    customer_name: str
    account_number: str
    balance: float


class TransactionCreate(BaseModel):
    """
    Schema for initiating a money transfer.

    Attributes:
        from_iban (str): IBAN of the sender’s account.
        to_iban (str): IBAN of the recipient’s account.
        amount (Decimal): Transfer amount (must be greater than zero).
    """
    from_iban: str = Field(..., min_length=18, max_length=22)
    to_iban: str = Field(..., min_length=18, max_length=22)
    amount: Decimal = Field(..., gt=0)  # Ensures amount is positive


class TransactionResponse(BaseModel):
    """
    Schema for responding with transaction details.

    Attributes:
        transaction_id (int): Unique identifier for the transaction.
        from_iban (str): IBAN of the sender’s account.
        from_customer_name (str): Full name of the sender.
        to_iban (str): IBAN of the recipient’s account.
        to_customer_name (str): Full name of the recipient.
        amount (float): Transfer amount.
        status (str): Status of the transaction (e.g., "Completed").
    """
    transaction_id: int
    from_iban: str
    from_customer_name: str
    to_iban: str
    to_customer_name: str
    amount: float
    status: str

    class Config:
        from_attributes = True  # Allows ORM compatibility


class TransferHistoryResponse(BaseModel):
    """
    Schema for responding with a single transaction history record.

    Attributes:
        transaction_id (int): Unique transaction identifier.
        from_iban (str): IBAN of the sender’s account.
        from_customer_name (str): Full name of the sender.
        to_iban (str): IBAN of the recipient’s account.
        to_customer_name (str): Full name of the recipient.
        amount (float): Transfer amount.
        status (str): Status of the transaction.
        timestamp (str): Timestamp of the transaction (change to `datetime` if applicable).
    """
    transaction_id: int
    from_iban: str
    from_customer_name: str
    to_iban: str
    to_customer_name: str
    amount: float
    status: str
    timestamp: str  # Consider changing this to `datetime` for better handling


class TransferHistoryListResponse(BaseModel):
    """
    Schema for responding with a list of transaction history records.

    Attributes:
        transactions (List[TransferHistoryResponse]): List of transaction history records.
    """
    transactions: List[TransferHistoryResponse]