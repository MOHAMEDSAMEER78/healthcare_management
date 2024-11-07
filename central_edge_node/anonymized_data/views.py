# anonymized_data/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import AnonymizedPatientData
from .serializers import AnonymizedPatientDataSerializer
from .services import process_patient_data
from .utils import save_patient_data

class AnonymizedPatientDataViewSet(viewsets.ModelViewSet):
    queryset = AnonymizedPatientData.objects.all()
    serializer_class = AnonymizedPatientDataSerializer

    @action(detail=False, methods=['post'])
    def process_data(self, request):
        try:
            response = process_patient_data(request.data)
            return Response({"message": "Data processed successfully", "data": response}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def save_patient_data(self, request):
        return save_patient_data(request.data)
