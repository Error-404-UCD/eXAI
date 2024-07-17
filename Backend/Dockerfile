# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# install app dependencies
RUN apt-get update && apt-get install -y python3 python3-pip && apt install python3-venv -y
RUN apt-get install pkg-config -y
RUN apt install pkg-config libhdf5-dev -y
RUN pip install gdown
RUN apt-get install unzip
RUN apt-get clean


# Set the working directory
WORKDIR /exai

# Copy the application code
COPY . /exai

# Create and activate a virtual environment, and install Python dependencies
RUN python3 -m venv pyenv && \
    . pyenv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt


# Create a models folder and data folder
RUN mkdir -p data

RUN mkdir -p models/checkpoints

# Download the Datasets
# RUN gdown --fuzzy "https://drive.google.com/file/d/14ueW-7m3HkjVIR1O2RjX3TPr_4ZS8Vh1/view?usp=sharing" -O data/ 
# RUN unzip data/Astronomy.zip -d data/Astronomy
# RUN rm data/Astronomy.zip

RUN gdown --fuzzy "https://drive.google.com/file/d/1MwIyLK1h0iEi3Lfi9piRR7LNQf6gXXYT/view?usp=drive_link" -O data/ 
RUN unzip data/MNIST.zip -d data/MNIST
RUN rm data/MNIST.zip

# final configuration

EXPOSE 5000
CMD ["/exai/pyenv/bin/python3", "/exai/app/server_launch.py"]
