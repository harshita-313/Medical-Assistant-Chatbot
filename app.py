import streamlit as st
from chatbot import get_answer

st.set_page_config ("Medical Chatbot")
st.title("🩺 Your Medical Assistant!")

# Save conversation state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display old messages
for role, content in st.session_state.chat_history:
    with st.chat_message(role):
        st.write(content)

# User input
if user_query := st.chat_input("Write your query..."):
    # Save & display user message
    st.session_state.chat_history.append(("user", user_query))
    with st.chat_message("user"):
        st.write(user_query)

    # Get assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = get_answer(user_query)
            st.write(answer)

    # Save response
    st.session_state.chat_history.append(("assistant", answer))
