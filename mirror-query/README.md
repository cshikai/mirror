# mirror-query
Sets up a qeury service which waits for a query from the gateway, and then preprocess the query and then pass the query to the databases for querying

### src/query.py
**The main script that contains all the logic for the querying**   
`QueryManager`: acts as the main class where the `api_service.py` will be called     
`IntentIdentifier`: to take in the query from the UI, and determines which database will be queried based on the characteristics of the query   
`QueryTransformer`: based on the intent (which database), decide what form of text transformations are needed to process the text query    
`LexicalProcessor` and `SemanticProcessor`: The processor classes where the query service will call the databases   
`LexicalProcessorEvaluation` and `SemanticProcessorEvaluation`: The processor classes where the query service will call the databases for evaluation    
   

### src/hs_functions.py & src/milvus_functions.py 
**The script where the query service will call the respective databases for a response**   
    
### src/api_service.py
**api service to wait for call from other services**    
   
**/query**   
to wait for the gateway to pass the query to the query service   
    
**/evaluate_es**    
to wait for the evaluation service to pass the query to the query service to return the evaluation result from the elasticsearch dataset    
    
**/evaluate_milvus**   
to wait for the evaluation service to pass the query to the query service to return the evaluation result from the milvus dataset    
  