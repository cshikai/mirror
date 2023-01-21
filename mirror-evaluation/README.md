# mirror-evaluation
Sets up a evaluation service by passing the test/dev json file via calling the query service     
   
### src/read_queries_from_json.py
reads the test/dev set json files, calls the query service to get back the search result ids and append the values into the dictionary and return back to the evaluation service   