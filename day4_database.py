import sqlite3

# Connect to database (creates the file if it doesn't exist)
conn = sqlite3.connect("budget.db")
cursor = conn.cursor()

# Create the transactions table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        description TEXT,
        amount REAL,
        category TEXT
    )
""")

# Insert 5 fake transactions
cursor.execute("INSERT INTO transactions (date, description, amount, category) VALUES ('2024-06-01', 'SWIGGY BANGALORE', 340, NULL)")
cursor.execute("INSERT INTO transactions (date, description, amount, category) VALUES ('2024-06-02', 'NETFLIX', 649, NULL)")
cursor.execute("INSERT INTO transactions (date, description, amount, category) VALUES ('2024-06-03', 'UBER AUTO', 120, NULL)")
cursor.execute("INSERT INTO transactions (date, description, amount, category) VALUES ('2024-06-04', 'ZOMATO', 280, NULL)")
cursor.execute("INSERT INTO transactions (date, description, amount, category) VALUES ('2024-06-05', 'AMAZON', 1200, NULL)")

conn.commit()

# Read them back
cursor.execute("SELECT * FROM transactions")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
# Reopen connection
conn = sqlite3.connect("budget.db")
cursor = conn.cursor()

# Total spend
cursor.execute("SELECT SUM(amount) FROM transactions")
total = cursor.fetchone()
print("Total spend:", total[0])

# Most expensive transaction
cursor.execute("SELECT description, amount FROM transactions ORDER BY amount DESC LIMIT 1")
biggest = cursor.fetchone()
print("Biggest transaction:", biggest[0], "-", biggest[1])

conn.close()
conn = sqlite3.connect("budget.db")
cursor = conn.cursor()

# WHERE - only transactions above 300
print("\n--- Transactions above 300 ---")
cursor.execute("SELECT description, amount FROM transactions WHERE amount > 300")
for row in cursor.fetchall():
    print(row)

# ORDER BY - most expensive first
print("\n--- Most expensive first ---")
cursor.execute("SELECT description, amount FROM transactions ORDER BY amount DESC")
for row in cursor.fetchall():
    print(row)

conn.close()
conn = sqlite3.connect("budget.db")
cursor = conn.cursor()

# First update some categories manually so GROUP BY has something to work with
cursor.execute("UPDATE transactions SET category = 'Food' WHERE description IN ('SWIGGY BANGALORE', 'ZOMATO')")
cursor.execute("UPDATE transactions SET category = 'Transport' WHERE description = 'UBER AUTO'")
cursor.execute("UPDATE transactions SET category = 'Entertainment' WHERE description = 'NETFLIX'")
cursor.execute("UPDATE transactions SET category = 'Shopping' WHERE description = 'AMAZON'")
conn.commit()

# GROUP BY - total spend per category
print("\n--- Spend by category ---")
cursor.execute("SELECT category, SUM(amount) FROM transactions GROUP BY category")
for row in cursor.fetchall():
    print(row)

conn.close()