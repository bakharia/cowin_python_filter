from datetime import datetime, date, timedelta
import time
import requests
import numpy as np
import pandas as pd
import json

def convert_time(date_str):
  time_value = datetime.strptime(date_str, '%I:%M%p').time()
  return time_value

def cowin_get(pincode:str, age_limit:int, start_date: datetime, fee_type:str, availability:str):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Authorization": "Bearer 1234"}
    response = requests.get(f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pincode}&date={start_date}", headers = headers) 
    read_json = response.json()   
    if 'Forbidden' in read_json.values():
      print(f'Message is forbidden, fetch is being blocked for PIN: {pincode} and Date: {date} - {read_json}')
    elif [] in read_json.values():
      print(f'Fetch successful, no vaccination centres available for PIN: {pincode} and Date: {date}  - {read_json}')
    else:
        centers = pd.DataFrame(read_json.get('centers'))
        list_sessions = []
        for j, row in centers.iterrows():
            session = pd.DataFrame(row['sessions'][0])
            session['center_id'] = centers.loc[j, 'center_id']
            list_sessions.append(session)
        sessions = pd.concat(list_sessions, ignore_index=True)
        session_center = centers.merge(sessions, on='center_id')
        session_center.drop(columns=['sessions', 'session_id'], inplace=True)
        if availability.lower() == 'stock':
            session_center = session_center[session_center['available_capacity'] > 0]
        if fee_type.lower() == 'paid':
            session_center = session_center[session_center['fee_type'] == 'Paid']
        elif fee_type.lower() == 'free':
            session_center = session_center[session_center['fee_type'] == 'Free']
        
        if age_limit == 18:
            session_center = session_center[session_center['min_age_limit'] == 18]
        elif age_limit == 45:
            session_center = session_center[session_center['min_age_limit'] == 45]

        if not session_center.empty:
            session_center[['start', 'finish']] = session_center['slots'].str.split('-', expand=True)
            session_center['start'] = session_center['start'].apply(lambda x: convert_time(x))
            session_center['finish'] = session_center['finish'].apply(lambda x: convert_time(x))

            # print(session_center.columns)
            return session_center.sort_values(by=['date','start','available_capacity'])
        # print(session_center)
        return session_center


def cowin_schedule():
    #/v2/appointment/schedule
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    body = {
            "dose": 1,
            "session_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "slot": "FORENOON",
            "beneficiaries": [
                "1234567890123",
                "9876543210987"
            ]
        }
    response = requests.get(f"https://cdn-api.co-vin.in/api/v2​/appointment​/schedule", headers = headers) 
    read_json = response.json()
    print(read_json)

# def cowin_otp():
#     #curl -X POST "https://cdn-api.co-vin.in/api/v2/auth/generateOTP" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"mobile\":\"9876543210\"}"
#     response = requests.post("https://api.demo.co-vin.in/api/v2/auth/generateOTP", 
#                                 data = {'mobile': '9113598549'},
#                                 headers={
#                                     'content-type':'application/json',
#                                     "accept": "application/json",
#                                     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
#                                     'x-api-key' : '3sjOr2rmM52GzhpMHjDEE1kpQeRxwFDr4YcBEimi'
#                                     },
#                                 params = {'mobile': '9113598549'}
#                             )
#     print(response)
if __name__ == '__main__':
    #cowin_get(201301,18,date(2021,5,6).strftime('%d-%m-%Y'), 'All', 'All')
    cowin_otp()



