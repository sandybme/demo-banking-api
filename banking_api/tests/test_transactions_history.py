import pytest
from sqlalchemy.orm import Session
from app.models import Account, Customer, Transaction

def test_transaction_history(client, db: Session):
    """
    Test retrieving transaction history for an account.

    Steps:
        1. Create test customers in the database.
        2. Assign multiple IBANs to the first customer and one IBAN to another customer.
        3. Perform multiple money transfers:
            - Between two IBANs of the same customer.
            - Between an IBAN and another customer.
        4. Retrieve transaction history (`GET /accounts/transfer-history/{iban}`).
        5. Validate:
            - Response status is `200 OK`.
            - Transactions are recorded correctly.
            - The API response includes accurate details.

    Args:
        client (TestClient): The FastAPI test client.
        db (Session): The test database session.

    Returns:
        None
    """
    # Step 1: Insert test customers
    customer1 = Customer(id=1, name="Arisha Barron")
    customer2 = Customer(id=2, name="Branden Gibson")
    customer3 = Customer(id=3, name="Rhonda Church")

    db.add_all([customer1, customer2, customer3])
    db.commit()

    # Step 2: Insert test accounts linked to customers
    account1 = Account(account_number="DE1000000000000001", balance=5000.0, customer_id=customer1.id)
    account2 = Account(account_number="DE4000000000000004", balance=2000.0, customer_id=customer1.id)  # Same customer, different IBAN
    account3 = Account(account_number="DE3000000000000003", balance=1500.0, customer_id=customer3.id)
    account4 = Account(account_number="DE2000000000000002", balance=3000.0, customer_id=customer2.id)

    db.add_all([account1, account2, account3, account4])
    db.commit()

    # Step 3: Perform multiple transactions
    transactions = [
        {"from_iban": "DE1000000000000001", "to_iban": "DE4000000000000004", "amount": 1000.0},  # Transfer within same customer
        {"from_iban": "DE1000000000000001", "to_iban": "DE3000000000000003", "amount": 100.55},  # Transfer to another customer
        {"from_iban": "DE1000000000000001", "to_iban": "DE2000000000000002", "amount": 1000.0},  # Transfer to a second customer
    ]

    for txn in transactions:
        response = client.post("/accounts/transfer/", json=txn)
        assert response.status_code == 200, f"Transfer failed for {txn}"

    # Step 4: Retrieve transaction history for the first IBAN
    response = client.get("/accounts/transfer-history/DE1000000000000001")
    assert response.status_code == 200, "Failed to retrieve transaction history"

    data = response.json()
    assert "transactions" in data, "Missing transactions field"
    assert isinstance(data["transactions"], list), "Transactions field should be a list"
    assert len(data["transactions"]) == 3, f"Expected 3 transactions, got {len(data['transactions'])}"

    # Step 5: Validate transaction details
    expected_transactions = [
        {"from_iban": "DE1000000000000001", "to_iban": "DE4000000000000004", "amount": 1000.0, "to_customer_name": "Arisha Barron"},
        {"from_iban": "DE1000000000000001", "to_iban": "DE3000000000000003", "amount": 100.55, "to_customer_name": "Rhonda Church"},
        {"from_iban": "DE1000000000000001", "to_iban": "DE2000000000000002", "amount": 1000.0, "to_customer_name": "Branden Gibson"},
    ]

    for index, txn in enumerate(data["transactions"]):
        assert txn["from_iban"] == "DE1000000000000001", "Incorrect sender IBAN"
        assert txn["to_iban"] == expected_transactions[index]["to_iban"], "Incorrect receiver IBAN"
        assert txn["amount"] == expected_transactions[index]["amount"], "Incorrect transfer amount"
        assert txn["to_customer_name"] == expected_transactions[index]["to_customer_name"], "Receiver name mismatch"
        assert txn["status"] == "Completed", "Incorrect transaction status"