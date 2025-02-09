# Ensure the database table for AnonymizedPatientData exists
# Run the following commands in your terminal to create and apply migrations

# python manage.py makemigrations anonymized_data
# python manage.py migrate anonymized_data

import google.generativeai as genai
import os
import logging
import json
import requests

from .utils import save_patient_data

logger = logging.getLogger(__name__)

def initialize_gemini():
    """Initialize Gemini model configuration"""
    try:
        api_key = 'AIzaSyBsIZsbvLSI9ArQzWl72FdFgKCzxUCoSs4'
            
        base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        model_name = "gemini-1.5-flash"
        
        # Store configuration for use in other functions
        return {
            "api_key": api_key,
            "endpoint": f"{base_url}/{model_name}:generateContent",
            "headers": {
                "Content-Type": "application/json"
            }
        }
    except Exception as e:
        logger.error(f"Failed to initialize Gemini configuration: {e}")
        return None

def anonymize_data(config, patient_data):
    """Use Gemini to anonymize patient data"""
    try:
        if not config:
            raise ValueError("Gemini configuration not initialized")
            
        payload = {
            "contents": [{
                "parts": [{
                    "text": """
                    Anonymize the following patient data by replacing sensitive information with generic placeholders.
                    Return ONLY a valid JSON object with no additional text or formatting.
                    
                    Input: {patient_data}
                    
                    Rules:
                    - Replace real names with generic names
                    - Keep all medical values unchanged
                    - Keep timestamps and dates unchanged
                    - Keep device names unchanged
                    - Return only the JSON object, no explanations
                    """.format(patient_data=str(patient_data))
                }]
            }]
        }
        
        # Make the API request
        response = requests.post(
            f"{config['endpoint']}?key={config['api_key']}", 
            headers=config['headers'],
            json=payload
        )
        
        if response.status_code != 200:
            logger.error(f"API request failed: {response.status_code} - {response.text}")
            return None
            
        # Parse the response
        response_data = response.json()
        if 'candidates' in response_data:
            anonymized_text = response_data['candidates'][0]['content']['parts'][0]['text']
            # Clean up the response to ensure it's valid JSON
            anonymized_text = anonymized_text.replace('```json', '').replace('```', '').strip()
            
            try:
                return json.loads(anonymized_text)
            except json.JSONDecodeError as je:
                logger.error(f"JSON parsing error: {je}")
                logger.debug(f"Attempted to parse: {anonymized_text}")
                return None
                
        return None
            
    except Exception as e:
        logger.error(f"Failed to anonymize data: {e}")
        return None

def process_patient_data(data):
    """Process and anonymize patient data"""
    try:
        # Initialize Gemini model
        config = initialize_gemini()
        if not config:
            logger.error("Failed to initialize Gemini model")
            return
            
        # Anonymize the data
        anonymized_data = anonymize_data(config, data)
        if not anonymized_data:
            logger.error("Failed to anonymize data")
            return
            
        # Process the anonymized data further as needed
        logger.info("Successfully anonymized patient data")
        return save_patient_data(anonymized_data)
        
    except Exception as e:
        logger.error(f"Error in process_patient_data: {e}")
        return None
