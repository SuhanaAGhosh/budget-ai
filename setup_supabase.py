import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cursor = conn.cursor()

# Create transactions table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id SERIAL PRIMARY KEY,
        date TEXT,
        description TEXT,
        amount REAL,
        category TEXT
    )
""")

# Create budget goals table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS budget_goals (
        id SERIAL PRIMARY KEY,
        category TEXT UNIQUE,
        monthly_limit REAL
    )
""")

# Insert default budget goals
goals = [
    ("Food", 2000),
    ("Transport", 500),
    ("Groceries", 2500),
    ("Shopping", 1500),
    ("Electricity", 1000),
    ("Water", 300),
    ("Rent", 8000),
    ("Entertainment", 1000),
    ("Desired Expenditure", 2000),
]

for cat, limit in goals:
    cursor.execute("""
        INSERT INTO budget_goals (category, monthly_limit) 
        VALUES (%s, %s)
        ON CONFLICT (category) DO NOTHING
    """, (cat, limit))

conn.commit()
cursor.close()
conn.close()
print("Supabase tables created successfully!")
