# budget AI

An AI-powered personal finance assistant that automatically categorizes your transactions, tracks your spending against monthly budgets, and lets you ask questions about your money in plain English.

**Live demo:** https://budget-ai-j2dqwxrztefggryayobtyd.streamlit.app/

---

## What it does

- Upload a bank statement CSV — transactions are auto-categorized using an LLM (Llama 3.1 via Groq)
- Set monthly budget goals per category and track progress in real time
- Get alerts when you're approaching or exceeding a budget limit
- Ask anything: "where am I overspending?" or "compare my food spend vs last month"
- Month-over-month comparison table
- Spending history line chart across months

---

## Tech stack

- **Frontend:** Streamlit
- **Backend:** FastAPI
- **Database:** PostgreSQL (Supabase)
- **LLM:** Llama 3.1 8B via Groq API
- **Charts:** Plotly
- **Language:** Python

---

## How to run locally

1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with your keys.
4. Run the backend: `py -m uvicorn day6_api:app --reload`
5. Run the frontend: `py -m streamlit run dashboard.py`

---

---

## Built by

Suhana Ghosh — BTech AI/ML, PES University, Bangalore

