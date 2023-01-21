import yaml
from typing import List
from pymilvus import connections, Collection

SEARCH_RESULT = 'search_result'
ID = 'id'
CONFIDENCE_SCORE = 'confidence_score'
METRIC_TYPE = 'metric_type'
PARAMS = "params"
NPROBE = "nprobe"

with open('../configs/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

connections.connect(
    alias=config['milvus']['alias'], 
    host=config['milvus']['host'], 
    port=config['milvus']['port']
)

collection = Collection(config['milvus']['collection_name'])
collection.load()

search_params = {METRIC_TYPE: config['milvus']['metric_type'], PARAMS: {NPROBE: 10}}

def query_milvus(query_embeddings: List[List[float]]):

    result = collection.search(
        data=query_embeddings, 
        anns_field=config['milvus']['search_field'], 
        param=search_params, 
        limit=config['query_service']['limit'], 
        expr=None,
        consistency_level=config['query_service']['consistency_level']
    )

    # do the preprocessing from the returned results

    # initiate the preprocessed dict
    preprocessed_dict = {SEARCH_RESULT: []}
    for idx, dist in zip(result[0].ids, result[0].distances):
        preprocessed_dict[SEARCH_RESULT].append({ID: idx, CONFIDENCE_SCORE:dist})

    return preprocessed_dict

def query_milvus_evaluation(query_embeddings: List[List[float]]):

    result = collection.search(
        data=query_embeddings, 
        anns_field=config['milvus']['search_field'], 
        param=search_params, 
        limit=config['query_sevice']['limit'], 
        expr=None,
        consistency_level=config['query_service']['consistency_level']
    )

    # do the preprocessing from the returned results

    # initiate the preprocessed dict
    preprocessed_dict = {SEARCH_RESULT: []}

    for entry in result[0]:
        preprocessed_dict[SEARCH_RESULT].append(entry.doc_id)

    return preprocessed_dict

if __name__ == '__main__':
    pass