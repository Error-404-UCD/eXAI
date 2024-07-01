# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# install app dependencies
RUN apt-get update && apt-get install -y python3 python3-pip && apt install python3-venv -y
RUN apt-get install pkg-config -y
RUN apt install pkg-config libhdf5-dev -y
RUN pip install gdown

# install app
COPY . /exai

RUN pip install -r exai/requirements.txt

# Create a models folder and data folder
RUN mkdir -p exai/data

RUN mkdir -p exai/models/checkpoints

# Download the Datasets
RUN gdown "https://drive.google.com/drive/folders/19RAzLHb2aUOtYxh-EYNfcipZNp8AEHu0?usp=drive_link" --folder -O exai/data/ --remaining-ok
# final configuration

EXPOSE 5000
CMD ["python3", "/exai/app/server_launch.py"]
