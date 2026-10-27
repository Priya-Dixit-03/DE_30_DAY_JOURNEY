from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "orders",
    bootstrap_servers="localhost:9092",
    group_id="dashboard",
    auto_offset_reset="earliest",
    value_deserializer=lambda v: v.decode("utf-8"),
)

for msg in consumer:
    print(f"partition={msg.partition} offset={msg.offset} value={msg.value}")