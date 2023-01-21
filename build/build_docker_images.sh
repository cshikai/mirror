# build gateway
cd gateway/build
docker build -t mirror/gateway:latest .
cd ../..

# build databases
cd mirror_db/build

# ...

cd ../..

# build query service
cd mirror-query/docker
docker build -t mirror/query_service:latest .
cd ../..

# build upload service
cd mirror-upload_service/build
docker build -t mirror/upload_service:latest .

