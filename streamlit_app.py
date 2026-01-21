# streamlit_app.py

import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from groq import Groq
import logging

# Setup
logging.basicConfig(level=logging.INFO)
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# LLM Function

def call_llm(prompt: str, model: str = "mixtral-8x7b-32768") -> str:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a fund CFO assistant and capital accounting expert."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

# Functional Modules

def generate_capital_accounting(df: pd.DataFrame) -> str:
    prompt = f"Create a capital account summary by LP for this fund: {df.head(3).to_dict()}"
    return call_llm(prompt)

def calculate_waterfall(df: pd.DataFrame) -> str:
    prompt = f"Calculate IRR, MOIC, carry splits, and waterfall outputs based on: {df.head(3).to_dict()}"
    return call_llm(prompt)

def generate_lp_portal_content(df: pd.DataFrame) -> str:
    prompt = f"Generate LP update summary and performance visuals for: {df.head(3).to_dict()}"
    return call_llm(prompt)

def audit_compliance_pack(text: str) -> str:
    prompt = f"Generate GAAP compliance memo and audit checklist for fund description: {text}"
    return call_llm(prompt)

def cfo_copilot_response(question: str, context: str) -> str:
    prompt = f"Fund context: {context}\nCFO asks: {question}\nRespond as a CFO AI copilot."
    return call_llm(prompt)

# Streamlit UI

def main():
    st.set_page_config("Regent AI – Autonomous Fund CFO", page_icon="🤖", layout="wide")
    st.title("🤖 Regent AI – Autonomous Private Fund CFO")
    st.write("Capital accounting, waterfalls, LP comms, and compliance — fully automated.")

    uploaded_file = st.file_uploader("Upload fund capital data (CSV)", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("Data uploaded successfully.")
    else:
        df = pd.DataFrame()

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📒 Capital Accounts",
        "💧 Waterfall Calculator",
        "📤 LP Portal Builder",
        "🧾 Audit + Compliance",
        "💬 CFO Chatbot"
    ])

    with tab1:
        st.subheader("📒 Generate Capital Account Summary")
        if st.button("Generate Capital Summary"):
            if df.empty:
                st.error("Please upload fund data.")
            else:
                summary = generate_capital_accounting(df)
                st.text_area("Capital Account Summary", value=summary, height=400)

    with tab2:
        st.subheader("💧 Run Waterfall + Returns")
        if st.button("Calculate Waterfall"):
            if df.empty:
                st.error("Please upload distribution data.")
            else:
                calc = calculate_waterfall(df)
                st.text_area("Waterfall Output", value=calc, height=400)

    with tab3:
        st.subheader("📤 LP Update + Portal Content")
        if st.button("Generate LP Comms"):
            if df.empty:
                st.error("Upload fund data first.")
            else:
                lp = generate_lp_portal_content(df)
                st.text_area("LP Portal Copy", value=lp, height=400)

    with tab4:
        st.subheader("🧾 GAAP Audit/Compliance Memos")
        text = st.text_area("Paste fund description or internal notes")
        if st.button("Generate Compliance Pack"):
            if not text:
                st.error("Provide fund description.")
            else:
                pack = audit_compliance_pack(text)
                st.text_area("Audit + GAAP Output", value=pack, height=400)

    with tab5:
        st.subheader("💬 CFO Assistant Chat")
        context = st.text_area("Paste fund ops context")
        q = st.text_input("Ask an operational question")
        if st.button("Ask Regent AI"):
            if not context or not q:
                st.error("Fill both fields.")
            else:
                answer = cfo_copilot_response(q, context)
                st.markdown(f"**AI Answer:** {answer}")

if __name__ == "__main__":
    main()
