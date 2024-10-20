# anonymized_data/views.py

from rest_framework import viewsets, permissions
from .models import AnonymizedPatientData
from .serializers import AnonymizedPatientDataSerializer

class AnonymizedPatientDataViewSet(viewsets.ModelViewSet):
    queryset = AnonymizedPatientData.objects.all()
    serializer_class = AnonymizedPatientDataSerializer