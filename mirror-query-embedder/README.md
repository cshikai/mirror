# Text Embeddings for Haystack and beyond.

A module to convert a given text passage into a vector.

## Setup/Installs

install PyTorch: https://pytorch.org/get-started/locally/

install Docker (this is for containerizing the ElasticSearch instance)

`python -m pip install --upgrade pip` (make sure it's the latest pip to ensure dependencies are resolved correctly).

then `pip install -r requirements.txt`.

or

`pip install farm-haystack`

`pip install boto3` (needed for ClearML access to S3)

`pip install clearml`


### Setting up ElasticSearch instance and API endpoints on a Docker container.

git clone https://github.com/achew012/es-ie

`docker-compose up` (init docker container using docker-compose.yaml)

#### to test whether ES instance is running
Navigate any browser to `localhost:9200` 

And you should see something that looks like this:

```
{
  "name" : "dbe6efde5019",
  "cluster_name" : "docker-cluster",
  "cluster_uuid" : "Pbn0DXBJRF-38oum0nYyhw",
  "version" : {
    "number" : "8.2.0",
    "build_flavor" : "default",
    "build_type" : "docker",
    "build_hash" : "b174af62e8dd9f4ac4d25875e9381ffe2b9282c5",
    "build_date" : "2022-04-20T10:35:10.180408517Z",
    "build_snapshot" : false,
    "lucene_version" : "9.1.0",
    "minimum_wire_compatibility_version" : "7.17.0",
    "minimum_index_compatibility_version" : "7.0.0"
  },
  "tagline" : "You Know, for Search"
}
```


#### Accessing ElasticSearch instance from HayStack

`document_store = ElasticsearchDocumentStore()`

Refer to Haystack's API docs for how to interact with the document_store.

Make sure to `pip install python-magic` and `pip install python-magic-bin`.

### Setting up ClearML (once only)

`clearml-init`

Then follow instructions to get the clearml credentials. Input the clearml credentials and a clearml.conf 
config file will be generated at a default location.

Set up S3 credentials. Go to the generated clearml.conf file and edit the s3 portion with the s3 credentials.


#### Load ClearML dataset into ElasticSearch via HayStack

```
from clearml import Dataset
ds = Dataset.get(dataset_project="incubation/dataset/wikIR59k", dataset_name="documents")
path = ds.get_local_copy()

import pandas as pd
df = pd.read_csv(f"{path}/documents.csv", nrows=1000)

# convert each doc in the dataset to the Haystack format.
<Dinghan to fill>

# use Haystack API to add docs to ElasticSearch
<Dinghan to fill>
```

## Using this package 


### Customizing Haystack's Retriever behaviour with CustomRetriever and TextVectoriser.

See `UpdateEmbeddings.py` for an example :).


### Using the TextVectoriser

```
from TextVectoriser import TextVectoriser

PATH = "models/sup-simcse-roberta-large"  # path to Huggingface model dir.
text_vec = TextVectoriser.TextVectoriser(PATH)

queries = ["this is a test query 1.", "this is a test query 2."]

vectors = text_vec.compute_vector(queries)
```
