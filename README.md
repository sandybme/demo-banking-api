# Entrix Banking API - Run Locally or Pull Docker -- Detailed Instructions Below

## Overview
This is a **banking API** built using **FastAPI** that allows:
- **Creating bank accounts** for customers.
- **Transferring money** between accounts.
- **Retrieving account details and balances**.
- **Fetching transaction history** for a specific IBAN.
- **Unit testing** for core banking functionalities.

---

## Features
✔ Create a **new bank account** for a customer.  
✔ Transfer **money between any two accounts** (including the same customer).  
✔ Retrieve **account balances** and **transaction history**.  
✔ Supports **SQLite (default)** database.  
✔ Includes **unit tests** using `pytest`.  
✔ Uses **FastAPI for high-performance APIs**.

---
## To make life easier, 4 dummy accounts are created with following names, iban and balances:
✔ You can fetch details using the following listed IBANs or account number. Perform Transactions using IBAN. Then check transaction history
```python
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
```

## Installation
### After cloning the Repository (git clone http://entrix-oobjfa@git.codesubmit.io/entrix/banking-api-gdpxyy)
```bash
mkdir banking_api
cd banking_api
```

### Set Up a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Database Configuration
By default, the API uses **SQLite** (`bank.db`).  

---
##  Running the Application
Start the FastAPI server:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
- The API will be available at: **`http://127.0.0.1:8000`**
- Interactive API docs: **`http://127.0.0.1:8000/docs`**

Start the streamlit frontend:
```bash
streamlit run front-end.py --server.port=8501 --server.address=0.0.0.0
```
- frontend will be available at:  **`http://127.0.0.1:8501`**
---

## Running Tests
To run unit tests:
```bash
pytest tests/ -v
```
- **Test cases include:**
  - Creating accounts
  - Transferring money
  - Checking account balances
  - Retrieving transaction history

---
## After Passing Tests You can run docker (assuming docker is downloaded and started)
```bash
cd banking_api
docker build -t banking-api . 
docker rm banking_api
docker run -d --name banking_api -p 8000:8000 -p 8501:8501 banking-api
docker logs banking_api
```
### You can run test inside docker container using the following command
```bash
docker exec banking_api pytest
```

### You can also pull the docker image: https://hub.docker.com/r/sandy9827/banking-api 
```bash
docker pull sandy9827/banking-api:latest
docker run -d -p 8000:8000 -p 8501:8501 sandy9827/banking-api:latest
```
- The API will be available at: **`http://127.0.0.1:8000`**
- frontend will be available at:  **`http://127.0.0.1:8501`**
------


## API Endpoints (File-structure.md)
### Create a Bank Account
**Endpoint:** `POST /accounts/create-account/`  
**Request:**
```json
{
    "existing_customer": false,
    "customer_name": "XXX",
    "balance": 1000.0
}
```
**Response:**
```json
{
    "customer_id": 1,
    "account_id": 1,
    "customer_name": "XXX",
    "account_number": "DE1000000000000001",
    "balance": 1000.0
}
```

---

### Transfer Money Between Accounts
**Endpoint:** `POST /accounts/transfer/`  
**Request:**
```json
{
    "from_iban": "DE1000000000000001",
    "to_iban": "DE2000000000000002",
    "amount": 500.0
}
```
**Response:**
```json
{
    "transaction_id": 1,
    "from_iban": "DE1000000000000001",
    "from_customer_name": "XXX",
    "to_iban": "DE2000000000000002",
    "to_customer_name": "YYY",
    "amount": 500.0,
    "status": "Completed"
}
```

---

### Get Account Balance
**Endpoint:** `GET /accounts/get-account-details/?account_number=DE1000000000000001`  
**Response:**
```json
{
    "customer_id": 1,
    "customer_name": "XXX",
    "account_number": "DE1000000000000001",
    "balance": 500.0
}
```

---

### Retrieve Transaction History
**Endpoint:** `GET /transfer-history/DE1000000000000001`  
**Response:**
```json
{
  "transactions": [
    {
      "transaction_id": 1,
      "from_iban": "DE1000000000000001",
      "from_customer_name": "XXX",
      "to_iban": "DE2000000000000002",
      "to_customer_name": "YYY",
      "amount": 500.0,
      "status": "Completed",
      "timestamp": "N/A"
    }
  ]
}
```

---

