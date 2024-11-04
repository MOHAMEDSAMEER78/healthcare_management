# anonymized_data/models.py

from django.db import models

class AnonymizedPatientData(models.Model):
    id = models.AutoField(primary_key=True)  # Regular integer field 
    patient_original_data_id = models.IntegerField(unique=True)  # Regular integer field
    edge_device_name = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100, blank=True)
    age = models.IntegerField()
    heartrate = models.IntegerField(null=True, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    blood_pressure = models.CharField(max_length=20, blank=True)
    glucose_level = models.FloatField(null=True, blank=True)
    oxygen_level = models.FloatField(null=True, blank=True)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.name} - {self.date} {self.time}"
