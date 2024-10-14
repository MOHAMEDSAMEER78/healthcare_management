from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from .models import PatientData, AnomizedPatientData
from rest_framework.exceptions import NotFound
import random
import string
import numpy as np

# Helper functions for privacy techniques
def anonymize_name(name):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def randomize_heartrate(heartrate):
    return heartrate + random.randint(-3, 3)

def randomize_temperature(temperature):
    return round(temperature + random.uniform(-0.5, 0.5), 2)

def apply_laplace_noise(value, epsilon=1.0):
    noise = np.random.laplace(loc=0, scale=1/epsilon)
    return value + noise

@api_view(['POST'])
def GetPatientData(request):
    data = request.data
    
    name = anonymize_name(data.get('name'))  # Anonymize name
    age = data.get('age')
    heartrate = randomize_heartrate(data.get('heartrate'))  # Randomize heartrate
    temperature = randomize_temperature(data.get('temperature'))  # Randomize temperature
    blood_pressure = data.get('blood_pressure')
    glucose_level = apply_laplace_noise(data.get('glucose_level', 0))  # Apply noise to glucose level
    oxygen_level = apply_laplace_noise(data.get('oxygen_level', 0))  # Apply noise to oxygen level
    date = datetime.now().date()
    time = datetime.now().time()

    # Save the original patient data
    patient_data = PatientData(
        name=data.get('name'),
        age=data.get('age'),
        heartrate=data.get('heartrate'),
        temperature=data.get('temperature'),
        blood_pressure=data.get('blood_pressure'),
        glucose_level=data.get('glucose_level'),
        oxygen_level=data.get('oxygen_level'),
        date=date,
        time=time
    )
    patient_data.save()
    
    patient_id = patient_data.id
    if patient_id is None:
        return Response({'error': 'patient_id is required'}, status=status.HTTP_400_BAD_REQUEST)

    patient_data = PatientData.objects.filter(id=patient_id).first()
    if patient_data is None:
        return Response({'error': 'PatientData matching query does not exist'}, status=status.HTTP_404_NOT_FOUND)

    anomolized_patient_data = AnomizedPatientData(
        patient=patient_data,
        name=name,
        age=age,
        heartrate=heartrate,
        temperature=temperature,
        blood_pressure=blood_pressure,
        glucose_level=glucose_level,
        oxygen_level=oxygen_level,
        date=date,
        time=time
    )
    anomolized_patient_data.save()

    return Response({'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def DisplayPatientData(request):
    data = request.data
    name = data.get('name')

    # Fetch all patients with the given name
    patients = PatientData.objects.filter(name=name)

    # Check if any patients were found
    if not patients.exists():
        raise NotFound(detail="Patient not found.")

    # You can also choose to handle only the first patient if needed
    patient = patients.first()  # This gets the first patient if you want to process just one
    patient_id = patient.id

    # Fetch anonymized patient data using the fetched patient_id
    patient_data = AnomizedPatientData.objects.filter(id=patient_id).values(
        'name', 'age', 'heartrate', 'temperature', 'blood_pressure', 'glucose_level', 'oxygen_level', 'date', 'time'
    )

    if not patient_data:
        return Response({'status': 'success', 'patient_data': []}, status=status.HTTP_200_OK)

    # Anonymizing patient data for display
    anonymized_patient_data = [
        {
            'name': item['name'],
            'age': item['age'],
            'heartrate': item['heartrate'],
            'temperature': item['temperature'],
            'blood_pressure': item['blood_pressure'],
            'glucose_level': item['glucose_level'],
            'oxygen_level': item['oxygen_level'],
            'date': item['date'],
            'time': item['time']
        } for item in patient_data
    ]

    return Response({'status': 'success', 'patient_data': anonymized_patient_data}, status=status.HTTP_200_OK)


@api_view(['GET'])
def AllPatientData(request):
    patient_data = AnomizedPatientData.objects.all().values(
        'name', 'age', 'heartrate', 'temperature', 'blood_pressure', 'glucose_level', 'oxygen_level', 'date', 'time'
    )
    return Response({'status': 'success', 'patient_data': list(patient_data)}, status=status.HTTP_200_OK)
