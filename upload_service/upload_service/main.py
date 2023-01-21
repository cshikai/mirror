
import yaml
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any, List

from utils.elasticsearch_manager import ESManager
from utils.kafka_manager import KafkaManager

from datetime import datetime

import warnings
warnings.filterwarnings("ignore")

def read_yaml(file_path='config.yaml'):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

config = read_yaml()

elastic = ESManager(config)
kafka = KafkaManager(config)

api = FastAPI(
    title='Doc Upload API',
    version='1.0.0'
)

class Data(BaseModel):
    doc_id: str
    title: str
    content: str
    content_type: str
    doc_timestamp: str
    medium: str
    source: str

class BulkData(BaseModel):
    data: List[Data]



### SINGLE UPLOAD ###
@api.put("/upload")
def upload(data: Data):
    """
    Expects a dictionary:
    {
        doc_id: unique id from data from its source,
        title: title from corpus (if not available, leave empty string),
        doc_timestamp: timestamp of document (if not available, ),
        medium: text/image/audio,
        source: origin of data
    }
    """
    print(data)
    data = data.dict()
    data['upload_timestamp']=datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    status = elastic.upload_to_es(data)
    response = {}
    if status:
        kafka.enqueue_kafka(status['_id'], config['KAFKA']['TOPIC'])
    response['status'] = 'Success'
    return response




### BULK UPLOAD ###
@api.put("/bulk_upload")
def bulk_upload(data: BulkData):
    data = data.dict()
    bulk_ids = elastic.enqueue_bulk_upload(data['data'])
    print(bulk_ids)
    for es_ids in bulk_ids:
        kafka.enqueue_kafka(es_ids, config['KAFKA']['TOPIC'])
    response = {}
    response['status'] = 'Success'
    return response

@api.put("/flush")
def flush():
    """
    Explicitly bulk upload enqueued documents
    """
    try:
        elastic.flush()
        response = {}
        response['status'] = 'Success'
        return response
    except:
        response['status'] = 'Error'
        return response


@api.put("/kafka_enqueue_all_docs")
def kafka_enqueue_all_docs():
    for doc_id in elastic.get_all_documents():
        kafka.enqueue_kafka(doc_id, config['KAFKA']['TOPIC'])
        
if __name__ == '__main__':
    kafka_enqueue_all_docs()
    