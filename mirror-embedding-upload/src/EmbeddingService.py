# standard lib
from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from typing import Dict, List
import time

# external packages
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import FilterRetriever

from confluent_kafka import Consumer
from confluent_kafka.admin import AdminClient, NewTopic
import torch
import yaml

# own modules/classes
from TextVectoriser import TextVectoriser
from utils.milvus_manager import MilvusMgr


class EmbeddingService:

    def __init__(self, cfg: Dict):
        self.config = cfg
        self.consumer = None
        self.kafka_consumer_cfg = {'topic': 'queue-upload-semantic-text'}  # TODO: refactor: init Topic from config file.
        self.setup()
        
    def setup(self):
        #parser = ArgumentParser()
        #parser.add_argument('config_file', type=FileType('r'))
        #parser.add_argument('--reset', action='store_true')
        #args = parser.parse_args()

        #config_parser = ConfigParser()
        #config_parser.read_file(args.config_file)
        #self.kafka_consumer_cfg = dict(config_parser['default'])
        #self.kafka_consumer_cfg.update(config_parser['consumer'])
        self.init_kafka_topics()
        self.init_kafka_consumer()
        self.init_embedding_model()
        

    def init_kafka_topics(self):
        admin_client = AdminClient({'bootstrap.servers':'broker:29092'})
        topic_list = []
        topic_list.append(NewTopic(self.kafka_consumer_cfg['topic'], 1, 1))
        return_values = admin_client.create_topics(topic_list)
        print(f"return value of create_topics: {return_values}")
        print(f"topics: {admin_client.list_topics().topics}")

    def init_kafka_consumer(self):
        # TODO: instantiate from config file instead of hardcoding.
        self.consumer = Consumer({'bootstrap.servers':'broker:29092',
            'group.id':'python-consumer',
            'auto.offset.reset':'earliest'})
        print("Kafka Consumer has been initiated... and listening to...")
        print(f"Subscribing to Kafka topic:'{self.kafka_consumer_cfg['topic']}'")
        self.consumer.subscribe([self.kafka_consumer_cfg['topic']])

    def init_embedding_model(self):
        # TODO: instantiate from config file instead of hardcoding. e.g. point to a different model path.
        self.embedding_model = TextVectoriser("../models/sup-simcse-roberta-base")

    def poll_consumer(self, timeout_in_secs):
        return self.consumer.poll(timeout_in_secs)

    def get_embedding(self, data_list):
        return self.embedding_model.compute_vector(data_list)

class MessageUtils:
    ELASTICSEARCH_INDEX_KEY = 'es_id'


def store_embedding(milvus_manager: MilvusMgr, doc_ids: List[str], embeddings: torch.FloatTensor):
    '''
    Upload batch of embeddings to an embedding database.
    :param milvus_manager: MilvusMgr instance.
    :param doc_ids: the unique string indices of a batch of documents. 
    :param embeddings: torch.FloatTensor of shape (batch_size, hidden_size.
    '''
    milvus_manager.upload_to_Milvus(
        {
        'es_ids': doc_ids,
        'embeddings': embeddings.tolist()
        }
    )

def main():
    
    with open('../../configs/config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    FLUSH_PERIOD = config['embedding_upload_service']['flush_period']
    # FLUSH_PERIOD determines the maximum number of seconds before a non-empty text buffer
    # is flushed and its contents used to generate embeddings which are then uploaded to Milvus.

    BATCH_SIZE = config['embedding_upload_service']['batch_size']
    # number of documents to batch before generating embeddings and uploading to db.

    emb_service = EmbeddingService(config)

    milvus_manager = MilvusMgr(config)
    print(f"connected to Milvus db.")

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
    print(f"connected to ElasticsearchDocumentStore.")

    retriever = FilterRetriever(document_store)

    text_buffer = []  # for holding text data.
    doc_id_buffer = []  # for holding doc ids.
    time_since_buffer_last_added = 0  # seconds since epoch.
    try:
        while True:
            if text_buffer:
                if time.time() - time_since_buffer_last_added >= FLUSH_PERIOD or len(text_buffer) == BATCH_SIZE:
                    embeddings = emb_service.get_embedding(text_buffer)
                    store_embedding(milvus_manager, doc_id_buffer, embeddings)
                    print(f"pushed {len(text_buffer)} embeddings.")
                    # clear buffers.
                    text_buffer = []
                    doc_id_buffer = []

            msg = emb_service.poll_consumer(1.0) #timeout
            if msg is None:
                continue
            if msg.error():
                print('Error: {}'.format(msg.error()))
                continue
        
            data = msg.value().decode('utf-8')
            data_dict = eval(data)
            doc_id = data_dict[MessageUtils.ELASTICSEARCH_INDEX_KEY]
            
            # Query text db for text data associated with doc_id.
            docs = retriever.retrieve(query="",filters={"_id": [doc_id]})

            text = docs[0].content
            print(f"retrieved: {doc_id}: {text}")
            
            text_buffer.append(text)
            time_since_buffer_last_added = time.time()
            doc_id_buffer.append(doc_id)
            
            
    except KeyboardInterrupt:
        emb_service.consumer.close()


if __name__ == '__main__':
    main()