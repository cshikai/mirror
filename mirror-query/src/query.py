from typing import List, Dict, Any, Optional
import string
import requests
from hs_functions import *
from milvus_functions import *
from pymilvus import connections
from fastapi import FastAPI, Request

LEXICAL_INTENT = 'lexical'
SEMANTIC_INTENT = 'semantic'
LEXICAL_EVAL_INTENT = 'lexical_evaluation'
SEMANTIC_EVAL_INTENT = 'semantic_evaluation'

QUERY = 'query'
SEARCH_QUERY = 'searched_query'
TRANSFORMED_QUERY = 'transformed_query'
SEARCH_RESULT = 'search_result'

lock = Lock()
app = FastAPI()

class QueryManager:
    def __init__(self) -> None:
        self.intent_identifier = IntentIdentifier()
        self.query_process = {
            LEXICAL_INTENT: LexicalProcessor(), 
            SEMANTIC_INTENT: SemanticProcessor(), 
            LEXICAL_EVAL_INTENT: LexicalProcessorEvaluation(),
            SEMANTIC_EVAL_INTENT: SemanticProcessorEvaluation()
        }
        self.query_transformer = QueryTransformer()

class IntentIdentifier:

    def __init__(self) -> None:
        pass
   
    def identify(self, query: str) -> str:
        '''
        returns either 'lexical' or 'semantic' for now
        '''

        # if query.find('?') != -1: # ? and 5W1H extend conditions if there are natural qns field
        #     return 'natural_question'

        # text preprocessing to remove the punctuation for the check
        query_check = query.translate(str.maketrans('', '', string.punctuation))

        if len(query_check.split()) < 5:
            return LEXICAL_INTENT

        else:
            return SEMANTIC_INTENT

class QueryTransformer:

    def __init__(self) -> None:
        pass

    def transform(self,  query: str, intent: str) -> str:

        # check on the intent
        if intent == LEXICAL_INTENT:
            # TODO: future implementation
            transformed_query = query
        
        elif intent == SEMANTIC_INTENT:
            # TODO: future implementation
            transformed_query = query

        return transformed_query

class QueryProcessor:
    '''
    interface
    '''

    def __init__(self) -> None:
        pass

    def get(self):
        pass

class LexicalProcessor(QueryProcessor):

    def __init__(self) -> None:
        super().__init__()

    def get(self, transformed_query: str):
        '''
        do the api call to the lexical database -> ES
        '''

        result = query_es(transformed_query)

        return result

class LexicalProcessorEvaluation(QueryProcessor):

    def __init__(self) -> None:
        super().__init__()

    def get(self, transformed_query: str):
        '''
        do the api call to the lexical database -> ES
        '''

        result = query_es_evaluation(transformed_query)

        return result

class SemanticProcessor(QueryProcessor):

    def __init__(self) -> None:
        super().__init__()

    def get(self, transformed_query: str):
        '''
        do the api call to the semantic database -> milvus
        query -> query_embedding -> milvus database
        '''

        # get the document embedding first
        transformed_query_dict = {QUERY: transformed_query}
        semantic_embedding_response = requests.post('http://query_embedder:8001/embed_query', json=transformed_query_dict)
        transformed_query_embeddings = semantic_embedding_response.json()['embed_query']
        # print(transformed_query_embeddings)
        # print(type(transformed_query_embeddings))
        # pass the response to milvus
        result = query_milvus(transformed_query_embeddings)

        return result

class SemanticProcessorEvaluation(QueryProcessor):

    def __init__(self) -> None:
        super().__init__()

    def get(self, transformed_query: str):
        '''
        do the api call to the semantic database -> milvus
        query -> query_embedding -> milvus database
        '''

        # get the document embedding first
        transformed_query_dict = {QUERY: transformed_query}
        semantic_embedding_response = requests.post('http://query_embedder:8001/embed_query', json=transformed_query_dict)
        transformed_query_embeddings = semantic_embedding_response.json()['embed_query']
        
        # pass the response to milvus
        result = query_milvus_evaluation(transformed_query_embeddings)

        return result
    
if __name__ == '__main__':

    # FOR TESTING

    # get the query from gateway - danieldoc
    query = 'hey hey you' # < 5 characters

    query_manager = QueryManager()
    intent = query_manager.intent_identifier.identify(query)
    transformed_query = query_manager.query_transformer.transform(query, intent)
    process = query_manager.query_process[intent]
    result_raw = process.get(transformed_query)

    # append the search query and the preprocessed query into the result dictionary
    result = {}
    result[SEARCH_QUERY] = query
    result[TRANSFORMED_QUERY] = transformed_query
    result[SEARCH_RESULT] = result_raw[SEARCH_RESULT]

    # return this result to gateway - daniel
    # print(result)