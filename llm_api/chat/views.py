from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import os

OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")

@csrf_exempt
def generate_text(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            prompt = data.get("prompt", "")

            response = requests.post(OLLAMA_API_URL, json={"model": "mistral", "prompt": prompt})
            return JsonResponse(response.json(), safe=False)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)
