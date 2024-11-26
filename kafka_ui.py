import streamlit as st
import requests

API_SERVER = "http://localhost:5000"
HARD_CODED_TOPIC = "elv_json"  # Hardcoded topic for demo purposes

st.title("Kafka Message Viewer")
st.header(f"Topic: {HARD_CODED_TOPIC}")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Start consuming messages from the topic (only once)
if "started_consuming" not in st.session_state:
    response = requests.post(f"{API_SERVER}/consume", json={"topic": HARD_CODED_TOPIC})
    if response.status_code == 200:
        st.session_state.started_consuming = True
        st.success(f"Started consuming topic: {HARD_CODED_TOPIC}")

# Display chat-like message history
st.subheader("Message History")
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

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

# Refresh and fetch new messages
if st.button("Refresh Messages"):
    response = requests.get(f"{API_SERVER}/messages", params={"topic": HARD_CODED_TOPIC})
    if response.status_code == 200:
        data = response.json()
        messages = data.get("messages", [])
        for message in messages:
            # Assuming the response has encrypted messages, decrypt before displaying
            decrypted_message = decrypt_message(message, ENCRYPTION_KEY)
            # Add new messages to chat history
            if {"role": "user", "content": message} not in st.session_state.chat_history:
                st.session_state.chat_history.append({"role": "user", "content": message})
    else:
        st.error("Failed to fetch messages from API.")




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
