import logging
from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework import status

from central_edge_node.anonymized_data.anonymizer import protect_identity
from .models import AnonymizedPatientData
from .serializers import AnonymizedPatientDataSerializer

logger = logging.getLogger(__name__)

def save_patient_data(data):
    try:
        logger.info(f"Saving patient data: {data}")

        anonymized_patient_data = AnonymizedPatientData(**data)
        dictx = model_to_dict(anonymized_patient_data)
        dictx['patient_original_data_id'] = data['id']
        dictx = anonymize_data(dictx)
        logger.info("Anonymized patient data object: {}".format(dictx))

        serializer = AnonymizedPatientDataSerializer(data=dictx)
        if serializer.is_valid():
            serializer.save()
            logger.info("Valid Serialiser Saving patient data {} ".format(serializer.data))

        else:
            logger.error("Error saving patient data: {}".format(serializer.errors))
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        logger.info("Unformatted Anonymized patient data object: {}".format(serializer))        

        return Response({"message": "Patient data saved successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    except Exception as e:
        logger.error(f"Error saving patient data: {e}", exc_info=True)
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

def anonymize_data(data):
    # Anonymize data here
    data['name'] = "Anonymized "+ protect_identity(data['name'])
    return data