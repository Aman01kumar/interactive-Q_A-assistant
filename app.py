import streamlit as st
import os
from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.environ["GOOGLE_API_KEY"]
ai_client = genai.Client(api_key=api_key)


st.set_page_config(page_title="Interactive Q&A Assistant")
st.title("Interactive Q&A Assistant")
st.caption("Ask questions and get clear answers")


if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []


question_text = st.text_input("Enter your question:")


if st.button("Ask Question") and question_text.strip():


    st.session_state.conversation_history.append(
        f"User: {question_text}"
    )


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


    st.session_state.conversation_history.append(
        f"Assistant: {answer_text}"
    )


    st.subheader("Answer")
    st.write(answer_text)
