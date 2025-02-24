import streamlit as st
import requests

# Replace with the base URL of your running FastAPI (or any) backend
BASE_URL = "http://127.0.0.1:8000"

st.title("Banking API Tester")

st.sidebar.title("Navigation")
pages = ["Create Account", "Transfer Money", "Get Account Details", "Transaction History"]
choice = st.sidebar.radio("Go to:", pages)

# -----------------------------
# CREATE ACCOUNT
# -----------------------------
if choice == "Create Account":
    st.header("Create a New Bank Account")

    existing_customer = st.checkbox("Existing customer?")
    customer_name = st.text_input("Customer Name")
    initial_deposit = st.number_input("Initial Deposit", min_value=0.0, value=1000.0)

    if st.button("Create Account"):
        endpoint = f"{BASE_URL}/accounts/create-account/"
        payload = {
            "existing_customer": existing_customer,
            "customer_name": customer_name,
            "balance": initial_deposit
        }
        try:
            response = requests.post(endpoint, json=payload)
            if response.status_code == 200:
                st.json(response.json())
            else:
                st.error(f"Error {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")

# -----------------------------
# TRANSFER MONEY
# -----------------------------
elif choice == "Transfer Money":
    st.header("Transfer Funds Between Accounts")

    from_iban = st.text_input("From IBAN")
    to_iban = st.text_input("To IBAN")
    amount = st.number_input("Amount", min_value=0.0, value=100.0)

    if st.button("Transfer"):
        endpoint = f"{BASE_URL}/accounts/transfer/"
        payload = {
            "from_iban": from_iban,
            "to_iban": to_iban,
            "amount": amount
        }
        try:
            response = requests.post(endpoint, json=payload)
            if response.status_code == 200:
                st.json(response.json())
            else:
                st.error(f"Error {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")

# -----------------------------
# GET ACCOUNT DETAILS
# -----------------------------
elif choice == "Get Account Details":
    st.header("Retrieve Account Details")

    account_number = st.text_input("Account Number (IBAN)")
    if st.button("Fetch Details"):
        endpoint = f"{BASE_URL}/accounts/get-account-details/"
        try:
            # Using query param ?account_number=...
            response = requests.get(endpoint, params={"account_number": account_number})
            if response.status_code == 200:
                st.json(response.json())
            else:
                st.error(f"Error {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")

# -----------------------------
# TRANSACTION HISTORY
# -----------------------------
elif choice == "Transaction History":
    st.header("Check Transaction History")

    iban_query = st.text_input("IBAN for Transaction History")
    if st.button("Retrieve History"):
        endpoint = f"{BASE_URL}/accounts/transfer-history/{iban_query}"
        try:
            response = requests.get(endpoint)
            if response.status_code == 200:
                st.json(response.json())
            else:
                st.error(f"Error {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")