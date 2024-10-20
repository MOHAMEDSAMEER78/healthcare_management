# anonymized_data/models.py

from django.db import models
from patientdata.models import PatientData  # Import PatientData directly

class AnonymizedPatientData(models.Model):
    # Use the imported model directly instead of a string reference
    patient = models.ForeignKey(PatientData, on_delete=models.CASCADE)  
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
