import streamlit as st
import os

st.set_page_config(page_title="BIT AI Support", page_icon="🎓")
st.title("🎓 AI Student Support Agent")
st.caption("University College of Engineering, BIT Campus, Tiruchirappalli")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

def load_data():
    base = os.path.dirname(os.path.abspath(__file__))
    paths = [
        os.path.join(base, "college_data.txt"),
        os.path.join(base, "Data", "college_data.txt"),
        "college_data.txt",
        "Data/college_data.txt"
    ]
    for p in paths:
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
    return ""

def get_answer(user_q):
    data = load_data()
    lines = [l.strip() for l in data.splitlines() if l.strip()]

    q = user_q.lower().strip()
    q_words = [w for w in q.split() if len(w) > 2]

    best_line = None
    best_score = -1

    for line in lines:
        ll = line.lower()
        score = 0

        # Exact phrase bonus
        if q in ll:
            score += 20

        # Word by word match from file
        for w in q_words:
            # handle fee/fees, company/companies
            base_w = w.rstrip('s')
            if w in ll or base_w in ll:
                score += 2

        # Special handling for your file keywords
        if "exam fee" in q and "exam fees" in ll: score += 20
        if "due date" in q and "due date" in ll: score += 20
        if "college name" in q and "college name" in ll: score += 20
        if "college code" in q and "college code" in ll: score += 20
        if "companies" in q or "company" in q:
            if "companies visited" in ll: score += 20
        if "sem 1" in q or "sem1" in q:
            if "sem1" in ll: score += 20
        if "sem 2" in q or "sem2" in q:
            if "sem2" in ll: score += 20

        if score > best_score:
            best_score = score
            best_line = line

    if best_line and best_score > 0:
        return f"✅ {best_line}"
    else:
        return "❌ Sorry, not found in college_data.txt"

if prompt := st.chat_input("Ask any question from college data..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    answer = get_answer(prompt)

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
