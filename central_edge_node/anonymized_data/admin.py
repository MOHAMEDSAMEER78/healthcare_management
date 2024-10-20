# anonymized_data/admin.py

from django.contrib import admin
from .models import AnonymizedPatientData

admin.site.register(AnonymizedPatientData)
