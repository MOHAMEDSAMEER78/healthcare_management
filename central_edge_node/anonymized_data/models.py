# anonymized_data/models.py

from django.db import models

class AnonymizedPatientData(models.Model):
    patient_id = models.IntegerField()  # Regular integer field 
    patient_original_data_id = models.IntegerField(unique=True)  # Regular integer field
    edge_device_name = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100, blank=True)
    age = models.IntegerField()
    heartrate = models.IntegerField(blank=True)
    temperature = models.FloatField(blank=True)
    blood_pressure = models.CharField(max_length=20, blank=True)
    glucose_level = models.FloatField(blank=True)
    oxygen_level = models.FloatField(blank=True)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.name} - {self.date} {self.time}"
