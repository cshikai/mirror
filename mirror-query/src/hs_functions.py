from fastapi import FastAPI, Request
from typing import List, Dict, Any, Optional
from asyncio import Lock
import requests
import yaml
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import EmbeddingRetriever, ElasticsearchRetriever

SEARCH_RESULT = 'search_result'
ID = 'id'
CONFIDENCE_SCORE = 'confidence_score'

with open('../configs/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

document_store = ElasticsearchDocumentStore(
                host=config['elasticsearch']['host'],
                port=config['elasticsearch']['port'],
                username=config['elasticsearch']['username'],
                password=config['elasticsearch']['password'],
                scheme="https",
                verify_certs=False,
                index=config['elasticsearch']['index'],
                search_fields=["content", "title"]
            )

print(document_store)

def query_es(query: str):
    sparse_retriever = ElasticsearchRetriever(document_store=document_store)
    result = sparse_retriever.retrieve(query=query, top_k=config['query_service']['top_k'], index=config['elasticsearch']['index'], filters=None)

    # initiate the preprocessed dict
    preprocessed_dict = {SEARCH_RESULT: []}

    # Post processing, to return only the id and the confidence score
    for entry in result:
        preprocessed_dict[SEARCH_RESULT].append({ID: entry.id,
                                                 CONFIDENCE_SCORE: entry.score})

    return preprocessed_dict

def query_es_evaluation(query: str):
    sparse_retriever = ElasticsearchRetriever(document_store=document_store)
    result = sparse_retriever.retrieve(query=query, top_k=config['query_service']['top_k'], index=config['elasticsearch']['index'], filters=None)

    # initiate the preprocessed dict
    preprocessed_dict = {SEARCH_RESULT: []}

    # Post processing, to return only the id and the confidence score
    for entry in result:
        preprocessed_dict[SEARCH_RESULT].append(entry.meta['doc_id'])

    return preprocessed_dict