from pymilvus import connections, utility, FieldSchema, CollectionSchema, DataType, Collection
import yaml
from typing import Dict

#def read_yaml(file_path='config.yaml'):
#    with open(file_path, "r") as f:
#        return yaml.safe_load(f)

#config = read_yaml()

class MilvusMgr():
    def __init__(self, config: Dict):
        print(config)

        self.alias = config['milvus']['alias']
        self.host = config['milvus']['host']
        self.port = config['milvus']['port']
        
        connections.connect(alias=self.alias, host=self.host, port=self.port)
        self.milvus = Collection(config['milvus']['collection_name'])
    
    def upload_to_Milvus(self, embedding_dict):
        """
        Format of embedding_dict:
        {
            es_ids: [List of ids],
            embeddings: [List of 512 dim embeddings]
        }
        """
        if len(embedding_dict['es_ids'])  != len(embedding_dict['embeddings']):
            print("IDs and EMBEDDING LENGTH MISMATCH")
            return 
        entities = [embedding_dict['embeddings'], embedding_dict['es_ids']]
        self.milvus.insert(entities)