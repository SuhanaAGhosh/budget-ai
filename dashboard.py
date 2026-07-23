import streamlit as st
import requests
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

st.title("Budget AI Dashboard")

# Fetch data from your FastAPI backend
transactions = requests.get("http://localhost:8000/transactions").json()["transactions"]
summary = requests.get("http://localhost:8000/summary").json()["summary"]

# Convert to dataframes
df_transactions = pd.DataFrame(transactions)
df_summary = pd.DataFrame(summary)

# Show transactions table
st.subheader("All Transactions")
st.dataframe(df_transactions)

# Show spending by category
st.subheader("Spending by Category")
st.bar_chart(df_summary.set_index("category")["total"])

# Show total spend
total = df_transactions["amount"].sum()
st.metric("Total Spend", f"₹{total}")

st.subheader("Ask anything about your spending")

question = st.text_input("Type your question here", placeholder="e.g. how much did I spend on food?")

if question:
    # Get all transactions as context for the LLM
    transactions_text = df_transactions.to_string()
    
    from groq import Groq
    import os
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": f"""You are a personal finance assistant. Here is the user's transaction data:

{transactions_text}

Answer this question based on the data: {question}

Be concise and specific. Use rupee amounts where relevant."""
            }
        ]
    )
    
    st.write(response.choices[0].message.content)
