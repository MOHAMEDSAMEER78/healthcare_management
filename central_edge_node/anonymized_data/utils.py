import logging
from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework import status
from .models import PatientData, AnonymizedPatientData
from .serializers import AnonymizedPatientDataSerializer

logger = logging.getLogger(__name__)

def save_patient_data(data):
    try:
        logger.info(f"Saving patient data: {data}")
        
        # Create PatientData object from request data
        patient_data = PatientData(**data)
        logger.info(f"Patient data object: {patient_data}")
        
        # Convert the PatientData object to a dictionary
        patient_data_dict = model_to_dict(patient_data)
        logger.info(f"Patient data dictionary: {patient_data_dict}")
        
        # Filter out unknown fields for AnonymizedPatientData
        anonymized_data = {key: value for key, value in patient_data_dict.items() if key in [field.name for field in AnonymizedPatientData._meta.get_fields()]}
        
        # Create AnonymizedPatientData object with filtered data
        anonymized_patient_data = AnonymizedPatientData(**anonymized_data)
        logger.info(f"Anonymized patient data object: {anonymized_patient_data}")
        
        # Save the AnonymizedPatientData object
        anonymized_patient_data.save()
        
        # Serialize the AnonymizedPatientData object
        serialized_data = AnonymizedPatientDataSerializer(anonymized_patient_data).data
        
        return Response({"message": "Patient data saved successfully", "data": serialized_data}, status=status.HTTP_201_CREATED)
    except Exception as e:
        logger.error(f"Error saving patient data: {e}", exc_info=True)
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
