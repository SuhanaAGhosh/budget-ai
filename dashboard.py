import streamlit as st
import requests
import pandas as pd

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
