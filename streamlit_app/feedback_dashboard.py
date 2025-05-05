import os
import sys
import streamlit as st
import pandas as pd
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from assistant.config import FEEDBACK_LOG

st.set_page_config(page_title="📈 Feedback Dashboard", layout="wide")

st.title("📊 Lab Assistant Feedback Dashboard")


# Load feedback logs
def load_feedback():
    entries = []
    try:
        with open(FEEDBACK_LOG, "r") as f:
            for line in f:
                entries.append(json.loads(line))
    except FileNotFoundError:
        st.warning("No feedback log found yet.")
    return pd.DataFrame(entries)


df = load_feedback()

# Convert timestamp to datetime for filtering
if not df.empty:
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

    # Filters
    with st.sidebar:
        st.header("🔍 Filters")

        # Feedback Type Filter
        feedback_type = st.multiselect("Feedback Type", options=df["feedback"].unique(),
                                       default=df["feedback"].unique())
        df = df[df["feedback"].isin(feedback_type)]

        # Comment Filter
        comment_filter = st.checkbox("Only show feedback with comments")
        if comment_filter:
            df = df[df["comment"].str.strip() != ""]

        # Time Range Filter
        st.subheader("Filter by Date Range")
        start_date = st.date_input("Start date", df["timestamp"].min().date())
        end_date = st.date_input("End date", df["timestamp"].max().date())
        df = df[(df["timestamp"].dt.date >= start_date) & (df["timestamp"].dt.date <= end_date)]

    # Show data
    st.dataframe(df[["timestamp", "feedback", "comment", "user_message", "assistant_response"]],
                 use_container_width=True)

    # Download button
    st.download_button("📥 Download as CSV", data=df.to_csv(index=False), file_name="feedback_export.csv",
                       mime="text/csv")
else:
    st.info("No feedback to show.")
