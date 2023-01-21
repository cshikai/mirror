FROM nvcr.io/nvidia/pytorch:22.02-py3

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
&& apt-get -y install build-essential git apt-utils gcc libpq-dev python3-pip vim \
&& rm -rf /var/lib/apt/lists/*

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

#Installing dependencies
RUN pip install --no-cache-dir fastapi[all] transformers

#set work directory to the one where you will do your model training in
WORKDIR /query_embedder