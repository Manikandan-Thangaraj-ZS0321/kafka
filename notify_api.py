from fastapi import FastAPI
from Crypto.Cipher import AES
from pydantic import BaseModel
from Crypto.Util.Padding import unpad
import base64
import json
import uvicorn

app = FastAPI()

# Simulating a message store (in-memory, could be replaced by a database)
messages = []
ENCRYPTION_KEY = "RgF7I3z5FC8k9HkKUm3Htb1HhZPBczdk"


# Endpoint to retrieve messages
@app.get('/messages')
def get_messages():
    json_messages = [json.loads(message) for message in reversed(messages)]
    return json_messages


class NotifyRequest(BaseModel):
    documentId: str
    checksum: str
    transactionId: str
    extractionResponse: str
     # Added the new field


# Endpoint to send a message to the API
@app.post('/messages')
def post_message(request: NotifyRequest):
    if request.documentId:
        # Decrypt message
        decrypted_message = decrypt_message(request.extractionResponse)
        # Store the user's message with the new transactionId field
        request.extractionResponse = json.loads(decrypted_message)
        messages.append(json.dumps(request.model_dump()))  # Use `dict()` instead of `model_dump()` if not available
        print("Received the input")
        return {"status": "Message received"}
    else:
        return {"error": "No message provided"}


def decrypt_message(encrypted_message):
    # Decode the base64 encoded encrypted message
    encrypted_data = base64.b64decode(encrypted_message)
    # Create AES cipher object using ECB mode
    cipher = AES.new(ENCRYPTION_KEY.encode('utf-8'), AES.MODE_ECB)
    # Decrypt the data and unpad it
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    print("Decrypted successfully")

    # Return the decrypted message as a string
    return decrypted_data.decode('utf-8')


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)
