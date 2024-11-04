from django.apps import AppConfig

class AnonymizedDataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'anonymized_data'

    def ready(self):
        from .kafka_consumer import PatientDataConsumer
        consumer = PatientDataConsumer()
        consumer.start()
