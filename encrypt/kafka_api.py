from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from kafka import KafkaProducer, KafkaConsumer
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad
import json
import base64
from typing import Optional
import uvicorn  # Import uvicorn for programmatic execution

app = FastAPI()

KAFKA_SERVER = "172.20.0.25:9092"
KAFKA_USERNAME = "anthem-elevance@intics.ai"  # Replace with your Kafka SASL username
KAFKA_PASSWORD = "Password@1"  # Replace with your Kafka SASL password

# AES Encryption Key (This should be kept secret and the same as used by producer)
ENCRYPTION_KEY = "RgF7I3z5FC8k9HkKUm3Htb1HhZPBczdksVr9fqGbTwc="  # AES-256 Key (32 bytes)

# Kafka Producer with SASL/PLAIN Authentication
producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    security_protocol="SASL_SSL",
    sasl_mechanism="PLAIN",
    sasl_plain_username=KAFKA_USERNAME,
    sasl_plain_password=KAFKA_PASSWORD,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Kafka Consumer with SASL/PLAIN Authentication
def consume_messages(topic: str):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=KAFKA_SERVER,
        security_protocol="SASL_SSL",
        sasl_mechanism="PLAIN",
        sasl_plain_username=KAFKA_USERNAME,
        sasl_plain_password=KAFKA_PASSWORD,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    for message in consumer:
        if topic not in messages_by_topic:
            messages_by_topic[topic] = []
        # Decrypt message before storing it
        decrypted_message = decrypt_message(message.value)
        messages_by_topic[topic].append(decrypted_message)

# Dictionary to store messages for each topic
messages_by_topic = {}

# AES Encryption Function (for producer side)
def encrypt_message(message, encryption_key):
    # Ensure the key is 32 bytes (AES-256)
    key = encryption_key.encode('utf-8')
    # Generate a random IV
    cipher = AES.new(key, AES.MODE_CBC)
    # Pad the message to be a multiple of the AES block size
    ct_bytes = cipher.encrypt(pad(message.encode('utf-8'), AES.block_size))
    # Get the IV used for encryption
    iv = cipher.iv
    # Combine IV and ciphertext and encode as base64 to store/transmit
    encrypted_message = base64.b64encode(iv + ct_bytes).decode('utf-8')

    return encrypted_message

# AES Decryption Function (for consumer side)
def decrypt_message(encrypted_message):
    # Decode the base64 encoded encrypted message
    encrypted_data = base64.b64decode(encrypted_message)
    # Create AES cipher object using ECB mode
    cipher = AES.new(ENCRYPTION_KEY.encode('utf-8'), AES.MODE_ECB)
    # Decrypt the data and unpad it
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    # Return the decrypted message as a string
    return decrypted_data.decode('utf-8')

# Pydantic model for request body validation
class PublishMessageRequest(BaseModel):
    topic: str
    message: str

class ConsumeMessageRequest(BaseModel):
    topic: str

# API to publish messages to a specific Kafka topic (with AES encryption)
@app.post("/publish")
async def publish_message(request: PublishMessageRequest):
    topic = request.topic
    message = request.message

    # Encrypt the message before sending to Kafka
    encrypted_message = encrypt_message(message, ENCRYPTION_KEY)

    # Send encrypted message to Kafka
    producer.send(topic, value=encrypted_message)
    producer.flush()

    return {"message": "Message published", "topic": topic, "data": encrypted_message}

# API to start consuming a specific topic
@app.post("/consume")
async def start_consuming(request: ConsumeMessageRequest, background_tasks: BackgroundTasks):
    topic = request.topic

    if topic not in messages_by_topic:
        background_tasks.add_task(consume_messages, topic)

    return {"message": f"Started consuming topic: {topic}"}

# API to get consumed messages for a specific topic
@app.get("/messages")
async def get_messages(topic: Optional[str] = None):
    if not topic:
        raise HTTPException(status_code=400, detail="Topic name is required")

    topic_messages = messages_by_topic.get(topic, [])
    return {"topic": topic, "messages": topic_messages}

# Run the FastAPI application programmatically using uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)