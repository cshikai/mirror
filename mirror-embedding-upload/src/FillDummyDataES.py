# Connect to Elasticsearch
from haystack.document_stores import ElasticsearchDocumentStore
from clearml import Dataset
import pandas as pd
from typing import List, Dict

# Connect to Elasticsearch
document_store = ElasticsearchDocumentStore(
    host="localhost",
    port="9200",
    username="elastic",
    password="dh123",
    index="wikir9k",
)
document_store.delete_all_documents()

def ingest_csv_hs(_index:str, dataset_project:str, dataset_name:str, csv_filename:str, col_name:str, nrows: int)->List[Dict]:
    #ds = Dataset.get(dataset_project = dataset_project, dataset_name=dataset_name)
    #filepath=f"{ds.get_local_copy()}/{csv_filename}"
    #docs = pd.read_csv(filepath, nrows=nrows)
    #doc_list = docs[col_name].values.tolist()
    dict_list = [{'content': f"hello this is test data {i}"} for i in range(10)]
    document_store.write_documents(dict_list, batch_size=100)


ingest_csv_hs(_index="wikir9k", dataset_project= "incubation/dataset/wikIR59k", dataset_name="documents", csv_filename="documents.csv", col_name="text_right", nrows=100)
doc_list = document_store.get_all_documents()
print(f"doc count: {len(doc_list)}")
print()
print(doc_list[0])
# document_store.delete_all_documents()