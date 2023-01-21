

# Mirror
![System Overview](github.com/cshikai/mirror)

Basic Information Retrieval system designed for multimedia documents and future extensibility. 

The system allows users to carry out text-based search on a repository of multimedia documents including texts, audio, and images. The search itself has a multi-pronged approach that uses a combination of keyword, semantic and graphical techniques to retrieve the most relevant documents. Several ML services run in the back end to enable important information to be extracted from each document type, and indexed in a manner that is compatible across media types.

##   Service Description

### Upload Service
User-facing service that allows documents to be uploaded by the clients through a web browser. Documents uploaded are stored in the document database and triggers the relevant ML services to extract information for indexing.

### Inference Service(s)
Back end services that employ ML techniques to extract information from the documents.
Current supported service(s) are:

 - Text Embedding Generation - The current version uses a SimCSE RoBERTa model to generate embeddings
 - Entity Extraction - Utilizes JEREX model for joint Entity and Relationship Extraction
 
Future services to be implemented
 - ASR (Speech-to-Text)
 - Translation 
 - Caption Generation

### Query
User-facing service that returns users relevant documents based on search query. Responsible for query transformation, querying the relevant databases for different types of search, and collating the results before generating a unified search result.

# Individual Service Structure


    ├── README.md               <- The top-level README for developers using this project.
    |
    ├── build                   <- Folder that contains files for building the environment 
    │   ├── docker-compose.yml  <- docker-compose file for quickly building containers
    │   ├── Makefile            <- Makefile which will be ran when building the docker image
    │   └── requirements.txt    <- The requirements file for reproducing the analysis environment, e.g.
    │                           generated with `pip freeze > requirements.txt`
    │── Dockerfile              <- Dockerfile for building docker image (unfortunately it has to be in root for it to work)
    |
    ├── data                    <- Download data from clearml here
    |   ├── train        
    │   └── valid
    |     
    ├── models                  <- Download/load pretrained model/save trained model locally here
    |   ├── vgg        
    │   └── elmo
    |   └── trained_models      <- Folder that contains the trained model weights
    │       └── model_weights.ckpt     
    |
    ├── src                     <- Source code for use in this project.
    │   │
    │   ├── main.py             <- Code to run for task initialization,  sending to remote, download datasets, starting experimentation
    |   |
    │   ├── experiment.py       <- Experimentation defining the datasets, trainer, epoch behaviour and running training
    |   |
    │   ├── config
    |   │   ├── config.py       <- Boilerplate code for config loading.yaml   
    |   │   └── config.yaml     <- Configfile for parameters
    |   |
    │   ├── data                <- Scripts related to data procesing
    │   │   ├── dataset.py
    │   │   ├── postprocessing.py
    │   │   ├── preprocessing.py
    │   |   ├── transforms.py
    |   |   └── common          <- common reusable transformation modules
    |   │       └── transforms.py 
    │   │
    |   ├── model               <- Scripts related to module architecture
    |   │   ├── model.py        <- Main model file chaining together modules 
    |   │   └── modules         <- Folder containing model modules
    |   |       ├── common
    |   |       |   └── crf.py 
    |   |       ├── encoder.py           
    |   |       └── decoder.py           
    │   │
    │   └── evaluation          <- Scripts to generate evaluations of model e.g. confusion matrix etc.
    |       ├── visualize.py           
    |       └── common 
    |           └── metrics.py
    |
    ├── tests                   <- Folder where all the unit-tests are
    |
    ├── notebooks               <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                           the creator's initials, and a short `-` delimited description, e.g.
    │                           `1.0-jqp-initial-data-exploration`.
    |
    ├── docs                    <- A default Sphinx project; see sphinx-doc.org for details
    |
    ├── references              <- Data dictionaries, manuals, and all other explanatory materials.
    │
    │
    └── tox.ini                 <- tox file with settings for running tox; see tox.readthedocs.io


# Setting Up
Prerequisites:  Requires docker and docker-compose 

## Docker Compose

### Steps to commission a service in docker compose

Step 1: Build docker images for each service 
```
cd <repo of service>/build
docker build -t mirror-<service_name>:latest .
```
Step 2: Spin up containers for all services using docker-compose:

```
docker-compose up -d
```
