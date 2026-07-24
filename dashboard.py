import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os
from groq import Groq
from dotenv import load_dotenv
import csv
import io

load_dotenv()
BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Budget AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }

.stApp { background-color: #12120f; }

[data-testid="stSidebar"] {
    background-color: #1a1f14;
    border-right: 1px solid #3d5c35;
}

.app-title {
    font-size: 42px;
    font-weight: 700;
    color: #a8c490;
    text-align: center;
    letter-spacing: -1px;
}

.app-subtitle {
    font-size: 16px;
    color: #6b8560;
    text-align: center;
    margin-bottom: 24px;
}

.metric-card {
    background: linear-gradient(135deg, #1e2b18, #243020);
    border: 1px solid #4a7040;
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    margin-bottom: 16px;
}

.metric-value {
    font-size: 26px;
    font-weight: 700;
    color: #a8c490;
}

.metric-label {
    font-size: 12px;
    color: #6b8560;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 4px;
}

.warning-exceeded {
    background: linear-gradient(135deg, #2e1818, #3d2020);
    border: 1px solid #8b3a3a;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 10px;
    color: #e8b5b5;
}

.warning-warn {
    background: linear-gradient(135deg, #2e2518, #3d3020);
    border: 1px solid #8b6e3a;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 10px;
    color: #e8d5b5;
}

.ai-answer {
    background: linear-gradient(135deg, #1e2b18, #243020);
    border: 1px solid #4a7040;
    border-left: 4px solid #7d9b76;
    border-radius: 12px;
    padding: 20px;
    color: #c8d8b5;
    font-size: 15px;
    line-height: 1.7;
}

h1, h2, h3, h4 { color: #a8c490 !important; }
</style>
""", unsafe_allow_html=True)

def fetch(endpoint):
    try:
        return requests.get(f"{BASE_URL}{endpoint}").json()
    except:
        return None

def month_name(m):
    return ["Jan","Feb","Mar","Apr","May","Jun",
            "Jul","Aug","Sep","Oct","Nov","Dec"][int(m)-1]

# ---- SIDEBAR ----
with st.sidebar:
    st.markdown("### 🌿 Budget AI")
    st.markdown("---")

    st.markdown("**Select Month**")
    year = st.selectbox("Year", [2024, 2025], index=0)
    month = st.selectbox("Month", list(range(1,13)),
                         format_func=lambda x: month_name(x), index=6)

    st.markdown("---")
    st.markdown("**Budget Goals (₹/month)**")

    goals_data = fetch("/goals")
    existing = {}
    if goals_data:
        for g in goals_data["goals"]:
            existing[g["category"]] = g["monthly_limit"]

    categories = ["Food","Transport","Groceries","Shopping",
                  "Electricity","Water","Rent","Entertainment","Desired Expenditure"]

    updated = {}
    for cat in categories:
        updated[cat] = st.number_input(cat, min_value=0,
                                        value=int(existing.get(cat, 1000)),
                                        step=100, key=f"g_{cat}")

    if st.button("💾 Save Goals", use_container_width=True):
        for cat, limit in updated.items():
            requests.post(f"{BASE_URL}/goals",
                          json={"category": cat, "monthly_limit": limit})
        st.success("Goals saved!")

    st.markdown("---")
    st.markdown("**Upload CSV**")
    uploaded = st.file_uploader("Bank statement CSV", type="csv")
    if uploaded:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        content = uploaded.read().decode("utf-8")
        reader = list(csv.DictReader(io.StringIO(content)))
        bar = st.progress(0)
        for i, row in enumerate(reader):
            resp = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role":"user","content":
                    f"Categorize into one of: Food, Transport, Groceries, Shopping, Electricity, Water, Rent, Entertainment, Desired Expenditure. Transaction: {row['description']}. Reply with just the category name."}]
            )
            category = resp.choices[0].message.content.strip()
            requests.post(f"{BASE_URL}/transactions", json={
                "date": row["date"],
                "description": row["description"],
                "amount": float(row["amount"]),
                "category": category
            })
            bar.progress((i+1)/len(reader))
        st.success(f"✅ {len(reader)} transactions loaded!")
        st.rerun()

# ---- MAIN PAGE ----
st.markdown('<div class="app-title">🌿 Budget AI</div>', unsafe_allow_html=True)
st.markdown('<div class="app-subtitle">Your intelligent personal finance assistant</div>', unsafe_allow_html=True)
st.markdown("---")

month_data = fetch(f"/transactions/{year}/{month}")
warnings_data = fetch(f"/warnings/{year}/{month}")
history_data = fetch("/history")

if not month_data or not month_data["transactions"]:
    st.warning(f"No transactions for {month_name(month)} {year}")
    st.stop()

df = pd.DataFrame(month_data["transactions"])

# ---- METRIC CARDS ----
st.markdown(f"### {month_name(month)} {year} Overview")
c1, c2, c3, c4 = st.columns(4)

total = df["amount"].sum()
top_cat = df.groupby("category")["amount"].sum().idxmax()
most_freq = df["description"].value_counts().index[0]
count = len(df)

for col, val, label in zip(
    [c1, c2, c3, c4],
    [f"₹{total:,.0f}", top_cat, most_freq, str(count)],
    ["Total Spent", "Top Category", "Most Frequent", "Transactions"]
):
    col.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{val}</div>
        <div class="metric-label">{label}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("---")

# ---- CHARTS ----
col_l, col_r = st.columns(2)

with col_l:
    st.markdown("#### Spending by Category")
    summary = df.groupby("category")["amount"].sum().reset_index()
    fig = px.pie(summary, values="amount", names="category",
                 color_discrete_sequence=["#7d9b76","#a8c490","#5a7a52",
                                           "#c8d8b5","#3d5c35","#b5c9a1",
                                           "#4a7040","#2d4a2d","#e8f0e0"])
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)",
                      font_color="#c8d8b5")
    st.plotly_chart(fig, use_container_width=True)

with col_r:
    st.markdown("#### Budget Progress")
    if goals_data:
        goals_dict = {g["category"]: g["monthly_limit"] for g in goals_data["goals"]}
        spent_dict = df.groupby("category")["amount"].sum().to_dict()
        for cat, limit in goals_dict.items():
            spent = spent_dict.get(cat, 0)
            pct = min(spent/limit, 1.0) if limit > 0 else 0
            icon = "🔴" if pct >= 1.0 else "🟡" if pct >= 0.8 else "🟢"
            st.markdown(f"**{icon} {cat}** — ₹{spent:,.0f} / ₹{limit:,.0f}")
            st.progress(pct)

st.markdown("---")

# ---- WARNINGS ----
if warnings_data and warnings_data["warnings"]:
    st.markdown("#### ⚠️ Budget Alerts")
    for w in warnings_data["warnings"]:
        css = "warning-exceeded" if w["status"] == "exceeded" else "warning-warn"
        icon = "🚨" if w["status"] == "exceeded" else "⚠️"
        st.markdown(f'<div class="{css}">{icon} {w["message"]}</div>',
                    unsafe_allow_html=True)
    st.markdown("---")

# ---- SPENDING OVER TIME ----
if history_data:
    st.markdown("#### Spending Over Time")
    df_h = pd.DataFrame(history_data["history"])
    df_h["label"] = df_h["month"].apply(month_name) + " " + df_h["year"]
    df_monthly = df_h.groupby("label")["total"].sum().reset_index()
    fig2 = px.line(df_monthly, x="label", y="total", markers=True,
                   color_discrete_sequence=["#7d9b76"])
    fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                       plot_bgcolor="rgba(0,0,0,0)",
                       font_color="#c8d8b5",
                       xaxis=dict(gridcolor="#2d3d2d"),
                       yaxis=dict(gridcolor="#2d3d2d"),
                       xaxis_title="Month", yaxis_title="Total Spend (₹)")
    fig2.update_traces(line=dict(width=3))
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("---")

# ---- TRANSACTIONS TABLE ----
st.markdown("#### Transactions")
show = df[["date","description","amount","category"]].copy()
show["amount"] = show["amount"].apply(lambda x: f"₹{x:,.0f}")
st.dataframe(show, use_container_width=True, hide_index=True)
st.markdown("---")

# ---- ASK ANYTHING ----
st.markdown("#### 🤖 Ask anything about your spending")
q = st.text_input("", placeholder="e.g. Where am I overspending? Compare food vs last month?")
if q:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    all_tx = fetch("/transactions")
    tx_text = pd.DataFrame(all_tx["transactions"]).to_string() if all_tx else ""
    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role":"user","content":
            f"You are a smart personal finance assistant. Transaction data:\n{tx_text}\n\nBudget goals:\n{goals_data}\n\nAnswer concisely: {q}\n\nUse ₹ amounts. Be specific and actionable."}]
    )
    st.markdown(f'<div class="ai-answer">🌿 {resp.choices[0].message.content}</div>',
                unsafe_allow_html=True)
    st.markdown("---")

# ---- LAST MONTH COMPARISON ----
st.markdown("#### Last Month vs This Month")
pm = month - 1 if month > 1 else 12
py = year if month > 1 else year - 1
prev = fetch(f"/transactions/{py}/{pm}")

if prev and prev["transactions"]:
    df_prev = pd.DataFrame(prev["transactions"])
    curr_cat = df.groupby("category")["amount"].sum()
    prev_cat = df_prev.groupby("category")["amount"].sum()
    all_cats = set(curr_cat.index) | set(prev_cat.index)
    rows = []
    for cat in sorted(all_cats):
        c = curr_cat.get(cat, 0)
        p = prev_cat.get(cat, 0)
        diff = c - p
        rows.append({
            "Category": cat,
            f"{month_name(pm)}": f"₹{p:,.0f}",
            f"{month_name(month)}": f"₹{c:,.0f}",
            "Change": f"{'▲' if diff > 0 else '▼'} ₹{abs(diff):,.0f}"
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
else:
    st.info("No data for last month.")
