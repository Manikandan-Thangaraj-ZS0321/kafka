
```markdown
# Run Notify App

## Notify API:
To run the Notify API, use the following command:
```bash
python notify_api.py
```

## Notify App:
To run the Notify App using Streamlit, use the following command:
```bash
streamlit run notify_ui.py
```

---

# Run Kafka Server

## Kafka API:
To run the Kafka API, use the following command:
```bash
python kafka_test.py
```

## Kafka App:
To run the Kafka App using Streamlit, use the following command:
```bash
streamlit run kafka_ui.py
```

docker exec -it kafka bash
kafka-topics --create --topic elv_json --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
kafka-topics --list --bootstrap-server localhost:9092
kafka-console-producer --topic elv_json --bootstrap-server localhost:9092
kafka-console-consumer --topic elv_json --from-beginning --bootstrap-server localhost:9092