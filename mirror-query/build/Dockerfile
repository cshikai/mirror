#from docker image of python 3.8 build a new image
FROM python:3.8.12-slim-buster

#using root access
USER root

#set environment to singapore and update local time
ENV TZ=Asia/Singapore
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

#Downloading dependencies 
#that is, dependencies on linux
RUN apt-get update \
&& apt-get upgrade -y \
&& apt-get install -y \
&& apt-get -y install build-essential git apt-utils gcc libpq-dev libsndfile1 ffmpeg sox wget youtube-dl python3-pip vim \
&& rm -rf /var/lib/apt/lists/*

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

#Installing dependencies
#this set of dependencies are the libraries you import in python
#eg. from transformer import Wav2Vec2FeatureExtractor, you are using transformer library
#add such libraries to requirements.txt for easy downloading of dependencies into a new image
#if you add new libraries to your project that are not in default Python package, 
#run docker-compose up --build -d (with sudo if you are doing as admin) to rebuild image
#use sudo docker system prune to remove images with repo name: <none>
ADD requirements.txt .
RUN pip uninstall -y -r requirements.txt --no-cache-dir
RUN pip install -r requirements.txt --no-cache-dir

#set work directory to the one where you will do your model training in
WORKDIR /query_manager