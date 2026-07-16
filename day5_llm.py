import os
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
    return response.choices[0].message.content

# Test it on real transactions
transactions = [
    "SWIGGY BANGALORE",
    "UBER AUTO",
    "NETFLIX",
    "AMAZON",
    "ZOMATO",
    "BESCOM ELECTRICITY",
    "BOOKMYSHOW"
]

for t in transactions:
    category = categorize_transaction(t)
    print(f"{t} → {category}")