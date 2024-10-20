from django.urls import path
from . import views

urlpatterns = [
    path('', views.patient_data_list, name='patient_data_list'),
    path('<int:pk>/', views.patient_data_detail, name='patient_data_detail'),
]
