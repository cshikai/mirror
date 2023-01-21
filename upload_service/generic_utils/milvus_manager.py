from pymilvus import connections, utility, FieldSchema, CollectionSchema, DataType, Collection

class MilvusMgr():
    def __init__(self, config):
        """
        To initialize:
            from utils.milvus_manager import MilvusMgr
            milvus = MilvusMgr(cfg) #cfg needs host, port, and collection name

        Config Format:
            MILVUS:
                HOST: 'standalone'
                PORT: '19530'
                COLLECTION: 'moat'
        """
        self.host = config['MILVUS']['HOST']
        self.port = config['MILVUS']['PORT']
        self.collection = config['MILVUS']['COLLECTION']
        self.milvus = Collection(self.collection)
        connections.connect('default', self.host, self.port)
    
    def upload_to_milvus(self, embedding_dict):
        """
        Format of embedding_dict:
        {
            es_ids: List of ids,
            embeddings: List of 512 dim embeddings
        }
        """
        if len(embedding_dict['es_ids'])  != len(embedding_dict['embeddings']):
            print("IDs and EMBEDDING LENGTH MISMATCH")
            return 
        entities = [embedding_dict['embeddings'], embedding_dict['es_ids']]
        self.milvus.insert(entities)
        return

    def delete_from_milvus(self, ids):
        """
        id: List of id of vector to be deleted
        """
        self.milvus.delete_entity_by_id(collection_name=self.collection, id_array=ids)

    # def query_milvus
