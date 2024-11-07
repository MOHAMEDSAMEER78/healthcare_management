# Ensure the database table for AnonymizedPatientData exists
# Run the following commands in your terminal to create and apply migrations

# python manage.py makemigrations anonymized_data
# python manage.py migrate anonymized_data

import logging

from .utils import save_patient_data

logger = logging.getLogger(__name__)

def process_patient_data(data):
    try:
        # Save patient data as anonymized data
        logger.info(f"Data received: {data}") 
        return save_patient_data(data)
    except Exception as e:
        logger.error(f"Error in process_patient_data: {e}")
        raise
