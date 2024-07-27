# Getting Started

There are 2 ways you can run it locally. The options are via conda environment or via docker hub. But you must create your gemini api first.
Link for create gemini api : [Gemini API](https://makersuite.google.com/app/apikey)
or use my gemini api in email.

## Conda

These are the steps

1. Create conda environment with python spesific version
```
conda create -n palmcode_chatbot python=3.9
```

2. Activate environment
```
conda activate palmcode_chatbot
```

3. Clone this repository
```
git clone https://github.com/RendiZein/palmcode-assignment
```

4. Change the parrent directory
```
cd "palmcode-assignment"
```

5. Install required library
```
pip install -r requirements.txt
```

6. Copy your gemini ai api to `app/main.py` and save

7. Run the restapi
```
fastapi dev app/main.py
```

8. Open the local host
```
http://127.0.0.1:8000/
```


## Docker
1. Clone this repository
```
git clone https://github.com/RendiZein/palmcode-assignment
```

2. Change the parrent directory
```
cd "palmcode-assignment"
```

3. Build docker image.
```
docker build -t myimage .
```

2. Run the docker container.
```
docker run -d --name mycontainer -p 8000:8000 myimage
```

3. Open the local host
```
http://127.0.0.1:8000/
```

### advantages and disadvantages using Docker way is

* Cant see the change of csv files
* Simplest way to test the chatbot

