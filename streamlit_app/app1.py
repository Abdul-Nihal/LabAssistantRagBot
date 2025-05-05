import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from assistant.feedback import store_feedback
#
# import streamlit as st
# from assistant.assistant import LabAssistant
# from assistant.models import AssistantType
# from assistant.logger import logger
#
# st.set_page_config(page_title="🧪 Lab Assistant", layout="wide")
#
# # Init session state
# if "lab_assistant" not in st.session_state:
#     st.session_state.lab_assistant = LabAssistant(AssistantType.WaterCementConc)
#
# if "thread_id" not in st.session_state:
#     st.session_state.thread_id = None
#
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
#
# st.title("🤖 Lab Assistant Chat")
#
# # Upload fixed PDF
# uploaded_file = "Cementing.pdf"
#
# # Thread creation
# if st.button("📁 Start New Thread"):
#     with st.spinner("Creating assistant thread and loading file..."):
#         try:
#             st.session_state.thread_id = st.session_state.lab_assistant.load_or_create_thread(uploaded_file)
#             st.session_state.chat_history = []
#             st.success("Assistant is ready to chat!")
#         except Exception as e:
#             logger.error(f"Failed to create thread: {e}")
#             st.error("❌ Failed to initialize assistant. Please check logs.")
#
# # Show chat only if thread is created
# if st.session_state.thread_id:
#     st.markdown("---")
#     st.markdown("### 💬 Chat")
#
#     chat_container = st.container()
#     with chat_container:
#         for i, (user_msg, assistant_msg) in enumerate(st.session_state.chat_history, 1):
#             st.chat_message("user").markdown(user_msg)
#             st.chat_message("assistant").markdown(assistant_msg)
#
#     user_input = st.chat_input("Ask something about the cementing report...")
#     if user_input:
#         with st.spinner("Assistant is thinking..."):
#             try:
#                 st.session_state.lab_assistant.add_message_to_thread(
#                     st.session_state.thread_id, user_input
#                 )
#                 st.session_state.lab_assistant.run_thread(st.session_state.thread_id)
#                 response,message_id = st.session_state.lab_assistant.get_run_output(st.session_state.thread_id)
#
#                 if response:
#                     st.session_state.chat_history.append((user_input, response))
#                     st.chat_message("user").markdown(user_input)
#                     st.chat_message("assistant").markdown(response)
#                 else:
#                     st.error("❌ Assistant failed to respond. Please try after 1 Minute.")
#             except Exception as e:
#                 logger.error(f"Error during assistant interaction: {e}")
#                 st.error("❌ Unexpected error occurred. Check logs.")


