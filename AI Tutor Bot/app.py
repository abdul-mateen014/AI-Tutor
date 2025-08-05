import streamlit as st
from pdf_loader import load_and_split_pdf
from rag_chain import build_qa_chain

# Set page config
st.set_page_config(page_title="AI Tutor Bot", layout="centered")
st.title("📘 AI Tutor Bot")

# --- Session State ---
if "chain" not in st.session_state:
    st.session_state.chain = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pdf_processed" not in st.session_state:
    st.session_state.pdf_processed = False
if "processing" not in st.session_state:
    st.session_state.processing = False

# --- File Upload ---
uploaded_file = st.file_uploader("📎 Upload your PDF to begin", type="pdf")

# --- Reset Button ---
if st.button("🔁 Reset"):
    st.session_state.chain = None
    st.session_state.chat_history = []
    st.session_state.pdf_processed = False
    st.session_state.processing = False
    uploaded_file = None
    st.rerun()  # Changed from experimental_rerun()

# --- Process PDF ---
if uploaded_file and not st.session_state.pdf_processed:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    with st.spinner("🔍 Processing PDF..."):
        docs = load_and_split_pdf("temp.pdf")
        st.session_state.chain = build_qa_chain(docs)
        st.session_state.pdf_processed = True
        st.success("✅ Core concepts extracted! You may now ask questions.")

# --- Chat UI ---
if st.session_state.chain and st.session_state.pdf_processed:
    # Display chat history
    for sender, message in st.session_state.chat_history:
        if sender == "user":
            st.markdown(f"**🧑‍💻 You:** {message}")
        else:
            st.markdown(f"**🤖 AI:** {message}")

    # Only show input when not processing
    if not st.session_state.processing:
        # Chat input area
        st.markdown("----")
        with st.form("chat_input", clear_on_submit=True):
            user_input = st.text_area(
                "Message",
                placeholder="Type your question and press Enter...",
                label_visibility="collapsed",
                height=100,
                key="chat_input"
            )
            submitted = st.form_submit_button("Send")

        # Process question when submitted
        if submitted and user_input:
            st.session_state.processing = True
            st.session_state.chat_history.append(("user", user_input))
            st.rerun()  # Changed from experimental_rerun()

    # Processing the question
    if st.session_state.processing:
        if st.session_state.chat_history and st.session_state.chat_history[-1][0] == "user":
            with st.spinner("🤖 Thinking..."):
                user_question = st.session_state.chat_history[-1][1]
                answer = st.session_state.chain.run(user_question)
                st.session_state.chat_history.append(("ai", answer))
                st.session_state.processing = False
                st.rerun()  # Changed from experimental_rerun()