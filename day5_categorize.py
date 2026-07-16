import os
import sqlite3
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def categorize_transaction(description):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": f"Categorize this transaction into one of these categories: Food, Transport, Entertainment, Shopping, Bills. Transaction: {description}. Reply with just the category name, nothing else."
            }
        ]
    )
    return response.choices[0].message.content.strip()

# Connect to database
conn = sqlite3.connect("budget.db")
cursor = conn.cursor()

# Get all uncategorized transactions
cursor.execute("SELECT id, description FROM transactions WHERE category IS NULL")
rows = cursor.fetchall()

# Categorize each one and update the database
for row in rows:
    id = row[0]
    description = row[1]
    category = categorize_transaction(description)
    cursor.execute("UPDATE transactions SET category = ? WHERE id = ?", (category, id))
    print(f"{description} → {category}")

conn.commit()

# Show final state of database
print("\n--- All transactions ---")
cursor.execute("SELECT description, amount, category FROM transactions")
for row in cursor.fetchall():
    print(row)

conn.close()