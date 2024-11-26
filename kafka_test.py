from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from confluent_kafka import Producer, Consumer, KafkaException, KafkaError
import uvicorn

app = FastAPI()

# Kafka Configuration
KAFKA_BROKER = "localhost:9092"  # Replace with your Kafka broker address
KAFKA_TOPIC = "elv_json"
KAFKA_USERNAME = "anthem-elevance@intics.ai"  # Replace with your Kafka username
KAFKA_PASSWORD = "Password@1"  # Replace with your Kafka password

# SASL Configuration
KAFKA_SASL_CONFIG = {
    "bootstrap.servers": KAFKA_BROKER,
    "security.protocol": "SASL_PLAINTEXT",  # SASL over plaintext
    "sasl.mechanism": "PLAIN",  # SASL mechanism
    "sasl.username": KAFKA_USERNAME,
    "sasl.password": KAFKA_PASSWORD,
}

# Kafka Producer
producer = Producer(KAFKA_SASL_CONFIG)


# Kafka Consumer
def create_consumer():
    return Consumer({
        **KAFKA_SASL_CONFIG,  # Include SASL configuration
        "group.id": "fastapi-group",
        "auto.offset.reset": "earliest"
    })


# Request Body for Producing Messages
class Message(BaseModel):
    key: str
    value: str


@app.post("/produce")
async def produce_message(message: Message):
    """
    Produce a message to Kafka.
    """
    try:
        producer.produce(
            KAFKA_TOPIC, key=message.key, value=message.value
        )
        producer.flush()  # Ensure the message is delivered
        return {"status": "success", "message": "Message produced successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to produce message: {str(e)}")


@app.get("/consume")
async def consume_message():
    """
    Consume messages from Kafka.
    """
    consumer = create_consumer()
    consumer.subscribe([KAFKA_TOPIC])

    try:
        msg = consumer.poll(timeout=5.0)  # Poll for a message
        if msg is None:
            return {"status": "success", "message": "No messages available"}
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                return {"status": "success", "message": "End of partition reached"}
            else:
                raise KafkaException(msg.error())

        message = {
            "key": msg.key().decode("utf-8") if msg.key() else None,
            "value": msg.value().decode("utf-8"),
        }
        return {"status": "success", "message": message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to consume message: {str(e)}")
    finally:
        consumer.close()


@app.get("/")
def root():
    return {"message": "Kafka API is running"}


# Run the FastAPI application programmatically using uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)