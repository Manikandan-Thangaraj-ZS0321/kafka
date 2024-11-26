docker exec -it kafka bash
kafka-topics --create --topic elv_json --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
kafka-topics --list --bootstrap-server localhost:9092
kafka-console-producer --topic elv_json --bootstrap-server localhost:9092
kafka-console-consumer --topic elv_json --from-beginning --bootstrap-server localhost:9092