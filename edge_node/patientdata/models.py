from django.db import models

# Create your models here.

class PatientData(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    age = models.IntegerField() 
    heartrate = models.IntegerField(null=True, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    blood_pressure = models.CharField(max_length=20, null=True, blank=True)
    glucose_level = models.FloatField(null=True, blank=True)
    oxygen_level = models.FloatField(null=True, blank=True)
    date = models.DateField()
    time = models.TimeField()