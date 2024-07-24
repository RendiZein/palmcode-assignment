from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import os
import google.generativeai as genai
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


os.environ['GOOGLE_API_KEY'] = "AIzaSyA28x0G-6PFd3U5-T5V-VyiUIndIDYGLAo"
genai.configure(api_key = os.environ['GOOGLE_API_KEY'])

model = genai.GenerativeModel('gemini-pro')

app = FastAPI()
templates = Jinja2Templates(directory="templates") 

# connect with fetch
origins = [
    "http://127.0.0.1:8000",
    "http://localhost:8000"
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request}) 

# @app.post("/chat")
# async def chat():
#     print()
#     return {"message": {'content': "rendi"}}

@app.post("/chat")
async def chat(request: Request):
    user_response=await request.json()
    user_response=user_response['message']["content"]
    agent_response=model.generate_content(user_response)
    agent_response=agent_response.text
    response={"message": {'content': agent_response}}
    return response


# async def handle_input(request: Request, user_input: str):
#     response_data = model.generate_content(user_input)
#     return templates.TemplateResponse("index.html", {"request": request, "response_data": response_data.text})

    