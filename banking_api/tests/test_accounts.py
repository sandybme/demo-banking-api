import pytest
from sqlalchemy.orm import Session
from app.schemas import AccountCreate
from app.models import Account, Customer

def test_create_account_get_details(client, db: Session):
    """
    Test creating a new bank account and retrieving its details.

    This test follows these steps:
    1. **Create an account** using `POST /accounts/create-account/`.
    2. **Verify the API response** to ensure the expected account details are returned.
    3. **Query the test database** to confirm that the account is stored correctly.
    4. **Validate that the API response matches the database entry**.
    5. **Retrieve account details** using `GET /accounts/get-account-details/`.
    6. **Compare the retrieved details with the expected values**.

    Args:
        client (TestClient): The FastAPI test client used for making API requests.
        db (Session): The SQLAlchemy test database session.

    Returns:
        None
    """
    # Step 1: Create an account via API
    response = client.post("/accounts/create-account/", json={
        "existing_customer": False,
        "customer_name": "Test User",
        "balance": 1000.0
    })

    assert response.status_code == 200, "Account creation failed"

    # Step 2: Verify API response
    data = response.json()
    assert "account_number" in data, "Missing account number in response"
    assert data["customer_name"] == "Test User", "Customer name mismatch"
    assert data["balance"] == 1000.0, "Balance mismatch"

    # Step 3: Query the database for the created account
    account = db.query(Account).filter(Account.customer_id == data["customer_id"]).first()
    assert account is not None, "Account was not created in the database"

    # Step 4: Validate consistency between API response and database entry
    assert account.customer_id == data["customer_id"], "Customer ID mismatch between API and database"
    assert account.account_number == data["account_number"], "Account number mismatch between API and database"
    assert account.balance == data["balance"], "Balance mismatch between API and database"

    # Step 5: Retrieve account details via API
    response = client.get(f"/accounts/get-account-details/?account_number={account.account_number}")
    assert response.status_code == 200, "Account details retrieval failed"

    # Step 6: Validate retrieved details
    retrieved_data = response.json()
    assert retrieved_data["customer_id"] == account.customer_id, "Customer ID mismatch"
    assert retrieved_data["customer_name"] == "Test User", "Customer name mismatch"
    assert retrieved_data["account_number"] == account.account_number, "IBAN mismatch"
    assert retrieved_data["balance"] == 1000.0, "Balance mismatch"