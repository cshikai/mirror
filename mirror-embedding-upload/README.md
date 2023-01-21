# mirror-embedding-upload

A service that listens to a Kafka topic (queue), generates embeddings and uploads embeddings to an embedding database.
Intended to run within a network of docker services. 

## Pre-conditions
Services:
- A kafka broker service running on {kafka-broker-hostname}:29092.
- A kafka producer service sending events to {kafka-broker-hostname}:29092.
- A running ElasticSearch db instance to store/retrieve document texts.
- A running Milvus db instance to store document embeddings.

Folder structure:
```
├───build
├───configs
├───models
│   ├───sup-simcse-roberta-base
|
└───src
    |───utils
```

`build/`: docker configs and python requirements.

`configs/`: there should be a config.yaml in here.

`models/`: the huggingface model (one folder per embedding model) folders should be in here.

`src/`: source code.

## To run
Enter the docker service running the EmbeddingService (currently this docker service is named "embedding-upload"),
`python src/EmbeddingService.py`

## How it works
1. The kafka consumer receives a `doc_id(str)` from the topic queue that signals this doc_id is ready to be queried.
1. EmbeddingService.py queries the text db (Elasticsearch) using this unique doc_id for the document text.
1. The document text is converted to an embedding with a text embedding model (wrapped by TextVectoriser).
1. The text embedding along with its Elasticsearch index is uploaded to a vector db (Milvus).

The embedding operation and upload operation can be batched for efficiency and this is controlled with `flush_period`
and  `batch_size` (see [Configs](#configs)).

## Embedding model
Currently, uses Simple Contrastive Sentence Embeddings (https://github.com/princeton-nlp/SimCSE)

Model checkpoint is from https://huggingface.co/princeton-nlp/sup-simcse-roberta-base

## Configs
In config.yaml, make sure to have the following fields under "embedding_upload_service".
```
embedding_upload_service:
  flush_period: 5   # max number of seconds before a non-empty text buffer
    # is flushed and its contents used to generate embeddings which are then uploaded to db.
  batch_size: 64  # number of documents to batch before generating embeddings and uploading to db.
```

