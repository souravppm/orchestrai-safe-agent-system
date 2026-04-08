import os
import streamlit as st
import requests

# Docker এর ভেতরে চললে Docker-এর সার্ভিস নাম নেবে, না হলে লোকালহোস্ট
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="OrchestrAI Dashboard", page_icon="🚀", layout="centered")

st.title("🚀 OrchestrAI")
st.caption("A Safe Agent System for Enterprise Operations")

# Initialize chat history and state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_action" not in st.session_state:
    st.session_state.pending_action = None

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("E.g., Cancel my order 1"):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare payload
    payload = {"query": prompt, "session_id": "ui_session"}
    if st.session_state.pending_action:
        payload["pending_action"] = st.session_state.pending_action

    # Call FastAPI Backend
    with st.spinner("Agent is thinking..."):
        try:
            response = requests.post(f"{API_URL}/chat", json=payload).json()
            
            with st.chat_message("assistant"):
                status = response.get("status")
                
                # Handle Confirmation Workflow
                if status == "confirmation_required":
                    st.warning("⚠️ Action Requires Confirmation!")
                    msg = response.get("message")
                    st.markdown(f"**{msg}**\n*(Type 'yes' to confirm or 'no' to abort)*")
                    
                    st.session_state.pending_action = response.get("pending_action")
                    st.session_state.messages.append({"role": "assistant", "content": f"⚠️ {msg} (Type 'yes' to confirm)"})
                
                # Handle Success Actions
                elif status == "success":
                    st.success("✅ Action Executed Safely!")
                    msg = response.get("result", {}).get("message", "Operation completed.")
                    st.markdown(msg)
                    
                    st.session_state.pending_action = None
                    st.session_state.messages.append({"role": "assistant", "content": msg})
                
                # Handle Normal Chat/Errors
                else:
                    msg = response.get("message", "Sorry, something went wrong.")
                    st.info(msg)
                    st.session_state.pending_action = None
                    st.session_state.messages.append({"role": "assistant", "content": msg})
                    
        except requests.exceptions.ConnectionError:
            st.error("🚨 Backend server is not running! Please start the FastAPI server.")
