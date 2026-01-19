import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

# --------------------------------------------------
# Environment Setup
# --------------------------------------------------
load_dotenv()

api_key = os.environ["GOOGLE_API_KEY"]
ai_client = genai.Client(api_key=api_key)

# --------------------------------------------------
# Streamlit Page Configuration
# --------------------------------------------------
st.set_page_config(page_title="Interactive Q&A Assistant")
st.title("Interactive Q&A Assistant")
st.caption("Ask questions and get clear answers")

# --------------------------------------------------
# Session State Initialization
# --------------------------------------------------
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# --------------------------------------------------
# User Input
# --------------------------------------------------
question_text = st.text_input("Enter your question:")

# --------------------------------------------------
# Handle Question Submission
# --------------------------------------------------
if st.button("Ask Question") and question_text.strip():

    # Store user question
    st.session_state.conversation_history.append(
        f"User: {question_text}"
    )

    # Build conversation context
    conversation_prompt = (
        "\n".join(st.session_state.conversation_history)
        + "\nAssistant:"
    )

    # Generate answer using free-tier model
    response = ai_client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=conversation_prompt
    )

    answer_text = response.text.strip()

    # Store assistant response
    st.session_state.conversation_history.append(
        f"Assistant: {answer_text}"
    )

    # Display response
    st.subheader("Answer")
    st.write(answer_text)
