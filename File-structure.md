banking_api/
│── app/
│   ├── __init__.py
│   ├── main.py            # Entry point for FastAPI application
│   ├── database.py        # Database setup and session management
│   ├── models.py          # SQLAlchemy models
│   ├── schemas.py         # Pydantic schemas for request/response validation
│   ├── crud.py            # Database interaction logic
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── accounts.py    # Account and transactions related API endpoints
│ 
│── tests/
│   ├── __init__.py
│   ├── test_accounts.py   # Unit tests for account operations (Creation, Retrieval)
│   ├── test_transactions.py # Unit tests for transactions
├   ├── test_transactions_history.py # Unit tests for transactions history (between accounts of same or different customers)
│   ├── conftest.py        # Test fixtures for database setup
│── .gitignore             # Files to be ignored by Git
│── requirements.txt       # Python dependencies
│── README.md              # Documentation from Entrix
│── Dockerfile             # Docker configuration