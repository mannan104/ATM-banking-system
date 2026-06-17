"""
ATM Banking System (Console-Based)
------------------------------------
A simple console application that simulates basic ATM operations:
login/authentication, balance inquiry, cash deposit, cash withdrawal,
mini statement, and PIN change.

Course   : Computer Programming (Lab) - CS-112-L
Task     : Open Ended Lab - ATM Banking System
"""

# ---------------------------------------------------------
# Predefined "database" of bank accounts.
# Key   -> Account Number (string)
# Value -> dictionary holding name, pin, balance and history
# ---------------------------------------------------------
accounts = {
    "1001": {"name": "Ali Raza",    "pin": "1234", "balance": 5000.0,  "history": []},
    "1002": {"name": "Sara Khan",   "pin": "5678", "balance": 12000.0, "history": []},
    "1003": {"name": "Bilal Ahmed", "pin": "0000", "balance": 750.0,   "history": []},
}

MAX_PIN_ATTEMPTS = 3   # how many times a user can retry the PIN


def show_welcome():
    """Display the welcome banner for the ATM."""
    print("=" * 50)
    print("        WELCOME TO THE PYTHON ATM SYSTEM")
    print("=" * 50)


def get_account_number():
    """Take the account number as input from the user and return it."""
    acc_no = input("Enter your Account Number: ").strip()
    return acc_no


def authenticate(account):
    """
    Ask the user for their PIN and verify it against the account.
    Allows up to MAX_PIN_ATTEMPTS tries.
    Returns True if authentication succeeds, False otherwise.
    """
    attempts = 0
    while attempts < MAX_PIN_ATTEMPTS:
        entered_pin = input("Enter your 4-digit PIN: ").strip()

        if not entered_pin.isdigit() or len(entered_pin) != 4:
            print("Invalid format. PIN must be exactly 4 digits.\n")
            attempts += 1
            continue

        if entered_pin == account["pin"]:
            print(f"\nLogin successful. Welcome, {account['name']}!\n")
            return True
        else:
            attempts += 1
            remaining = MAX_PIN_ATTEMPTS - attempts
            if remaining > 0:
                print(f"Incorrect PIN. {remaining} attempt(s) remaining.\n")

    print("Too many incorrect attempts. Card blocked for this session.\n")
    return False


def show_menu():
    """Display the main ATM operations menu."""
    print("-" * 50)
    print("1. Check Balance")
    print("2. Deposit Cash")
    print("3. Withdraw Cash")
    print("4. Mini Statement")
    print("5. Change PIN")
    print("6. Exit")
    print("-" * 50)


def check_balance(account):
    """Print the current balance of the account."""
    print(f"\nYour current balance is: Rs. {account['balance']:.2f}\n")


def deposit_cash(account):
    """Take a deposit amount, validate it, and update the balance."""
    amount_str = input("Enter amount to deposit: Rs. ").strip()

    if not amount_str.replace(".", "", 1).isdigit():
        print("\nInvalid amount entered.\n")
        return

    amount = float(amount_str)

    if amount <= 0:
        print("\nDeposit amount must be greater than zero.\n")
        return

    account["balance"] += amount
    account["history"].append(f"Deposited Rs. {amount:.2f}")
    print(f"\nRs. {amount:.2f} deposited successfully.")
    print(f"New balance: Rs. {account['balance']:.2f}\n")


def withdraw_cash(account):
    """Take a withdrawal amount, validate it, and update the balance."""
    amount_str = input("Enter amount to withdraw: Rs. ").strip()

    if not amount_str.replace(".", "", 1).isdigit():
        print("\nInvalid amount entered.\n")
        return

    amount = float(amount_str)

    if amount <= 0:
        print("\nWithdrawal amount must be greater than zero.\n")
    elif amount > account["balance"]:
        print("\nInsufficient balance. Transaction declined.\n")
    else:
        account["balance"] -= amount
        account["history"].append(f"Withdrew Rs. {amount:.2f}")
        print(f"\nPlease collect your cash: Rs. {amount:.2f}")
        print(f"New balance: Rs. {account['balance']:.2f}\n")


def mini_statement(account):
    """Display the last few transactions for the account."""
    print("\n----- MINI STATEMENT -----")
    if len(account["history"]) == 0:
        print("No transactions yet.")
    else:
        last_five = account["history"][-5:]
        for index, entry in enumerate(last_five, start=1):
            print(f"{index}. {entry}")
    print("---------------------------\n")


def change_pin(account):
    """Allow the user to change their PIN after confirming the new one twice."""
    new_pin = input("Enter new 4-digit PIN: ").strip()
    confirm_pin = input("Confirm new PIN: ").strip()

    if not new_pin.isdigit() or len(new_pin) != 4:
        print("\nInvalid PIN format. PIN not changed.\n")
        return

    if new_pin != confirm_pin:
        print("\nPINs do not match. PIN not changed.\n")
        return

    account["pin"] = new_pin
    account["history"].append("PIN changed")
    print("\nPIN changed successfully.\n")


def run_session(account):
    """
    Run the menu loop for an authenticated account.
    Keeps showing the menu until the user chooses to exit.
    """
    while True:
        show_menu()
        choice = input("Select an option (1-6): ").strip()

        if choice == "1":
            check_balance(account)
        elif choice == "2":
            deposit_cash(account)
        elif choice == "3":
            withdraw_cash(account)
        elif choice == "4":
            mini_statement(account)
        elif choice == "5":
            change_pin(account)
        elif choice == "6":
            print("\nThank you for using the Python ATM System. Goodbye!\n")
            break
        else:
            print("\nInvalid choice. Please select a number between 1 and 6.\n")


def another_customer():
    """Ask whether another customer wants to use the ATM. Returns True/False."""
    answer = input("Do you want to start a new transaction? (y/n): ").strip().lower()
    return answer == "y"


def main():
    """Driver function that controls the overall flow of the program."""
    show_welcome()

    while True:
        acc_no = get_account_number()

        if acc_no not in accounts:
            print("\nAccount not found. Please check the account number.\n")
        else:
            account = accounts[acc_no]
            if authenticate(account):
                run_session(account)

        if not another_customer():
            print("\nSession ended. Thank you!")
            break


if __name__ == "__main__":
    main()
