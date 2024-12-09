import json
import streamlit as st
import requests

API_SERVER = "http://localhost:5000"
HARD_CODED_TOPIC = "elv_json"  # Kafka topic

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # List to store messages
    st.session_state.seen_messages = set()  # Set for deduplication

# Streamlit UI
st.title("Kafka Message Viewer")
st.header(f"Topic: {HARD_CODED_TOPIC}")

# Refresh button
if st.button("Refresh Messages"):
    try:
        # Call the FastAPI endpoint
        response = requests.get(f"{API_SERVER}/consume")
        if response.status_code == 200:
            data = response.json()
            messages = data.get("messages", [])

            # Prepend new messages to chat history
            for message in messages:
                transaction_json = json.loads(message)  # Parse the JSON message

                # Check for duplicates using a set
                if message not in st.session_state.seen_messages:
                    st.session_state.chat_history.insert(0, transaction_json)  # Add to the beginning
                    st.session_state.seen_messages.add(message)  # Mark as seen

        else:
            st.error(f"Failed to fetch messages. Status code: {response.status_code}")
    except Exception as e:
        st.error(f"Error fetching messages: {e}")

# Display the current chat history as JSON nodes
for transaction in st.session_state.chat_history:
    transaction_id = transaction.get("transactionId", "Unknown ID")
    st.subheader(f"The outbound JSON for the transaction ID: {transaction_id}")
    st.json(transaction)  # Display each transaction as a JSON node

# Function to decrypt AES encrypted messages
def decrypt_message(encrypted_message, encryption_key):
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import unpad
    import base64

    # Decode the encrypted message from base64
    encrypted_data = base64.b64decode(encrypted_message)

    # Initialize AES cipher with the key
    cipher = AES.new(encryption_key.encode('utf-8'), AES.MODE_CBC, iv=encrypted_data[:16])
    decrypted_data = unpad(cipher.decrypt(encrypted_data[16:]), AES.block_size)

    # Convert decrypted bytes back to string
    return decrypted_data.decode('utf-8')
