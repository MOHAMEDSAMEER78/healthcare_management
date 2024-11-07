from django.urls import path
from .views import get_all_records

urlpatterns = [
    # ...existing urls...
    path('api/records/', get_all_records, name='get_all_records'),
]
