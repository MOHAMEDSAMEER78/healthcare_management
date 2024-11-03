from kafka import KafkaAdminClient, KafkaConsumer
from kafka.admin import NewTopic
import json

def consume_kafka():
    from .serializers import AnonymizedPatientDataSerializer

    # Your Kafka consumer code here
    print('Consuming Kafka messages')
    admin_client = KafkaAdminClient(
        bootstrap_servers='kafka:9092',
        client_id='healthcare_management_admin'
    )

    topic_list = [NewTopic(name='patient_data', num_partitions=1, replication_factor=1)]
    try:
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
        print('Kafka topics created')
    except Exception as e:
        print(f"Error creating topics: {e}")

    consumer = KafkaConsumer(
        'patient_data',
        bootstrap_servers='kafka:9092',
        auto_offset_reset='earliest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    for message in consumer:
        data = message.value
        serializer = AnonymizedPatientDataSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            print(f"Invalid data: {serializer.errors}")