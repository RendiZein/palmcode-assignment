import json #convert output from model
import pandas as pd #handle csv file
import google.generativeai as genai #chatbot model

def extract_csv():
    csv_path="app/appointments.csv"
    df=pd.read_csv(csv_path)# store as pandas dataframe
    df=df.astype({'Name': 'string','Date': 'string','Start': 'string','End': 'string'})
    if len(df['Start'][0])>5:#for first time
        df['Start'] = df['Start'].apply(lambda x: x[0:-3]) 
        df['End'] = df['End'].apply(lambda x: x[0:-3])
    df['Date'] = pd.to_datetime(df['Date']) #convert to datetime
    #extract data for prompting agent
    df_copy=df.copy() #copy dataframe to prevent interference
    df_copy["hour"]=df_copy['Start']+" until "+df_copy['End']
    datas={}
    for date in df_copy["Date"].unique():
        ls=df_copy[df_copy["Date"]==date]["hour"].values.tolist()
        datas[date]=', '.join([str(elem) for elem in ls])
        datas[date]= "already booked at "+ datas[date]
    return datas, df, csv_path

def chating(chat,user_response,df, csv_path):
    bot_response = chat.send_message(user_response)
    bot_response = bot_response.text
    
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
        row_to_add=len(df.index)
        df.loc[row_to_add] = new_data
        df['Date'] = pd.to_datetime(df['Date'])
        df.to_csv(csv_path, index=False)
    return bot_response 