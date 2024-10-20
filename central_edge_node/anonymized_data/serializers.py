# anonymized_data/serializers.py

from rest_framework import serializers
from .models import AnonymizedPatientData

class AnonymizedPatientDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnonymizedPatientData
        fields = '__all__'
