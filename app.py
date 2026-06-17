"""
ATM Banking System (Streamlit Web App)
----------------------------------------
A web-based version of the console ATM Banking System, built with Streamlit
for deployment on Streamlit Community Cloud / GitHub.

Run locally with:
    streamlit run app.py
"""

import streamlit as st

st.set_page_config(page_title="Python ATM Banking System", page_icon="🏦", layout="centered")

# ---------------------------------------------------------
# Initialize the account "database" once per browser session
# ---------------------------------------------------------
if "accounts" not in st.session_state:
    st.session_state.accounts = {
        "1001": {"name": "Ali Raza",    "pin": "1234", "balance": 5000.0,  "history": []},
        "1002": {"name": "Sara Khan",   "pin": "5678", "balance": 12000.0, "history": []},
        "1003": {"name": "Bilal Ahmed", "pin": "0000", "balance": 750.0,   "history": []},
    }

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_acc = None
    st.session_state.attempts = 0

MAX_PIN_ATTEMPTS = 3
accounts = st.session_state.accounts

st.title("🏦 Python ATM Banking System")


def login_screen():
    """Show the account number / PIN login form."""
    st.subheader("Please Login")

    acc_no = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password", max_chars=4)

    if st.button("Login", use_container_width=True):
        if acc_no not in accounts:
            st.error("Account not found. Please check the account number.")
        elif not pin.isdigit() or len(pin) != 4:
            st.error("PIN must be exactly 4 digits.")
        elif pin == accounts[acc_no]["pin"]:
            st.session_state.logged_in = True
            st.session_state.current_acc = acc_no
            st.session_state.attempts = 0
            st.rerun()
        else:
            st.session_state.attempts += 1
            remaining = MAX_PIN_ATTEMPTS - st.session_state.attempts
            if remaining > 0:
                st.error(f"Incorrect PIN. {remaining} attempt(s) remaining.")
            else:
                st.error("Too many incorrect attempts. Please try again later.")

    st.caption("Demo accounts \u2014 1001 / 1234, 1002 / 5678, 1003 / 0000")


def check_balance(account):
    st.metric("Current Balance", f"Rs. {account['balance']:.2f}")


def deposit_cash(account):
    amount = st.number_input("Amount to deposit (Rs.)", min_value=0.0, step=100.0, format="%.2f")
    if st.button("Deposit"):
        if amount <= 0:
            st.error("Deposit amount must be greater than zero.")
        else:
            account["balance"] += amount
            account["history"].append(f"Deposited Rs. {amount:.2f}")
            st.success(f"Rs. {amount:.2f} deposited successfully. New balance: Rs. {account['balance']:.2f}")


def withdraw_cash(account):
    amount = st.number_input("Amount to withdraw (Rs.)", min_value=0.0, step=100.0, format="%.2f")
    if st.button("Withdraw"):
        if amount <= 0:
            st.error("Withdrawal amount must be greater than zero.")
        elif amount > account["balance"]:
            st.error("Insufficient balance. Transaction declined.")
        else:
            account["balance"] -= amount
            account["history"].append(f"Withdrew Rs. {amount:.2f}")
            st.success(f"Please collect Rs. {amount:.2f}. New balance: Rs. {account['balance']:.2f}")


def mini_statement(account):
    st.write("#### Last 5 Transactions")
    if not account["history"]:
        st.info("No transactions yet.")
    else:
        for index, entry in enumerate(account["history"][-5:], start=1):
            st.write(f"{index}. {entry}")


def change_pin(account):
    new_pin = st.text_input("New 4-digit PIN", type="password", max_chars=4, key="new_pin")
    confirm_pin = st.text_input("Confirm new PIN", type="password", max_chars=4, key="confirm_pin")
    if st.button("Update PIN"):
        if not new_pin.isdigit() or len(new_pin) != 4:
            st.error("Invalid PIN format. PIN must be 4 digits.")
        elif new_pin != confirm_pin:
            st.error("PINs do not match. PIN not changed.")
        else:
            account["pin"] = new_pin
            account["history"].append("PIN changed")
            st.success("PIN changed successfully.")


def atm_menu():
    """Main menu shown after a successful login."""
    account = accounts[st.session_state.current_acc]

    st.success(f"Welcome, {account['name']}! (Account: {st.session_state.current_acc})")

    choice = st.sidebar.radio(
        "Select an operation",
        ["Check Balance", "Deposit Cash", "Withdraw Cash", "Mini Statement", "Change PIN", "Logout"]
    )

    if choice == "Check Balance":
        check_balance(account)
    elif choice == "Deposit Cash":
        deposit_cash(account)
    elif choice == "Withdraw Cash":
        withdraw_cash(account)
    elif choice == "Mini Statement":
        mini_statement(account)
    elif choice == "Change PIN":
        change_pin(account)
    elif choice == "Logout":
        st.session_state.logged_in = False
        st.session_state.current_acc = None
        st.session_state.attempts = 0
        st.rerun()


# ---------------------------------------------------------
# Main driver
# ---------------------------------------------------------
if st.session_state.logged_in:
    atm_menu()
else:
    login_screen()
