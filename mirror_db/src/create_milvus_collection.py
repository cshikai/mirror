from dataclasses import fields
from pymilvus import CollectionSchema, FieldSchema, DataType, connections, utility, Collection
import json
import yaml

def create_index(cfg):
    mappings_file = open(cfg['milvus']['mappings_file'])
    mappings = json.load(mappings_file)

    connections.connect(
        alias=cfg['milvus']['alias'],
        host=cfg['milvus']['host'],
        port=cfg['milvus']['port']
    )

    fields = []
    
    for key, value in mappings.items():
        if value['data_type'] == "FLOAT_VECTOR":
            embeddings = FieldSchema(
                            name=key, 
                            dtype=DataType.FLOAT_VECTOR, 
                            dim=value['embedding_dimensions']
                        )
            fields.append(embeddings)
        elif value['data_type'] == "VARCHAR":
            id = FieldSchema(
                            name=key, 
                            dtype=DataType.VARCHAR, 
                            max_length=value['max_length'],
                            is_primary=value['is_primary']
                        )
            fields.append(id)
        else:
            print("data type {} not supported".format(value['data_type']))

    schema = CollectionSchema(fields=fields)
    collection = Collection(
                    name=cfg['milvus']['collection_name'], 
                    schema=schema, 
                    using='default', 
                )
    index_params = {
                    "metric_type":cfg['milvus']['metric_type'],
                    "index_type":cfg['milvus']['index_type'],
                    "params":{"nlist":1024}
                   }


    collection.create_index(
                    field_name=cfg['milvus']['embeddings_field'], 
                    index_params=index_params
                )

    return

if __name__ == '__main__':
    with open("../configs/config.yaml", "r") as f:
        config = yaml.load(f)

    create_index(config)
