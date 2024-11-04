from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable, KafkaConfigurationError, KafkaError
import json
from django.conf import settings
from anonymized_data.models import AnonymizedPatientData
from .serializers import AnonymizedPatientDataSerializer

import threading
import time
import logging
from django.forms.models import model_to_dict


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
                        logger.info(f"Received message: {data}")
                        anonymized_data_json = self.anonymize_data(data)
                        logger.info(f"Anonymized data final: {anonymized_data_json}")

                        logger.info(f"Anonymized data JSON: {anonymized_data_json}")

                        # Serialize the anonymized data
                        serializer = AnonymizedPatientDataSerializer(data=anonymized_data_json)
                        logger.info(f"Serializer: {serializer}")

                        # Check if the serialization is valid
                        if serializer.is_valid():
                            # Save the serialized data to the database
                            serializer.save()
                        else:
                            logger.error(f"Error serializing anonymized data: {serializer.errors}")
                        logger.info(f"Data received from Kafka: {data}")
                    except Exception as e:
                        logger.error(f"Error processing message: {e}")
            except ConnectionResetError as e:
                logger.error(f"Connection reset error: {e}")
                time.sleep(self.retry_interval)
                consumer = self._create_consumer()  # Recreate the consumer after connection reset
                logger.info("Reconnected to Kafka after connection reset")
            except KafkaError as e:
                logger.error(f"Kafka error: {e}")
                time.sleep(self.retry_interval)
            except Exception as e:
                logger.error(f"Consumer error: {e}")
                time.sleep(self.retry_interval)

        consumer.close()

    def anonymize_data(self, data):
        """
        Anonymize patient data by mapping fields and replacing identifiers
        """
        anonymized = {}
        logger.error(f"Starting data anonymization: {data}")
        
        # Anonymize sensitive fields
        anonymized['patient_original_data_id'] = int(data.get('id', ''))
        anonymized['age'] = int(data.get('age', 0))
        anonymized['blood_pressure'] = str(data.get('blood_pressure', "120/80"))
        anonymized['temperature'] = float(data.get('temperature', 0.0))
        anonymized['glucose_level'] = float(data.get('glucose_level', 0.0))
        anonymized['heartrate'] = int(data.get('heartrate', 0))
        anonymized['oxygen_level'] = float(data.get('oxygen_level', 0.0))
        anonymized['edge_device_name'] = 'Edge Device 1'
        anonymized['name'] = 'Anonymous'
        anonymized['date'] = (data.get('date', ''))
        anonymized['time'] = (data.get('time', ''))

        logger.error(f"Anonymized data: {anonymized}")
        return anonymized
