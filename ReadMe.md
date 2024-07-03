- eXAI Image Insight

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
- Create folders named data and models
- In models directory create another folder checkpoints
- Download and extract the datasets in the data folder such that the path would be example, data/Astronomy/galaxies_heic0007b.jpg
- Make sure that the datasets contain images that store classname_ in it's file name
- Start the server in the Backend folder
```
python3 app/server_launch.py
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

- Run the docker container. Here the port numbers are in the format > frontend_portnumber:docker_backend_portnumber. Make sure to write the frontend_port number in the React POST request URL (127.0.0.1:8000). Currently frontend_portnumber: 8000 and docker_backend_portnumber: 5000
```
 docker run -p 8000:5000 docker-exai  
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
Refer Google Coding Style guide
- Python (https://google.github.io/styleguide/pyguide.html)
- Javascript (https://google.github.io/styleguide/jsguide.html)