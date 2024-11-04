from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable,KafkaConfigurationError
import json
from django.conf import settings
from .models import AnonymizedPatientData
import threading
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # This ensures logs go to stdout
    ]
)

# Set up logger
logger = logging.getLogger(__name__)

class PatientDataConsumer(threading.Thread):
    print("Starting PatientDataConsumer")
    def __init__(self, max_retries=2, retry_interval=1):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.max_retries = max_retries
        self.retry_interval = retry_interval

    def stop(self):
        self.stop_event.set()

    def _create_consumer(self):
        retries = 0
        while retries < self.max_retries:
            try:
                logger.info("Connecting to Kafka...")
                return KafkaConsumer(
                    'patient_data',
                    bootstrap_servers=['kafka:9092'],
                    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                    group_id='central_node_group',
                    api_version=(0, 10, 1),
                    session_timeout_ms=45000,          # Session timeout
                    heartbeat_interval_ms=14000,       # Less than session_timeout_ms/3
                    request_timeout_ms=60000,          # Larger than session_timeout_ms
                    fetch_max_wait_ms=500,
                    connections_max_idle_ms=600000,
                    auto_offset_reset='earliest'
                )
            except NoBrokersAvailable:
                logger.error("Failed to create consumer: NoBrokersAvailable")
                retries += 1
                time.sleep(self.retry_interval)
        raise KafkaConfigurationError("Failed to create Kafka consumer after retries")

    def run(self):
        try:
            logger.info("Starting Kafka consumer...")
            consumer = self._create_consumer()
        except Exception as e:
            logger.error(f"Failed to create consumer: {e}")
            return

        while not self.stop_event.is_set():
            try:
                for message in consumer:
                    try:
                        data = message.value
                        print(data)
                        logger.info(f"Received message: {data}")
                        anonymized_data = self.anonymize_data(data)
                        AnonymizedPatientData.objects.create(**anonymized_data)
                    except Exception as e:
                        logger.error(f"Error processing message: {e}")
            except Exception as e:
                logger.error(f"Consumer error: {e}")
                time.sleep(self.retry_interval)

        consumer.close()

    def anonymize_data(self, data):
        """
        Anonymize patient data by mapping fields and replacing identifiers
        """
        anonymized = {}
        anonymized['patient_original_data_id'] = str(data.get('id', ''))
        anonymized['edge_device_name'] = 'Edge Device 1'
        print("anonymized data : ",anonymized)
        
        # Map and anonymize other fields
        field_mapping = {
            'id': 'patient_original_data_id',  # Map id to patient_original_data_id
            'name': 'name',
            'age': 'age',
            'heart_rate': 'heart_rate',
            'blood_pressure': 'blood_pressure',
            'temperature': 'temperature',
            'oxygen_level': 'oxygen_level',
            'timestamp': 'timestamp',
            'date': 'date',
            'time': 'time'
        }
        
        # Copy non-sensitive data fields
        for source, target in field_mapping.items():
            if source in data:
                anonymized[target] = data[source]
                
      
        return anonymized
