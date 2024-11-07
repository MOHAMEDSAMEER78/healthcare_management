from django.shortcuts import render
from django.http import JsonResponse
from elasticsearch import Elasticsearch
from rest_framework.decorators import api_view
import logging
import time
from elasticsearch.exceptions import ConnectionError

logger = logging.getLogger(__name__)

# Initialize Elasticsearch with compatibility settings
es = Elasticsearch(
    ['http://elasticsearch:9200'],
    retry_on_timeout=True,
    max_retries=3,
    timeout=30,
    verify_certs=False,
    headers={"Content-Type": "application/json"})

def init_elasticsearch():
    """Initialize Elasticsearch indices and mappings"""
    try:
        # Create index if it doesn't exist
        if not es.indices.exists(index="anonymized_patient_data"):
            es.indices.create(
                index="anonymized_patient_data",
                body={
                    "settings": {
                        "number_of_shards": 1,
                        "number_of_replicas": 0
                    },
                    "mappings": {
                        "properties": {
                            "name": {"type": "text"},
                            "age": {"type": "integer"}
                        }
                    }
                }
            )
            logger.info("Created anonymized_patient_data index")
    except Exception as e:
        logger.error(f"Error initializing Elasticsearch: {e}")

@api_view(['GET'])
def get_all_records(request):
    init_elasticsearch()

    max_retries = 3
    retry_delay = 2

    for attempt in range(max_retries):
        try:
            if not es.ping():
                raise ConnectionError("Cannot connect to Elasticsearch")
            
            logger.info('Fetching all records from Elasticsearch')
            response = es.search(
                index="anonymized_patient_data",
                body={"query": {"match_all": {}}},
                ignore_unavailable=True
            )
            records = [hit['_source'] for hit in response['hits']['hits']]
            return JsonResponse(records, safe=False)
            
        except ConnectionError as e:
            logger.warning(f"Connection attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                return JsonResponse(
                    {'error': 'Could not connect to Elasticsearch'}, 
                    status=503
                )
        except Exception as e:
            logger.error(f"Error fetching records: {e}")
            return JsonResponse({'error': str(e)}, status=500)

# Call init_elasticsearch when the module loads
init_elasticsearch()