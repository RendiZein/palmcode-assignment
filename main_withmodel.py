from fastapi import FastAPI, Request #rest api
from fastapi.templating import Jinja2Templates #to conect with html
import os
import google.generativeai as genai #chatbot model
from fastapi.middleware.cors import CORSMiddleware #to handle fetch from html
import json #convert output from model
import pandas as pd #handle csv file

#connect to api
os.environ['GOOGLE_API_KEY'] = "GOOGLE_API_KEY"
genai.configure(api_key = os.environ['GOOGLE_API_KEY'])

#handle csv file
csv_path="appointments.csv"
df=pd.read_csv(csv_path)
df=df.astype({'Name': 'string','Date': 'string','Start': 'string','End': 'string'})
if len(df['Start'][0])>5:#for first time
    df['Start'] = df['Start'].apply(lambda x: x[0:-3])
    df['End'] = df['End'].apply(lambda x: x[0:-3])
df['Date'] = pd.to_datetime(df['Date'])
row_to_add=len(df.index)
df_copy=df.copy()
df_copy["hour"]=df_copy['Start']+" until "+df_copy['End']
datas={}
for date in df_copy["Date"].unique():
    ls=df_copy[df_copy["Date"]==date]["hour"].values.tolist()
    datas[date]=', '.join([str(elem) for elem in ls])
    datas[date]= "already booked at "+ datas[date]

#function to chatting with agent
def chating(user_response):
    # user_response=str(input())
    # print(f"User :\n{user_response}")
    bot_response = chat.send_message(user_response)
    bot_response = bot_response.text
    # print(f"Bot :\n{bot_response.text}")
    
    #check
    user_response=user_response.lower().strip() #prevent some miss
    if user_response == "i confirm my booking":
        model1 = genai.GenerativeModel('gemini-1.5-flash',
                                # Set the `response_mime_type` to output JSON
                                generation_config={"response_mime_type": "application/json"})

        prompt1 = """
        From text before if it's a confirmation .
        extract the name, date, start time, and finish time.
        Convert date to YYYY-MM-DD
        convert start time and finish time to 24 hour format.
        Using this JSON schema:
            Recipe = {"name": name, "date":date, "start_time":start time,"finish_time":finish time}
        Return a `Recipe`
            """
        new_data = model1.generate_content([bot_response, prompt1])
        new_data = json.loads(new_data.text)
        new_data=list(new_data.values())
        
        df.loc[row_to_add] = new_data
        df['Date'] = pd.to_datetime(df['Date'])
        df.to_csv(csv_path, index=False)
    return bot_response 
    
#initiate agent
# print("Bot : \nHello. Welcome to Example Inc. Do you want to book an appointment")
model = genai.GenerativeModel('gemini-1.5-flash')
prompt = """
        You are straight forward booking assistant of palm_surfing (surfing company) in bali.
        Be polite and humble.
        The current time is 7 am 20 july 2024.
        The surfing available from 08:00 until 19:00.
        Response in without any syntax.
        First :
                Ask name, date(YYYY-MM-DD), start time, finish time of user will book.
                dont give example.
        Second :
                check availiability from the booking data
                if available :
                        Confirm to the user about the name, date(YYYY-MM-DD), start time, finish time.
                        ask the user to type "i confirm my bookinf"
                if already booked:
                        Give the booking data of the day.
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
# print(f"User :\n{user_response}")
#give user response
bot_response = chat.send_message([f"The booked data {datas}. other time outside the booked data is available."\
        ,prompt, f"user response :{user_response}"])


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
async def chat_api(request: Request):
    user_response=await request.json()
    user_response=user_response['message']["content"]
    agent_response=chating(user_response)
    
    response={"message": {'content': agent_response}}
    return response


# async def handle_input(request: Request, user_input: str):
#     response_data = model.generate_content(user_input)
#     return templates.TemplateResponse("index.html", {"request": request, "response_data": response_data.text})

    