import sqlite3
import csv
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def categorize(description):
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

def load_csv(filepath):
    conn = sqlite3.connect("budget.db")
    cursor = conn.cursor()
    
    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            category = categorize(row["description"])
            cursor.execute(
                "INSERT INTO transactions (date, description, amount, category) VALUES (?, ?, ?, ?)",
                (row["date"], row["description"], float(row["amount"]), category)
            )
            print(f"{row['description']} → {category}")
    
    conn.commit()
    conn.close()
    print("Done! All transactions loaded.")

load_csv("sample.csv")
