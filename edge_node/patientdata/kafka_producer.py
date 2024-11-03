from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
import json
import time
from django.conf import settings

class PatientDataProducer:
    def __init__(self, max_retries=2, retry_interval=1):
        self.max_retries = max_retries
        self.retry_interval = retry_interval
        self.producer = None
        self.topic = 'patient_data'
        self._connect()

    def _connect(self):
        retries = 0
        bootstrap_servers = ['localhost:9092']
        
        while retries < self.max_retries:
            try:
                self.producer = KafkaProducer(
                    bootstrap_servers=bootstrap_servers,
                    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                    api_version=(0, 10, 1),
                    retries=3,
                    retry_backoff_ms=1000,
                    request_timeout_ms=30000
                )
                print(f"Successfully connected to Kafka at {bootstrap_servers}")
                return
            except NoBrokersAvailable:
                retries += 1
                if retries < self.max_retries:
                    print(f"Failed to connect to Kafka. Retrying in {self.retry_interval} seconds...")
                    time.sleep(self.retry_interval)
                else:
                    print("Max retries reached. Could not connect to Kafka")
                    raise

    def send_patient_data(self, data):
        if not self.producer:
            try:
                print("Reconnecting to Kafka...")
                self._connect()
            except Exception as e:
                print(f"Failed to reconnect to Kafka: {e}")
                return False

        try:
            print(f"Sending message to Kafka: {data}")
            future = self.producer.send(self.topic, data)
            future.get(timeout=10)  # Wait for send to complete
            print("Message sent successfully")
            return True
        except Exception as e:
            print(f"Error sending message to Kafka: {e}")
            return False
