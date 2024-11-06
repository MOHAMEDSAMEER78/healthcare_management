# Ensure the database table for AnonymizedPatientData exists
# Run the following commands in your terminal to create and apply migrations

# python manage.py makemigrations anonymized_data
# python manage.py migrate anonymized_data

from anonymized_data.models import AnonymizedPatientData
from django.forms.models import model_to_dict
import logging
from django.core import serializers
import json

from .patient.models import PatientData
from .utils import save_patient_data

logger = logging.getLogger(__name__)

def process_patient_data(data):
    try:
        # Save patient data as anonymized data
        logger.info(f"Data received: {data}") 
        response = save_patient_data(data)
        return response.data
    except Exception as e:
        logger.error(f"Error in process_patient_data: {e}")
        raise
