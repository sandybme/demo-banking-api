"""
Account and Transaction API Endpoints for Entrix Banking API

This module provides API routes for:
- Creating a new bank account.
- Retrieving account details.
- Transferring money between accounts.
- Fetching transaction history.

Routes:
1. `POST /create-account/` - Create a new bank account.
2. `GET /get-account-details/` - Retrieve account details.
3. `POST /transfer/` - Transfer money between accounts.
4. `GET /transfer-history/{iban}` - Fetch transaction history.

Author: Sandhankrishnan Ravichandran
Version: 1.0
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter()


@router.post("/create-account/", response_model=schemas.AccountResponse)
def create_account(account_data: schemas.AccountCreate, db: Session = Depends(get_db)):
    """
    Creates a new bank account.

    - If `existing_customer` is `True`, links a new account to the existing customer.
    - If `existing_customer` is `False`, creates a new customer with a new account.

    Args:
        account_data (schemas.AccountCreate): Contains customer details and initial balance.
        db (Session): The database session.

    Returns:
        schemas.AccountResponse: The created account details.

    Raises:
        HTTPException: If an error occurs during account creation.
    """
    try:
        if account_data.balance<50:
            raise ValueError("Minimum deposit should be 50 Euros")
        customer, new_account = crud.create_account(
            db, account_data.customer_name, account_data.balance, account_data.existing_customer
        )
        return {
            "customer_id": customer.id,
            "account_id": new_account.id,
            "customer_name": customer.name,
            "account_number": new_account.account_number,
            "balance": new_account.balance
        }
    except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

@router.get("/get-account-details/", response_model=schemas.AccountResponse)
def get_account_details(account_number: str, db: Session = Depends(get_db)):
    """
    Retrieves account details based on an IBAN.

    Args:
        account_number (str): The IBAN of the account to fetch.
        db (Session): The database session.

    Returns:
        schemas.AccountResponse: Account details including customer information.

    Raises:
        HTTPException: If the account does not exist.
    """
    try:
        customer, account = crud.get_account_details(db, account_number)
        return schemas.AccountResponse(
            customer_id=account.customer_id,
            account_id=account.id,
            customer_name=customer.name,
            account_number=account.account_number,
            balance=account.balance
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/transfer/", response_model=schemas.TransactionResponse)
def transfer_money(transfer_data: schemas.TransactionCreate, db: Session = Depends(get_db)):
    """
    Transfers money from one IBAN to another.

    - Validates sender and receiver accounts.
    - Ensures sufficient balance before processing.
    - Records the transaction.

    Args:
        transfer_data (schemas.TransactionCreate): Transfer details (from IBAN, to IBAN, amount).
        db (Session): The database session.

    Returns:
        schemas.TransactionResponse: Details of the completed transaction.

    Raises:
        HTTPException: If the transfer fails due to insufficient balance or invalid accounts.
    """
    try:
        if transfer_data.amount <= 0.0:
            raise ValueError("Minimum transfer amount should be greater than 0.0")
        transaction = crud.transfer_money(
            db,
            transfer_data.from_iban,
            transfer_data.to_iban,
            transfer_data.amount
        )
        return schemas.TransactionResponse(**transaction)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/transfer-history/{iban}", response_model=schemas.TransferHistoryListResponse)
def get_transfer_history(iban: str, db: Session = Depends(get_db)):
    """
    Retrieves all transaction history for a given IBAN.

    - Fetches both incoming and outgoing transactions.

    Args:
        iban (str): The IBAN whose transfer history is being fetched.
        db (Session): The database session.

    Returns:
        schemas.TransferHistoryListResponse: List of transactions including customer details.

    Raises:
        HTTPException: If the transaction history cannot be retrieved.
    """
    try:
        transactions = crud.get_transfer_history(db, iban)
        return {"transactions": transactions}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))