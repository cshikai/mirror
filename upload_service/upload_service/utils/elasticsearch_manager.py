from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk, scan, streaming_bulk
import json

QUEUE_SIZE=10000

class ESManager():

    def __init__(self, config):
        self.url = config['ELASTICSEARCH']['URL']
        self.index = config['ELASTICSEARCH']['INDEX_NAME']
        self.username = config['ELASTICSEARCH']['ELASTIC_USERNAME']
        self.password = config['ELASTICSEARCH']['ELASTIC_PASSWORD']
        self.client = Elasticsearch(self.url,
                                    verify_certs=False,
                                    basic_auth=(self.username, self.password))
        self.consolidated_actions=[]

    def upload_to_es(self, data_dict):
        # For single document upload
        response = self.client.index(index=self.index,
                        document=data_dict)
        if response['_shards']['successful']==1:
            return response['_id']
        else:
            return None
    
    def enqueue_bulk_upload(self, data_list):
        """
        Parse list of data dict into ES bulk format, then calls flush to start upload;
        Returns the list of id generated by ES for each of the documents
        """
        for doc in data_list:
            source_dict = {}
            source_dict['_op_type']= 'index'
            source_dict['_index']=self.index
            source_dict['_source']=doc
            self.consolidated_actions.append(source_dict)
        bulk_es_ids = self.flush()
        return bulk_es_ids

    def flush(self):
        """
        Call on helper.streaming_bulk to start the upload.
        """
        errors = []
        list_of_es_ids = []
        for ok, item in streaming_bulk(self.client, self.consolidated_actions):
            if not ok:
                errors.append(item)
            else:
                list_of_es_ids.append(item['index']['_id'])
        print("List of errors:", errors)
        # Not that we know what to do with the errors hehe
        self.consolidated_actions=[]
        return list_of_es_ids

    def get_all_documents(self):
        """
        A generator object; Retrieve all document ids iteratively. 
        """
        docs_response = scan(self.client, index=self.index, query={"query":{"match_all":{}}})
        for item in docs_response:
            doc_id = item['_id']
            yield doc_id