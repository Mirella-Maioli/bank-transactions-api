from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Bank Transactions API")

class Account(BaseModel):
    name: str
    balance: float = 0

class Transaction(BaseModel):
    account_id: int
    amount: float
    type: str  # deposit or withdraw

accounts = []
transactions = []

@app.post("/accounts")
def create_account(account: Account):
    accounts.append(account)
    return {"message": "Account created", "account": account}

@app.get("/accounts")
def get_accounts():
    return accounts

@app.get("/balance/{account_id}")
def get_balance(account_id: int):
    if account_id < len(accounts):
        return {"balance": accounts[account_id].balance}
    return {"error": "Account not found"}

@app.post("/transactions")
def create_transaction(transaction: Transaction):
    if transaction.account_id >= len(accounts):
        return {"error": "Account not found"}

    account = accounts[transaction.account_id]

    if transaction.type == "deposit":
        account.balance += transaction.amount
    elif transaction.type == "withdraw":
        account.balance -= transaction.amount

    transactions.append(transaction)

    return {"message": "Transaction completed"}

@app.get("/transactions")
def get_transactions():
    return transactions
