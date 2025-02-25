from kafka import KafkaProducer, KafkaConsumer
import json

def test_kafka_producer_consumer():
    producer = KafkaProducer(bootstrap_servers="kafka:9092", value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    consumer = KafkaConsumer("test_topic", bootstrap_servers="kafka:9092", value_deserializer=lambda x: json.loads(x.decode('utf-8')))

    producer.send("test_topic", {"message": "test"})
    producer.flush()

    for msg in consumer:
        assert msg.value == {"message": "test"}
        break