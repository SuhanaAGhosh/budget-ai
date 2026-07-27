import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cursor = conn.cursor()

transactions = [
    # May 2024
    ("2024-05-01", "SWIGGY BANGALORE", 340, "Food"),
    ("2024-05-02", "NETFLIX", 649, "Entertainment"),
    ("2024-05-03", "UBER AUTO", 120, "Transport"),
    ("2024-05-05", "DMART GROCERIES", 1800, "Groceries"),
    ("2024-05-07", "AMAZON", 1200, "Shopping"),
    ("2024-05-10", "ZOMATO", 280, "Food"),
    ("2024-05-12", "BESCOM ELECTRICITY", 800, "Electricity"),
    ("2024-05-15", "SWIGGY BANGALORE", 450, "Food"),
    ("2024-05-18", "RAPIDO", 80, "Transport"),
    ("2024-05-20", "BLINKIT", 600, "Groceries"),
    ("2024-05-22", "BOOKMYSHOW", 500, "Entertainment"),
    ("2024-05-25", "NEW OUTFIT ZARA", 2000, "Desired Expenditure"),
    ("2024-05-28", "WATER BILL", 200, "Water"),
    ("2024-05-30", "RENT PAYMENT", 8000, "Rent"),
    # June 2024
    ("2024-06-01", "SWIGGY BANGALORE", 380, "Food"),
    ("2024-06-03", "UBER AUTO", 150, "Transport"),
    ("2024-06-05", "DMART GROCERIES", 2100, "Groceries"),
    ("2024-06-07", "NETFLIX", 649, "Entertainment"),
    ("2024-06-10", "ZOMATO", 320, "Food"),
    ("2024-06-12", "BESCOM ELECTRICITY", 950, "Electricity"),
    ("2024-06-14", "AMAZON GADGET", 3500, "Desired Expenditure"),
    ("2024-06-16", "RAPIDO", 95, "Transport"),
    ("2024-06-18", "BLINKIT", 750, "Groceries"),
    ("2024-06-20", "SWIGGY BANGALORE", 420, "Food"),
    ("2024-06-22", "SPOTIFY", 119, "Entertainment"),
    ("2024-06-25", "WATER BILL", 200, "Water"),
    ("2024-06-28", "RENT PAYMENT", 8000, "Rent"),
    ("2024-06-30", "BOOKMYSHOW", 400, "Entertainment"),
    # July 2024
    ("2024-07-01", "SWIGGY BANGALORE", 400, "Food"),
    ("2024-07-03", "UBER AUTO", 130, "Transport"),
    ("2024-07-05", "DMART GROCERIES", 1950, "Groceries"),
    ("2024-07-07", "NETFLIX", 649, "Entertainment"),
    ("2024-07-09", "ZOMATO", 350, "Food"),
    ("2024-07-11", "BESCOM ELECTRICITY", 870, "Electricity"),
    ("2024-07-13", "SWIGGY BANGALORE", 290, "Food"),
    ("2024-07-15", "RAPIDO", 110, "Transport"),
    ("2024-07-17", "BLINKIT", 820, "Groceries"),
    ("2024-07-19", "NEW SHOES", 1800, "Desired Expenditure"),
    ("2024-07-21", "WATER BILL", 200, "Water"),
    ("2024-07-23", "RENT PAYMENT", 8000, "Rent"),
]

cursor.executemany(
    "INSERT INTO transactions (date, description, amount, category) VALUES (%s, %s, %s, %s)",
    transactions
)

conn.commit()
cursor.close()
conn.close()
print(f"Loaded {len(transactions)} transactions into Supabase!")
