# Notify App

## Notify API
To run the Notify API, use the following command:
```bash
python notify_api.py
```

## Notify App
To run the Notify App using Streamlit, use the following command:
```bash
streamlit run notify_ui.py
```

---

## Using Kafka Producer and Consumer Without Authentication

### 1. Start Kafka and Zookeeper without authentication
Start the Kafka and Zookeeper Docker Compose without authentication:
```bash
docker compose -f zk-single-kafka-single-no_auth.yml up -d
```

### 2. Access the Kafka container
To navigate inside the Kafka Docker container:
```bash
docker exec -it kafka bash
```

### 3. Create a Topic
Create a Kafka topic named `elv_json`:
```bash
kafka-topics --create --topic elv_json --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

### 4. Run the FastAPI endpoint
Run the FastAPI endpoint:
```bash
python kafka_no_auth.py
```

### 5. Kafka UI App
To run the Kafka UI App using Streamlit, use the following command:
```bash
streamlit run kafka_ui.py
```

### Other Commands

#### Listing Topics
To list all Kafka topics:
```bash
kafka-topics --list --bootstrap-server localhost:9092
```

#### Publishing a Message to Producer
To publish a message to the producer:
```bash
kafka-console-producer --topic elv_json --bootstrap-server localhost:9092
```

#### Reading Messages from Consumer
To read messages from the consumer:
```bash
kafka-console-consumer --topic elv_json --from-beginning --bootstrap-server localhost:9092
```

---

## Using Kafka Producer and Consumer With Authentication

### 1. Start Kafka and Zookeeper with authentication
Start the Kafka and Zookeeper Docker Compose with authentication:
```bash
docker compose -f zk-single-kafka-single-auth.yml up -d
```

### 2. Access the Kafka container
To navigate inside the Kafka Docker container:
```bash
docker exec -it kafka bash
```

### 3. Create a Topic with Authentication
Create a Kafka topic named `elv_json` with authentication:
```bash
kafka-topics.sh --bootstrap-server localhost:9092 --topic elv_json --create --partitions 1 --replication-factor 1 --command-config client.properties
```

### 4. Run the FastAPI endpoint
Run the FastAPI endpoint:
```bash
python kafka_auth.py
```

### 5. Kafka UI App
To run the Kafka UI App using Streamlit, use the following command:
```bash
streamlit run kafka_ui.py
```

### Other Commands

#### Listing Topics with Authentication
To list all Kafka topics with authentication:
```bash
kafka-topics.sh --list --bootstrap-server localhost:9092 --command-config client.properties
```

#### Publishing a Message to Producer with Authentication
To publish a message to the producer with authentication:
```bash
kafka-console-producer.sh --bootstrap-server localhost:9092 --topic elv_json --consumer.config client.properties
```

#### Reading Messages from Consumer with Authentication
To read messages from the consumer with authentication:
```bash
kafka-console-consumer.sh --topic elv_json --bootstrap-server localhost:9092 --consumer.config client.properties --max-messages 1
```