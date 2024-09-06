<h1>eXAI Image Insights</h1>

-----
<h2> BACKEND </h2>

<h2> To run with Python Virtual Environment</h2>

- Clone the project

```
git clone https://github.com/Error-404-UCD/eXAI
```

```
cd eXAI/Backend
```

- Setup the virtual environment for backend (Discard if pyenv already created)

```
python -m venv pyenv
```

- Start the virtual environment

```
source pyenv/bin/activate
```

- Install the requirements

```
pip install -r requirements.txt
```

- In the backend directory create folders named data and models
- In models directory create another folder checkpoints
- Download and extract the datasets in the data folder such that the path would be example, data/Astronomy/galaxies_heic0007b.jpg
- Make sure that the datasets contain images that store classname_ in it's file name
- Start the server in the Backend folder so that the paths are correctly received in the main file

```
python app/server_launch.py
```

- Run unit tests with

```
python -m unittest discover -s tests
```


<h2> To run with Docker</h2>

- Clone the project

```
git clone https://github.com/Error-404-UCD/eXAI
```

```
cd eXAI/Backend
```

- Build the docker image

```
 docker build -t docker-exai . 
```

- Run the docker container. Here the port numbers are in the format > frontend_portnumber:docker_backend_portnumber. Make sure to write the frontend_port number in the React POST request URL (127.0.0.1:5000). HERE frontend_portnumber= 5000 and docker_backend_portnumber= 5000

```
 docker run -p 5000:5000 docker-exai  
```
- Wait for the model to train and the server to start. It will display a localhost URL. Note that the port number of this URL is connected to the exposed docker_backend_portnumber.

<h2> FRONTEND </h2>

- Change Directory to Frontend

```
cd Frontend
```

- Install NPM packages

```
npm install
```

- Start react server

```
npm start
```
-----
<h2> Download the datasets from here</h2>

- [MNIST](https://drive.google.com/file/d/1MwIyLK1h0iEi3Lfi9piRR7LNQf6gXXYT/view?usp=drive_link)

- [BONE MARROW](https://drive.google.com/file/d/1gwtnhsOOcuwlChL1HTofrDN69uHPreIJ/view?usp=drive_link)

- [ASTRONOMY](https://drive.google.com/file/d/14ueW-7m3HkjVIR1O2RjX3TPr_4ZS8Vh1/view?usp=drive_link)

-----
Refer Google Coding Style guide to push into repository

- Python (https://google.github.io/styleguide/pyguide.html)

- Javascript (https://google.github.io/styleguide/jsguide.html)

-----
Dataset sources
- Kaggle Astronomy (https://www.kaggle.com/datasets/subhamshome/esa-hubble-images-3-classes?resource=download)
- Kaggle Bone Marrow (https://www.kaggle.com/datasets/andrewmvd/bone-marrow-cell-classification)
- Kaggle MNIST (https://www.kaggle.com/datasets/scolianni/mnistasjpg)

AWS Setup Guide
- Setup Nginx as reverse proxy on EC2 instance (https://medium.com/@imageadhikari/setup-nginx-as-reverse-proxy-on-ec2-instance-3c6820b6467b)
