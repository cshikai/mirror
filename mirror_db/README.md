# Mirror Database Repository

## Raw Text Database (Elasticsearch)
Ports:
- Elasticsearch: 9200
- Kibana: 5601

### Elastdocker
 Run:

 ```
 git submodule init
 git submodule update --recursive
 ```

 1. Initialize Elasticsearch Keystore and TLS Self-Signed Certificates

 ```
cd elastdocker
make setup
sudo sysctl -w vm.max_map_count=262144
```
2. Build elasticsearch
```
cd elastdocker
docker-compose build 
```

## Vector Database (Milvus)
Ports:
- 2379, 2380, 9000, 19530, 9091
