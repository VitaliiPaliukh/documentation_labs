"""Small helper to consume a few messages from Kafka topic used by Lab4."""
import sys
import json

try:
    from kafka import KafkaConsumer
except ImportError:
    print("Please install kafka-python: pip install kafka-python")
    sys.exit(1)

bootstrap = ["localhost:9092"]
if len(sys.argv) > 1:
    topic = sys.argv[1]
else:
    topic = "lab4.fire-prevention-inspections"

consumer = KafkaConsumer(
    topic,
    bootstrap_servers=bootstrap,
    auto_offset_reset='earliest',
    enable_auto_commit=False,
    consumer_timeout_ms=5000,
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

count = 0
for msg in consumer:
    print(msg.value)
    count += 1
    if count >= 10:
        break

print(f"Read {count} messages from topic {topic}")
consumer.close()

