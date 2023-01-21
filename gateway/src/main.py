
'''
Main file for gateway
uvicorn main:api --host 0.0.0.0 --port 8502
'''

import requests
from typing import List, Dict, Any
from fastapi import FastAPI
from pydantic import BaseModel

class Ports:
    '''Base port configs'''
    upload_service: str = 'http://uploader:8000/bulk_upload'
    query_service: str = 'http://query_service:3000/query'


class QueryItem(BaseModel):
    '''Base class for queries'''
    query: str

class UploadItem(BaseModel):
    '''Base class for upload items'''
    doc_id: str
    content: str
    content_type: str
    title: str
    doc_timestamp: str
    medium: str
    source: str

class UploadBulk(BaseModel):
    '''Bulk of Upload Items'''
    data: List[UploadItem]

class QueryOutput(BaseModel):
    '''Expected output from query service'''
    searched_query: str
    transformed_query: str
    searched_result: List[Dict[str, Any]]

class UploadOutput(BaseModel):
    '''Expected response from Upload service'''
    status: str

app = FastAPI()

@app.post('/query')
def query(item: QueryItem):
    '''docstring'''
    response = requests.post(Ports.query_service, json=item.dict(), headers={'content-type': 'application/json'})
    return response.json()

@app.post('/upload')
def upload(item: UploadBulk):
    '''docstring'''
    # for i in item.data:
    response = requests.put(Ports.upload_service, json=item.dict(), headers={'content-type':'application/json'})
    return response.json()

if __name__ == '__main__':
    pass
