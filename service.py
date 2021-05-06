import requests
import json
import datetime
import numpy as np
import pandas as pd
from cowin import cowin_get
from datetime import datetime, date

def check_data(age, pincode):
    try:
        if int(age) >=0 and int(age) <= 150:
            if len(str(pincode)) >= 5:
                response = requests.get(f"https://api.postalpincode.in/pincode/"+pincode)
                read_json = json.loads(response.text)
                if read_json[0]['Status'] == 'Error':
                    return False, None, None
                return True,read_json[0]['PostOffice'][0]['Circle'],read_json[0]['PostOffice'][0]['District']
    except ValueError:
        return False, None, None


def get_date(x):
    return datetime.strptime(x, '%Y-%m-%d').strftime('%d-%m-%Y')

def age_limit(age):
    if age < 45:
        return 18
    else:
        return 45

def check_vaccine(pincode,age, start_date:datetime, fee_type:str, availability: str):
    return cowin_get(pincode, age_limit(int(age)), get_date(start_date), fee_type,availability)
    