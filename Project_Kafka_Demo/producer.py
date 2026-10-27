from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers="localhost:9092")

for i in range(1, 10):
    producer.send("orders", key=str(i).encode(), value=f"order {i}".encode())

producer.flush()
print("sent 9 orders")