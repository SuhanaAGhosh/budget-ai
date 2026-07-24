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

class Goal(BaseModel):
    category: str
    monthly_limit: float

@app.get("/goals")
def get_goals():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM budget_goals")
    rows = cursor.fetchall()
    conn.close()
    return {"goals": [dict(row) for row in rows]}

@app.post("/goals")
def update_goal(goal: Goal):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO budget_goals (category, monthly_limit) VALUES (?, ?)",
        (goal.category, goal.monthly_limit)
    )
    conn.commit()
    conn.close()
    return {"category": goal.category, "monthly_limit": goal.monthly_limit}
@app.get("/transactions/{year}/{month}")
def get_transactions_by_month(year: int, month: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM transactions 
        WHERE strftime('%Y', date) = ? 
        AND strftime('%m', date) = ?
        ORDER BY date
    """, (str(year), str(month).zfill(2)))
    rows = cursor.fetchall()
    conn.close()
    return {"transactions": [dict(row) for row in rows]}
@app.get("/warnings/{year}/{month}")
def get_warnings(year: int, month: int):
    conn = get_db()
    cursor = conn.cursor()
    
    # Get this month's spending by category
    cursor.execute("""
        SELECT category, SUM(amount) as spent
        FROM transactions
        WHERE strftime('%Y', date) = ?
        AND strftime('%m', date) = ?
        GROUP BY category
    """, (str(year), str(month).zfill(2)))
    spending = {row["category"]: row["spent"] for row in cursor.fetchall()}
    
    # Get budget goals
    cursor.execute("SELECT category, monthly_limit FROM budget_goals")
    goals = {row["category"]: row["monthly_limit"] for row in cursor.fetchall()}
    
    conn.close()
    
    warnings = []
    for category, limit in goals.items():
        spent = spending.get(category, 0)
        percentage = (spent / limit) * 100 if limit > 0 else 0
        
        if percentage > 100:
            warnings.append({
                "category": category,
                "status": "exceeded",
                "spent": spent,
                "limit": limit,
                "message": f"You've exceeded your {category} budget by ₹{spent - limit:.0f}"
            })
        elif percentage == 100:
            warnings.append({
                "category": category,
                "status": "warning",
                "spent": spent,
                "limit": limit,
                "message": f"You've hit your exact {category} budget limit of ₹{limit:.0f}"
            })
        elif percentage >= 80:
            warnings.append({
                "category": category,
                "status": "warning",
                "spent": spent,
                "limit": limit,
                "message": f"You've used {percentage:.0f}% of your {category} budget (₹{spent:.0f} of ₹{limit:.0f})"
            })
    
    return {"warnings": warnings}
@app.get("/history")
def get_history():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            strftime('%Y', date) as year,
            strftime('%m', date) as month,
            category,
            SUM(amount) as total
        FROM transactions
        GROUP BY year, month, category
        ORDER BY year, month
    """)
    rows = cursor.fetchall()
    conn.close()
    return {"history": [dict(row) for row in rows]}