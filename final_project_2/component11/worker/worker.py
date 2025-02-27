from kafka import KafkaConsumer
import json

def main():
    consumer = KafkaConsumer(
        'test_topic',
        bootstrap_servers='kafka:9092',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    for message in consumer:
        print(f"Received message: {message.value}")

if __name__ == "__main__":
    main()