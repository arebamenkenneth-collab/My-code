import os
import time
import json
import hashlib
import getpass
from datetime import datetime

R  = "\033[0m"
G  = "\033[92m"
Y  = "\033[93m"
B  = "\033[94m"
C  = "\033[96m"
RE = "\033[91m"
W  = "\033[97m"
M  = "\033[95m"
BOLD = "\033[1m"

DATA_FILE = "bank_data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"users": {}}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def hash_pin(pin):
    return hashlib.sha256(pin.encode()).hexdigest()

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def header():
    print(f"{C}{BOLD}")
    print("╔══════════════════════════════════════╗")
    print("║       🏦  CodeWithKenneth Bank       ║")
    print("╚══════════════════════════════════════╝")
    print(f"{R}")

def divider():
    print(f"{B}{'─' * 40}{R}")

def success(msg): print(f"\n{G}✔  {msg}{R}")
def error(msg):   print(f"\n{RE}✘  {msg}{R}")
def info(msg):    print(f"\n{Y}ℹ  {msg}{R}")

def pause():
    input(f"\n{W}Press Enter to continue...{R}")

def reset_data():
    clear(); header()
    print(f"{BOLD}{RE}  ── Reset All Data ──{R}\n")
    confirm = input(f"{RE}  This deletes ALL accounts! Type YES to confirm: {W}").strip()
    if confirm == "YES":
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        success("All data cleared. You can now create a fresh account.")
    else:
        info("Reset cancelled.")
    pause()

def register():
    clear(); header()
    print(f"{BOLD}{W}  ── Create New Account ──{R}\n")
    name = input(f"{C}  Full Name : {W}").strip()
    if not name:
        error("Name cannot be empty."); pause(); return

    acc_no = input(f"{C}  Account No : {W}").strip()
    if not acc_no.isdigit() or len(acc_no) != 10:
        error("Account number must be 10 digits."); pause(); return

    data = load_data()
    if acc_no in data["users"]:
        error("Account number already taken."); pause(); return

    pin = getpass.getpass(f"{C}  Set PIN   : {W}")
    if len(pin) < 4 or not pin.isdigit():
        error("PIN must be 4+ digits."); pause(); return
    confirm = getpass.getpass(f"{C}  Confirm   : {W}")
    if pin != confirm:
        error("PINs do not match."); pause(); return

    for u in data["users"].values():
        if u["name"].lower() == name.lower():
            error("Account with this name already exists."); pause(); return

    data["users"][acc_no] = {
        "name": name,
        "account_no": acc_no,
        "pin": hash_pin(pin),
        "balance": 5000.0,
        "transactions": [
            {
                "type": "credit",
                "amount": 5000.0,
                "note": "Welcome bonus",
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
        ]
    }
    save_data(data)
    success(f"Account created! Your account number: {BOLD}{Y}{acc_no}{R}")
    info("You received a ₦5,000 welcome bonus!")
    pause()

def login():
    clear(); header()
    print(f"{BOLD}{W}  ── Login ──{R}\n")
    acc_no = input(f"{C}  Account No : {W}").strip()
    pin    = getpass.getpass(f"{C}  PIN        : {W}")

    data = load_data()
    user = data["users"].get(acc_no)
    if not user or user["pin"] != hash_pin(pin):
        error("Invalid account number or PIN."); pause(); return None
    success(f"Welcome back, {user['name']}!")
    time.sleep(1)
    return acc_no

def dashboard(acc_no):
    while True:
        data  = load_data()
        user  = data["users"][acc_no]
        clear(); header()
        print(f"{W}{BOLD}  Account   : {C}{acc_no}{R}")
        print(f"{W}{BOLD}  Name      : {G}{user['name']}{R}")
        print(f"{W}{BOLD}  Balance   : {Y}₦{user['balance']:,.2f}{R}")
        divider()
        print(f"\n  {B}[1]{R} Transfer Money")
        print(f"  {B}[2]{R} Deposit")
        print(f"  {B}[3]{R} Withdraw")
        print(f"  {B}[4]{R} Transaction History")
        print(f"  {B}[5]{R} Logout\n")
        divider()
        choice = input(f"\n{C}  Choose option: {W}").strip()

        if   choice == "1": transfer(acc_no)
        elif choice == "2": deposit(acc_no)
        elif choice == "3": withdraw(acc_no)
        elif choice == "4": history(acc_no)
        elif choice == "5": break
        else: error("Invalid option."); pause()

def transfer(acc_no):
    clear(); header()
    print(f"{BOLD}{W}  ── Transfer Money ──{R}\n")

    data = load_data()
    sender = data["users"][acc_no]

    recipient_acc = input(f"{C}  Recipient Account No : {W}").strip()
    if recipient_acc == acc_no:
        error("Cannot transfer to yourself."); pause(); return
    if recipient_acc not in data["users"]:
        error("Recipient account not found."); pause(); return

    recipient = data["users"][recipient_acc]
    print(f"\n{G}  Recipient : {W}{recipient['name']}{R}")

    try:
        amount = float(input(f"{C}  Amount (₦) : {W}").strip())
    except ValueError:
        error("Enter a valid amount."); pause(); return

    if amount <= 0:
        error("Amount must be positive."); pause(); return
    if amount > sender["balance"]:
        error(f"Insufficient balance. Available: ₦{sender['balance']:,.2f}"); pause(); return

    note = input(f"{C}  Note (optional) : {W}").strip() or "Transfer"
    pin  = getpass.getpass(f"{C}  Confirm PIN : {W}")
    if hash_pin(pin) != sender["pin"]:
        error("Incorrect PIN. Transfer cancelled."); pause(); return

    print(f"\n{Y}  ── Confirm Transfer ──{R}")
    print(f"  To      : {G}{recipient['name']} ({recipient_acc}){R}")
    print(f"  Amount  : {Y}₦{amount:,.2f}{R}")
    print(f"  Note    : {W}{note}{R}")
    confirm = input(f"\n{C}  Proceed? (yes/no): {W}").strip().lower()
    if confirm != "yes":
        info("Transfer cancelled."); pause(); return

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    data["users"][acc_no]["balance"] -= amount
    data["users"][acc_no]["transactions"].append({
        "type": "debit",
        "amount": amount,
        "to": f"{recipient['name']} ({recipient_acc})",
        "note": note,
        "date": now
    })
    data["users"][recipient_acc]["balance"] += amount
    data["users"][recipient_acc]["transactions"].append({
        "type": "credit",
        "amount": amount,
        "from": f"{sender['name']} ({acc_no})",
        "note": note,
        "date": now
    })
    save_data(data)

    clear(); header()
    print(f"\n{G}{BOLD}  ✔  Transfer Successful!{R}")
    print(f"\n  {W}Amount   : {Y}₦{amount:,.2f}{R}")
    print(f"  {W}To       : {G}{recipient['name']}{R}")
    print(f"  {W}Balance  : {C}₦{data['users'][acc_no]['balance']:,.2f}{R}")
    print(f"  {W}Date     : {W}{now}{R}")
    pause()

def deposit(acc_no):
    clear(); header()
    print(f"{BOLD}{W}  ── Deposit ──{R}\n")
    try:
        amount = float(input(f"{C}  Amount (₦) : {W}").strip())
    except ValueError:
        error("Invalid amount."); pause(); return
    if amount <= 0:
        error("Amount must be positive."); pause(); return

    data = load_data()
    data["users"][acc_no]["balance"] += amount
    data["users"][acc_no]["transactions"].append({
        "type": "credit",
        "amount": amount,
        "note": "Self deposit",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    save_data(data)
    success(f"₦{amount:,.2f} deposited. New balance: ₦{data['users'][acc_no]['balance']:,.2f}")
    pause()

def withdraw(acc_no):
    clear(); header()
    print(f"{BOLD}{W}  ── Withdraw ──{R}\n")
    try:
        amount = float(input(f"{C}  Amount (₦) : {W}").strip())
    except ValueError:
        error("Invalid amount."); pause(); return

    data = load_data()
    user = data["users"][acc_no]
    if amount <= 0:
        error("Amount must be positive."); pause(); return
    if amount > user["balance"]:
        error(f"Insufficient balance. Available: ₦{user['balance']:,.2f}"); pause(); return

    pin = getpass.getpass(f"{C}  Confirm PIN : {W}")
    if hash_pin(pin) != user["pin"]:
        error("Incorrect PIN."); pause(); return

    data["users"][acc_no]["balance"] -= amount
    data["users"][acc_no]["transactions"].append({
        "type": "debit",
        "amount": amount,
        "note": "Withdrawal",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    save_data(data)
    success(f"₦{amount:,.2f} withdrawn. Balance: ₦{data['users'][acc_no]['balance']:,.2f}")
    pause()

def history(acc_no):
    clear(); header()
    print(f"{BOLD}{W}  ── Transaction History ──{R}\n")

    data = load_data()
    txns = data["users"][acc_no]["transactions"]
    if not txns:
        info("No transactions yet."); pause(); return

    for i, t in enumerate(reversed(txns[-10:]), 1):
        tag   = f"{G}CR{R}" if t["type"] == "credit" else f"{RE}DR{R}"
        color = G if t["type"] == "credit" else RE
        sign  = "+" if t["type"] == "credit" else "-"
        party = t.get("from") or t.get("to") or ""
        print(f"  {B}{i:02}.{R} {tag} {color}{sign}₦{t['amount']:,.2f}{R}  {W}{t['date']}{R}")
        if party:
            label = "From" if t["type"] == "credit" else "To"
            print(f"       {label}: {C}{party}{R}")
        print(f"       Note: {W}{t.get('note','')}{R}")
        divider()
    pause()

def main():
    while True:
        clear(); header()
        print(f"  {B}[1]{R} Create Account")
        print(f"  {B}[2]{R} Login")
        print(f"  {B}[3]{R} Reset All Data")
        print(f"  {B}[4]{R} Exit\n")
        divider()
        choice = input(f"\n{C}  Choose: {W}").strip()

        if   choice == "1": register()
        elif choice == "2":
            acc_no = login()
            if acc_no:
                dashboard(acc_no)
        elif choice == "3": reset_data()
        elif choice == "4":
            print(f"\n{M}  Goodbye! 👋{R}\n"); break
        else:
            error("Invalid option."); pause()

if __name__ == "__main__":
    main()