import pandas as pd
from haystack import Document
from haystack.document_stores import ElasticsearchDocumentStore

document_store = ElasticsearchDocumentStore(
                host='elasticsearch',
                username='elastic',
                password='dh123',
                index='documents',
                embedding_dim = 1024,
                create_index=True, # True to init new index
                recreate_index = False,
            )

input_df = pd.read_csv('subset.csv')
doc_list = input_df['text'].values.tolist()
dict_list = [{'content': text,} for text in doc_list] 
document_store.write_documents(dict_list, batch_size=10000, index='documents')