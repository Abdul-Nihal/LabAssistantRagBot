import base64
import sys
import os
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from assistant.feedback import log_feedback
from assistant.assistant import LabAssistant
from assistant.models import AssistantType
from assistant.logger import logger
from streamlit_feedback import streamlit_feedback

st.set_page_config(page_title="🧪 Lab Assistant", layout="wide")

# ------------------ Session State Initialization ------------------
if "lab_assistant" not in st.session_state:
    st.session_state.lab_assistant = LabAssistant(AssistantType.WaterCementConc)

if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "feedback_dict" not in st.session_state:
    st.session_state.feedback_dict = {}

if "last_response" not in st.session_state:
    st.session_state.last_response = None

if "last_message_id" not in st.session_state:
    st.session_state.last_message_id = None

# ------------------ UI ------------------

st.markdown("""
    <style>
        [data-testid="stApp"] {
            background-color: #e6f7ff;
            padding: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Load and encode the image
with open("logo.png", "rb") as image_file:
    encoded = base64.b64encode(image_file.read()).decode()

# Create HTML for inline image + title
html = f"""
    <div style="display: flex; align-items: center;">
        <img src="data:image/png;base64,{encoded}" width="100" height="30" style="margin-right: 10px;" />
        <h2 style="margin: 0;">Cementing Assistant</h2>
    </div>
"""


# Render it
st.markdown(html, unsafe_allow_html=True)



# Fixed input file
uploaded_file = "Cementing.pdf"

# Start New Thread Button
if st.button("💬 Start New Thread"):
    with st.spinner("Assistant is loading ..."):
        try:
            st.session_state.thread_id = st.session_state.lab_assistant.load_or_create_thread(uploaded_file)
            st.session_state.chat_history = []
            st.session_state.last_response = None
            st.session_state.last_message_id = None
            st.success("Assistant is ready to chat!")
        except Exception as e:
            logger.error(f"Failed to create thread: {e}")
            st.error("❌ Failed to initialize assistant. Please check logs.")

# ------------------ Chat Section ------------------
if st.session_state.thread_id:
    # st.markdown("---")
    # st.markdown("### 💬 Chat")

    # Show chat history
    for user_msg, assistant_msg, msg_id in st.session_state.chat_history:
        st.chat_message("user").markdown(user_msg)
        st.chat_message("assistant").markdown(assistant_msg)

    # Chat input from user
    user_input = st.chat_input("Ask anything about the cementing procedures...")
    if user_input:
        st.chat_message("user").markdown(user_input)
        with st.spinner("Assistant is thinking..."):
            try:
                st.session_state.lab_assistant.add_message_to_thread(
                    st.session_state.thread_id,
                    "Based on all the context I’ve provided above, answer the following question: " + user_input
                )
                st.session_state.lab_assistant.run_thread(st.session_state.thread_id)
                response, message_id = st.session_state.lab_assistant.get_run_output(st.session_state.thread_id)

                if response:
                    st.session_state.chat_history.append((user_input, response, message_id))
                    st.session_state.last_response = response
                    st.session_state.last_message_id = message_id
                    st.chat_message("assistant").markdown(response)
                else:
                    st.error("❌ Assistant failed to respond. Please try after 1 Minute.")
            except Exception as e:
                logger.error(f"Error during assistant interaction: {e}")
                st.error("❌ Unexpected error occurred. Check logs.")

# ------------------ Feedback Section ------------------
# Only show for the most recent message


# Only show for most recent message
if st.session_state.last_response and st.session_state.last_message_id:
    feedback = streamlit_feedback(
        feedback_type="thumbs",
        optional_text_label="[Optional] Explain your feedback",
        align="flex-start",
        key=f"feedback_{st.session_state.last_message_id}"
    )
    print(feedback)

    if feedback:
        st.toast("✔️ Feedback received!")
        entry = {
            "feedback": feedback["score"],
            "text": feedback.get("text", "")
        }
        st.session_state.feedback_dict[st.session_state.last_message_id] = entry

        # Find the user/assistant message pair
        for user_msg, assistant_msg, msg_id in reversed(st.session_state.chat_history):
            print(msg_id, st.session_state.last_message_id)
            if msg_id == st.session_state.last_message_id:
                log_feedback(msg_id, entry, user_msg, assistant_msg)
                break
