import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel

class Transaction(BaseModel):
    date: str
    description: str
    amount: float
app = FastAPI()

def get_db():
    conn = sqlite3.connect("budget.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/")
def home():
    return {"message": "Budget AI is running"}

@app.get("/transactions")
def get_transactions():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()
    conn.close()
    return {"transactions": [dict(row) for row in rows]}

@app.get("/summary")
def get_summary():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT category, SUM(amount) as total FROM transactions GROUP BY category")
    rows = cursor.fetchall()
    conn.close()
    return {"summary": [dict(row) for row in rows]}
@app.post("/transactions")
def add_transaction(transaction: Transaction):
    # Categorize using Groq
    from groq import Groq
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": f"Categorize this transaction into one of these categories: Food, Transport, Entertainment, Shopping, Bills. Transaction: {transaction.description}. Reply with just the category name, nothing else."
            }
        ]
    )
    category = response.choices[0].message.content.strip()
    
    # Save to database
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO transactions (date, description, amount, category) VALUES (?, ?, ?, ?)",
        (transaction.date, transaction.description, transaction.amount, category)
    )
    conn.commit()
    conn.close()
    
    return {"description": transaction.description, "category": category, "amount": transaction.amount}