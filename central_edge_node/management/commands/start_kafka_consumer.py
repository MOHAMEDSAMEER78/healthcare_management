from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Launches Listener for patient_data messages from Kafka'

    def handle(self, *args, **options):
        from anonymized_data.kafka_consumer import PatientDataConsumer
        listener = PatientDataConsumer()
        listener.start()
        self.stdout.write(self.style.SUCCESS('Started Kafka Consumer Thread'))