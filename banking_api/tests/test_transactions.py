import pytest
from sqlalchemy.orm import Session
from app.models import Account, Customer, Transaction

def test_transfer_money(client, db: Session):
    """
    Test transferring money between two accounts.

    Steps:
        1. Create test customers in the database.
        2. Create test accounts linked to the customers.
        3. Perform a money transfer (`POST /accounts/transfer/`).
        4. Validate:
            - API response status is `200 OK`.
            - Sender and receiver account balances are updated correctly.
            - The transaction is recorded in the database.
            - API response includes transaction and customer details.

    Args:
        client (TestClient): The FastAPI test client for making API requests.
        db (Session): The test database session.

    Returns:
        None
    """
    # Step 1: Insert test customers
    customer1 = Customer(id=1, name="Arisha Barron")
    customer2 = Customer(id=2, name="Branden Gibson")

    db.add_all([customer1, customer2])
    db.commit()

    # Step 2: Insert test accounts linked to customers
    account1 = Account(account_number="DE1000000000000001", balance=5000.0, customer_id=customer1.id)
    account2 = Account(account_number="DE2000000000000002", balance=3000.0, customer_id=customer2.id)

    db.add_all([account1, account2])
    db.commit()

    # Step 3: Perform a money transfer via API
    response = client.post("/accounts/transfer/", json={
        "from_iban": "DE1000000000000001",
        "to_iban": "DE2000000000000002",
        "amount": 1000.0
    })

    data = response.json()
    assert response.status_code == 200, "Money transfer request failed"

    # Step 4: Verify updated balances in the database
    sender = db.query(Account).filter(Account.account_number == "DE1000000000000001").first()
    receiver = db.query(Account).filter(Account.account_number == "DE2000000000000002").first()

    assert sender.balance == 4000.0, f"Incorrect sender balance, expected 4000.0 but got {sender.balance}"
    assert receiver.balance == 4000.0, f"Incorrect receiver balance, expected 4000.0 but got {receiver.balance}"

    # Step 5: Verify transaction is recorded in the database
    transaction = db.query(Transaction).filter(
        Transaction.from_account_number == "DE1000000000000001",
        Transaction.to_account_number == "DE2000000000000002"
    ).first()

    assert transaction is not None, "Transaction record not found in database"
    assert transaction.amount == 1000.0, "Incorrect transaction amount recorded"

    # Step 6: Verify API response includes correct transaction and customer details
    sender_customer = db.query(Customer).filter(Customer.id == sender.customer_id).first()
    receiver_customer = db.query(Customer).filter(Customer.id == receiver.customer_id).first()

    assert data['transaction_id'] == 1, "Transaction ID mismatch"
    assert data['from_customer_name'] == sender_customer.name, "Sender customer name mismatch"
    assert data['to_customer_name'] == receiver_customer.name, "Receiver customer name mismatch"
    assert data['status'] == "Completed", "Transaction status mismatch"