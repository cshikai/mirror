from haystack.document_stores import ElasticsearchDocumentStore
from haystack.schema import Document
from haystack.nodes import BM25Retriever

import pandas as pd
import ast
import json
import yaml

import torch
import numpy as np
from tqdm import tqdm

def create_index(cfg):

    mappings_file = open(cfg['elasticsearch']['mappings_file'])
    print(cfg['elasticsearch']['mappings_file'])
    mappings = json.load(mappings_file)

    document_store = ElasticsearchDocumentStore(host=cfg['elasticsearch']['host'],
                                                port=cfg['elasticsearch']['port'],
                                                username=cfg['elasticsearch']['username'],
                                                password=cfg['elasticsearch']['password'],
                                                scheme="https", 
                                                verify_certs=False, 
                                                custom_mapping=mappings,
                                                index=cfg['elasticsearch']['index'])


    return document_store

if __name__ == '__main__':
    with open("../configs/config.yaml", "r") as f:
        config = yaml.load(f)

    create_index(config)
