from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import PatientData
from .serializers import PatientDataSerializer
from .kafka_producer import PatientDataProducer
kafka_producer = PatientDataProducer()
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

@api_view(['GET', 'POST'])
def patient_data_list(request):
    if request.method == 'GET':
        patient_data = PatientData.objects.all()
        serializer = PatientDataSerializer(patient_data, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PatientDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Send to Kafka after saving
            logger.info(f"Sending data to Kafka: {request.data}")
            kafka_producer.send_patient_data(request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def patient_data_detail(request, pk):
    try:
        patient_data = PatientData.objects.get(pk=pk)
    except PatientData.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PatientDataSerializer(patient_data)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PatientDataSerializer(patient_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        patient_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
