"""
CRUD Operations for Entrix Banking API

This module contains database interaction logic for managing:
- Customers
- Bank Accounts
- Transactions

Functions:
1. `generate_account_number()` - Generates a unique IBAN-like account number.
2. `get_customer_by_name(db, customer_name)` - Checks if a customer exists.
3. `create_account(db, customer_name, balance, existing_customer)` - Creates a new bank account.
4. `get_account_details(db, account_number)` - Retrieves account details.
5. `transfer_money(db, from_iban, to_iban, amount)` - Handles fund transfers between accounts.
6. `get_transfer_history(db, iban)` - Retrieves transaction history for a given IBAN.

Author: Sandhankrishnan Ravichandran
Version: 1.0
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound, IntegrityError
from app import models
import random
import re

def generate_account_number():
    """
    Generates a unique bank account number in IBAN format.

    Returns:
        str: A randomly generated IBAN-like account number.
    """
    return f"DE{random.randint(10000000000000000000, 99999999999999999999)}"


def get_customer_by_name(db: Session, customer_name: str):
    """
    Checks if a customer exists in the database.

    Args:
        db (Session): The database session.
        customer_name (str): The customer's name.

    Returns:
        Customer: The customer object if found, else None.
    """
    return db.query(models.Customer).filter(models.Customer.name == customer_name).first()


def create_account(db: Session, customer_name: str, balance: float, existing_customer: bool):
    """
    Creates a new bank account for a customer.

    - If `existing_customer` is `True`, links the new account to the existing customer.
    - If `existing_customer` is `False`, creates a new customer and assigns an account.

    Args:
        db (Session): The database session.
        customer_name (str): Name of the customer.
        balance (float): Initial deposit.
        existing_customer (bool): Whether the customer already exists.

    Returns:
        tuple: (Customer object, Account object).
    """
    # Strip leading/trailing spaces
    stripped_name = customer_name.strip()
    if not stripped_name:
        raise ValueError("Invalid customer name: cannot be empty or whitespace.")
    
    # Check that name has letters & spaces only (no digits, punctuation)
    # Adjust regex if you want to allow hyphens, apostrophes, etc.
    if not re.match(r"^[A-Za-z\s]+$", stripped_name):
        raise ValueError("Invalid customer name: letters and spaces only.")
    
    if existing_customer:
        customer = get_customer_by_name(db, customer_name)
    else:
        customer = models.Customer(name=customer_name)
        db.add(customer)
        db.commit()
        db.refresh(customer)

    new_account = models.Account(
        account_number=generate_account_number(),
        balance=balance,
        customer_id=customer.id
    )
    db.add(new_account)
    db.commit()
    db.refresh(new_account)

    return customer, new_account


def get_account_details(db: Session, account_number: str):
    """
    Fetches account details and associated customer information.

    Args:
        db (Session): The database session.
        account_number (str): The IBAN to look up.

    Returns:
        tuple: (Customer object, Account object).

    Raises:
        ValueError: If the account is not found.
    """
    try:
        account = db.query(models.Account).filter(models.Account.account_number == account_number).first()
        if not account:
            raise NoResultFound("Account not found.")
        customer = db.query(models.Customer).filter(models.Customer.id == account.customer_id).first()
        return customer, account
    except NoResultFound as e:
        raise ValueError(str(e))


def transfer_money(db: Session, from_iban: str, to_iban: str, amount: float):
    """
    Transfers money between two accounts.

    - Ensures the sender has sufficient balance.
    - Updates balances for both accounts.
    - Logs the transaction.

    Args:
        db (Session): The database session.
        from_iban (str): Sender's IBAN.
        to_iban (str): Recipient's IBAN.
        amount (float): Transfer amount.

    Returns:
        dict: Transaction details.

    Raises:
        ValueError: If the transfer fails due to insufficient balance or invalid IBAN.
    """
    if amount <= 0:
        raise ValueError("Transfer amount must be greater than zero.")

    from_account = db.query(models.Account).filter(models.Account.account_number == from_iban).first()
    to_account = db.query(models.Account).filter(models.Account.account_number == to_iban).first()

    if from_iban == to_iban:
        raise ValueError("Cannot transfer money to the same account (identical IBAN).")

    if not from_account:
        raise ValueError("Sender IBAN does not exist.")
    if not to_account:
        raise ValueError("Recipient IBAN does not exist.")
    if from_account.balance < amount:
        raise ValueError("Insufficient balance.")
    
    

    from_customer = db.query(models.Customer).filter(models.Customer.id == from_account.customer_id).first()
    to_customer = db.query(models.Customer).filter(models.Customer.id == to_account.customer_id).first()

    try:
        from_account.balance -= float(amount)
        to_account.balance += float(amount)

        transaction = models.Transaction(
            from_account_number=from_iban,
            to_account_number=to_iban,
            amount=amount,
            status="Completed"
        )
        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        return {
            "transaction_id": transaction.id,
            "from_iban": from_iban,
            "from_customer_name": from_customer.name if from_customer else "Unknown",
            "to_iban": to_iban,
            "to_customer_name": to_customer.name if to_customer else "Unknown",
            "amount": amount,
            "status": "Completed"
        }

    except IntegrityError:
        db.rollback()
        raise ValueError("Transaction failed due to a database error.")


def get_transfer_history(db: Session, iban: str):
    """
    Retrieves all transactions related to a given IBAN.

    Args:
        db (Session): The database session.
        iban (str): The IBAN to fetch transaction history.

    Returns:
        list: A list of transactions including customer names.
    """
    transactions = db.query(models.Transaction).filter(
        (models.Transaction.from_account_number == iban) |
        (models.Transaction.to_account_number == iban)
    ).all()

    history = []
    for txn in transactions:
        from_account = db.query(models.Account).filter(models.Account.account_number == txn.from_account_number).first()
        to_account = db.query(models.Account).filter(models.Account.account_number == txn.to_account_number).first()

        from_customer = db.query(models.Customer).filter(models.Customer.id == from_account.customer_id).first() if from_account else None
        to_customer = db.query(models.Customer).filter(models.Customer.id == to_account.customer_id).first() if to_account else None

        history.append({
            "transaction_id": txn.id,
            "from_iban": txn.from_account_number,
            "from_customer_name": from_customer.name if from_customer else "Unknown",
            "to_iban": txn.to_account_number,
            "to_customer_name": to_customer.name if to_customer else "Unknown",
            "amount": txn.amount,
            "status": txn.status,
            "timestamp": txn.timestamp if hasattr(txn, "timestamp") else "N/A"
        })

    return history