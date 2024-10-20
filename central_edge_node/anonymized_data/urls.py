# anonymized_data/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnonymizedPatientDataViewSet

router = DefaultRouter()
router.register(r'anonymized-patient-data', AnonymizedPatientDataViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
