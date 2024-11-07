# anonymized_data/models.py

from django.db import models

class AnonymizedPatientData(models.Model):
    id = models.AutoField(primary_key=True)
    patient_original_data_id = models.IntegerField(blank=True, null=True)
    edge_device_name = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100, default='Anonymous')
    age = models.IntegerField(blank=True, null=True)
    heartrate = models.IntegerField(blank=True, null=True)
    temperature = models.FloatField(blank=True, null=True)
    blood_pressure = models.CharField(max_length=20, blank=True)
    glucose_level = models.FloatField(blank=True, null=True)
    oxygen_level = models.FloatField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)

