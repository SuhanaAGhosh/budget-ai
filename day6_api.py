import sqlite3
from fastapi import FastAPI

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
