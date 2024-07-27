from fastapi import FastAPI, Request #rest api
from fastapi.templating import Jinja2Templates #to conect with html
import os
import google.generativeai as genai #chatbot model
from fastapi.middleware.cors import CORSMiddleware #to handle fetch from html
# import json #convert output from model
# import pandas as pd #handle csv file
from app.helper import * 

#connect to api
os.environ['GOOGLE_API_KEY'] = "AIzaSyA28x0G-6PFd3U5-T5V-VyiUIndIDYGLAo"
genai.configure(api_key = os.environ['GOOGLE_API_KEY'])

app = FastAPI()
templates = Jinja2Templates(directory="app/templates") 

# connect with fetch
origins = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "http://localhost:8080",
    "http://localhost"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#endpoint for ui
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

#extract data csv
datas, df, csv_path=extract_csv()

#initiate agent
model = genai.GenerativeModel('gemini-1.5-flash')
prompt = """
        You are straight forward booking assistant of palm_surfing (surfing company) in bali.
        Be polite and humble.
        The current time is 7 am 20 july 2024.
        The surfing available from 08:00 until 19:00.
        Response without any syntax.
        First :
                Ask name, date(YYYY-MM-DD), start time, finish time of user will book.
                dont give example.
        Second :
                check availiability from the booking data
                if available :
                        Confirm to the user about the name, date(YYYY-MM-DD), start time, finish time.
                        ask the user to type "i confirm my bookinf"
                if already booked:
                        Give the booking data of the day without private information (name).
                        Dont share private information like name from booked data.
        Third :
                Confirm to the user about the name, date(YYYY-MM-DD), start time, finish time.
                ask the user to type "i confirm my booking"
        Forth :
                if user type "i confirm my booking" :
                        show the `name`, date(YYYY-MM-DD), start time, finish time and say good bye
        """
chat = model.start_chat(history=[])
user_response="hello"
#give user response 
bot_response = chat.send_message([f"The booked data {datas}. other time outside the booked data is available."\
        ,prompt, f"user response :{user_response}"])   

#endpoint for chatting with agent
@app.post("/chat")
async def chat_api(request: Request):
    user_response=await request.json()
    user_response=user_response['message']["content"]
    agent_response=chating(chat,user_response,df, csv_path)
    response={"message": {'content': agent_response}}
    return response    