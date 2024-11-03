from django.apps import AppConfig
from .kafka_consumer import consume_kafka

class AnonymizedDataConfig(AppConfig):
    name = 'anonymized_data'

    def ready(self):
        from .kafka_consumer import consume_kafka
        consume_kafka()