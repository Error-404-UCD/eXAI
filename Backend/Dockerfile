# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# install app dependencies
RUN apt-get update && apt-get install -y python3 python3-pip && apt install python3-venv -y
RUN apt-get install pkg-config -y
RUN apt install pkg-config libhdf5-dev -y
RUN pip install gdown
RUN apt-get install unzip

# install app
COPY . /exai

RUN pip install -r exai/requirements.txt

# Create a models folder and data folder
RUN mkdir -p exai/data

RUN mkdir -p exai/models/checkpoints

# Download the Datasets
RUN gdown --fuzzy "https://drive.google.com/file/d/14ueW-7m3HkjVIR1O2RjX3TPr_4ZS8Vh1/view?usp=sharing" -O exai/data/ 
RUN unzip exai/data/Astronomy.zip -d exai/data/Astronomy
RUN rm exai/data/Astronomy.zip

# final configuration

EXPOSE 5000
CMD ["python3", "/exai/app/server_launch.py"]
