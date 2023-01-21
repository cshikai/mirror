FROM nvcr.io/nvidia/pytorch:20.12-py3


# # Keeps Python from generating .pyc files in the container
# ENV PYTHONDONTWRITEBYTECODE 1
# # Turns off buffering for easier container logging
# ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

ADD /upload_service/build /build

WORKDIR /build 

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y \
    && apt-get -y install make

RUN make

ADD ./upload_service /src

WORKDIR /src

# CMD ["uvicorn", "main:api", "--host", "0.0.0.0"]