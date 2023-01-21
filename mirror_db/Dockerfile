RUN apt-get update
RUN apt-get -y install python3-pip vim git
RUN apt-get -y install libfreetype-dev libfreetype6 libfreetype6-dev

RUN pip install -U pip
COPY requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir /mirror_db && mkdir /mirror_db/src && mkdir /mirror_db/configs
WORKDIR /mirror_db/src

CMD ["/bin/bash"]
