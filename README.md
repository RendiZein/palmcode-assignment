# Introduction

# Getting Started

There are 3 ways you can run it locally. The options are via conda environment, via docker hub, and google colab. But you must create your gemini api first
Link for create gemini api : [Gemini API](https://makersuite.google.com/app/apikey)

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

6. Copy your gemini ai api to `main.py` and save
7. Run the restapi

```
fastapi dev app/main.py
```

8. Open the local host

```
http://127.0.0.1:8000/
```

### Point

### Point

1. To start again as a new person

1.1. It's reccomended quit fast api with `ctrl+c`

1.2. Run fastapi again

```
fastapi dev app/main.py
```

1.3. This behavior because the agent is initiated when the `main.py` is ran.

2. The benefit using this way is

* You can watch the change of csv file

## Docker

1. Pull the docker hub.

```

```

2. Run the docker container.

```

```

3. Open the local host

```
http://127.0.0.1:8000/
```

### Point

2. The advantages and disadvantages using this way is

* You can't watch the change of csv file
* Simplest way to test the chatbot

## Colab (Inference)

Open the `agent_inference.ipynb`, click the google colab buton, then follow instruction.
