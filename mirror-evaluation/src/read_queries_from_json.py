'''
accepts the json file, then call the query service to get the prediction, returns the json appended with the top5
'''

import requests
import json

def _load_json(json_path: str):
    with open(json_path, 'r+') as f:
        queries = json.load(f)

    return queries

def get_result_id_es(json_path: str):
    queries_dict = _load_json(json_path)

    # call the query services
    response_es = requests.post('http://localhost:3000/evaluate_es', json=queries_dict)

    return response_es.json()
    
def get_result_id_milvus(json_path: str):
    queries_dict = _load_json(json_path)

    # milvus
    response_milvus = requests.post('http://localhost:3000/evaluate_milvus', json=queries_dict)

    return response_milvus.json()

if __name__ == '__main__':
    
    es_test_dict = get_result_id_es('../queries/test_pairs.json')
    # es_dev_dict = get_result_id_es('../queries/dev_pairs.json')
    # milvus_test_dict = get_result_id_es('../queries/test_pairs.json')

    # es_dev_dict = get_result_id_es('../queries/dev_pairs.json')
    # milvus_dev_dict = get_result_id_es('../queries/dev_pairs.json')

    ES_TEST_PATH = '../queries_top_k/test_result.json'
    # ES_DEV_PATH = '../queries_top_k/dev_result.json'

    with open(ES_TEST_PATH, 'w+') as f:
        json.dump(es_test_dict, f, indent=2)

    # with open(ES_DEV_PATH, 'w+') as f:
    #     json.dump(es_dev_dict, f, indent=2)

    # with open(ES_DEV_PATH, 'w+') as f:
    #     json.dump(milvus_test_dict, f, indent=2)