# anonymized_data/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnonymizedPatientDataViewSet

router = DefaultRouter()
router.register(r'anonymized-patient-data', AnonymizedPatientDataViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Custom route for save_patient_data
    path('anonymized_patient_data/save_patient_data/', AnonymizedPatientDataViewSet.as_view({'post': 'save_patient_data'}), name='save_patient_data'),
]
