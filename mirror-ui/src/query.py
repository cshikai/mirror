from haystack.nodes import FilterRetriever
from haystack.document_stores import ElasticsearchDocumentStore
import haystack
import requests
from typing import List

class UI_Querier:
    def __init__(self, config: dict) -> None:
        self.document_store = ElasticsearchDocumentStore(
                        host=config['elasticsearch']['host'],
                        port=config['elasticsearch']['port'],
                        username=config['elasticsearch']['username'],
                        password=config['elasticsearch']['password'],
                        scheme="https",
                        verify_certs=False,
                        index=config['elasticsearch']['index'],
                        search_fields=["content", "title"]
                    )

        self.retriever = FilterRetriever(document_store = self.document_store)
        self.url = f"http://{config['gateway']['host']}:{config['gateway']['port']}/query"

    def send_query(self, query:dict)-> dict:
        response = requests.post(self.url, json = query)
        try:
            response = response.json()
            return response
        except requests.exceptions.JSONDecodeError as e:
            return {}
    
    def retrieve_data(self, id:int) -> List[haystack.schema.Document]:
        result =  self.retriever.retrieve(
            query = "",
            filters = {'_id': id }
        )
        return result