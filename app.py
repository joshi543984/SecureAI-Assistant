import streamlit as st
from models.llm import get_response
from utils.rag import add_documents, retrieve
from utils.pdf_reader import read_pdf
from utils.web_search import search_web

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Cyber Dashboard", layout="wide")

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #0a0f1c, #05070d);
    color: #ffffff;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0f172a;
    border-right: 1px solid #1f2937;
}

/* Title Glow */
h1 {
    color: #00f7ff;
    text-shadow: 0 0 10px #00f7ff;
}

/* Chat bubbles */
.chat-user {
    background: #1f2937;
    padding: 12px;
    border-radius: 10px;
    margin: 8px 0;
    border-left: 4px solid #00f7ff;
}

.chat-bot {
    background: #111827;
    padding: 12px;
    border-radius: 10px;
    margin: 8px 0;
    border-left: 4px solid #00ff9f;
}

/* Input box */
input {
    background-color: #0f172a !important;
    color: white !important;
}

/* Buttons */
.stButton button {
    background: linear-gradient(90deg, #00f7ff, #00ff9f);
    color: black;
    border-radius: 8px;
    font-weight: bold;
}

/* Glow effect */
.stButton button:hover {
    box-shadow: 0 0 15px #00f7ff;
}

/* Status badge */
.status {
    padding: 8px;
    border-radius: 8px;
    background-color: #022c22;
    color: #00ff9f;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# ------------------ HEADER ------------------
st.markdown("""
<h1 style='text-align:center;'>🛡️ NEXUS Cyber Intelligence System</h1>
<p style='text-align:center; color:gray;'>AI-powered Threat Analysis & Document Intelligence</p>
""", unsafe_allow_html=True)

# ------------------ SESSION ------------------
if "docs_loaded" not in st.session_state:
    st.session_state.docs_loaded = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ------------------ SIDEBAR ------------------
with st.sidebar:
    st.header("⚙️ Control Panel")

    uploaded_file = st.file_uploader("📄 Upload PDF", type=["pdf"])

    if uploaded_file and not st.session_state.docs_loaded:
        try:
            text = read_pdf(uploaded_file)

            if text:
                text = text.replace("\n", " ")
                chunks = [text[i:i+500] for i in range(0, len(text), 500)]

                add_documents(chunks)
                st.session_state.docs_loaded = True
                st.success("✅ PDF Loaded")
            else:
                st.warning("⚠️ No text found")

        except Exception as e:
            st.error(f"Error: {str(e)}")

    if st.button("🔄 Reset"):
        st.session_state.docs_loaded = False
        st.session_state.chat_history = []

    st.markdown("---")
    st.markdown('<div class="status">🟢 System Active</div>', unsafe_allow_html=True)

# ------------------ CHAT INPUT ------------------
query = st.text_input("💬 Ask a question:")

if query:
    try:
        # ----------- PDF LOGIC -----------
        if st.session_state.docs_loaded:
            docs = retrieve(query)

            if docs:
                context = " ".join(docs)

                prompt = f"""
Answer ONLY using the context below.
If not found, say "Not found".

Context:
{context}

Question:
{query}
"""

                answer = get_response(prompt)

                # Web fallback
                if "not found" in answer.lower():
                    web_data = search_web(query)
                    answer = get_response(f"Use this:\n{web_data}")

            else:
                web_data = search_web(query)
                answer = get_response(f"Use this:\n{web_data}")

        # ----------- NO PDF -----------
        else:
            web_data = search_web(query)
            answer = get_response(f"Use this:\n{web_data}")

        # Save chat
        st.session_state.chat_history.append(("You", query))
        st.session_state.chat_history.append(("Bot", answer))

    except Exception as e:
        st.error(f"Error: {str(e)}")

# ------------------ CHAT DISPLAY ------------------
st.subheader("💬 Chat Window")

for sender, msg in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f'<div class="chat-user">🧑‍💻 {msg}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-bot">🤖 {msg}</div>', unsafe_allow_html=True)