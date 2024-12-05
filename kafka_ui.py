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

# Display current message history
st.subheader("Message History")
for msg in st.session_state.chat_history:
    st.write(f"{msg['role']}: {msg['content']}")

# Refresh button
if st.button("Refresh Messages"):
    try:
        # Call the FastAPI endpoint
        response = requests.get(f"{API_SERVER}/consume")
        if response.status_code == 200:
            data = response.json()
            messages = data.get("messages", [])

            # Append new messages
            for message in messages:
                st.write(json.loads(message))

        else:
            st.error(f"Failed to fetch messages. Status code: {response.status_code}")
    except Exception as e:
        st.error(f"Error fetching messages: {e}")



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

# Send a message
#st.subheader("Send a Message")
#user_message = st.text_input("Enter your message", key="message_input")
#if st.button("Send Message"):
#    if user_message:
#        response = requests.post(
#            f"{API_SERVER}/publish",
#            json={"topic": HARD_CODED_TOPIC, "message": user_message},
#        )
#        if response.status_code == 200:
#            st.session_state.chat_history.append({"role": "user", "content": user_message})
#            st.success("Message sent!")
#        else:
#            st.error("Failed to send the message.")
