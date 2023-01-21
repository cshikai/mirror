from fastapi import FastAPI, Request
from asyncio import Lock
from query import *
import requests

lock = Lock()
app = FastAPI()

QUERY_KEY = 'query'
LIST_QUERY_KEY = 'queries'
TEXT = 'text'
SEARCH_QUERY = 'searched_query'
TRANSFORMED_QUERY = 'transformed_query'
SEARCH_RESULT = 'search_result'
LEXICAL_INTENT = 'lexical'
LEXICAL_EVAL_INTENT = 'lexical_evaluation'
SEMANTIC_INTENT = 'semantic'
SEMANTIC_EVAL_INTENT = 'semantic_evaluation'
TOP_5 = 'top_5'

@app.post("/query")
async def get_query(request: Request):
    raw_query = await request.json()
    query = raw_query[QUERY_KEY]

    # preprocess the query, retrieve the data from es or milvus 
    query_manager = QueryManager()
    intent = query_manager.intent_identifier.identify(query)
    transformed_query = query_manager.query_transformer.transform(query, intent)
    process = query_manager.query_process[intent]
    result_raw = process.get(transformed_query)

    print(result_raw)

    # append the search query and the preprocessed query into the result dictionary
    result = {}
    result[SEARCH_QUERY] = query
    result[TRANSFORMED_QUERY] = transformed_query
    result[SEARCH_RESULT] = result_raw[SEARCH_RESULT]

    # pass this result to the gateway
    return result

@app.post("/evaluate_es")
async def get_evaluation(request: Request):
    raw_query = await request.json()

    # to send the query one by one
    for query in raw_query[LIST_QUERY_KEY]:
        query_manager = QueryManager()
        process_es = query_manager.query_process[LEXICAL_EVAL_INTENT]
        result_raw = process_es.get(query[TEXT])
        result_top_5 = result_raw[SEARCH_RESULT][:5]
        query[TOP_5] = result_top_5

    return raw_query

@app.post("/evaluate_milvus")
async def get_evaluation(request: Request):
    raw_query = await request.json()

    # to send the query one by one
    for query in raw_query[LIST_QUERY_KEY]:
        query_manager = QueryManager()
        process_milvus = query_manager.query_process[SEMANTIC_EVAL_INTENT]
        result_raw = process_milvus.get(query[TEXT])
        result_top_5 = result_raw[SEARCH_RESULT][:5]
        query[TOP_5] = result_top_5

    return raw_query