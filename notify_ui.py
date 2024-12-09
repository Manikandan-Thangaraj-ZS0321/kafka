import json

import streamlit as st
import requests
import pandas as pd

# URL of the API endpoint to fetch messages
API_URL = "http://localhost:5001/messages"  # Replace with your actual endpoint


# Function to get messages from the API
def fetch_messages():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            return response.json()  # Assuming the API returns a JSON response
        else:
            return {"error": f"Failed to fetch messages. Status code: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}


# Streamlit UI
st.title("Outbound Notification Messages")

# Initialize session state for storing messages
if "messages" not in st.session_state:
    st.session_state.messages = []


# Function to fetch and display messages from the API
def load_and_display_messages():
    # Fetch the new messages from the API
    messages = fetch_messages()

    if isinstance(messages, dict) and "error" in messages:
        st.error(messages["error"])
    else:
        for msg in messages:
            transaction_id = msg.get("transactionId", "Unknown Transaction ID")
            st.subheader(f"The outbound JSON for the transaction ID: {transaction_id}")
            msg["extractionResponse"] = json.loads(msg.get("extractionResponse"))
            st.json(msg)


# Refresh Button to fetch the latest messages
if st.button("Refresh Messages"):
    load_and_display_messages()  # Fetch all messages from the API
