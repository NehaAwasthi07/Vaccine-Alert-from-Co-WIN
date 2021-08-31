import requests
import datetime
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from gmail import GMail, Message

# Function to hit URL and return results
def make_request():
    today = datetime.datetime.today().date()
    tomorrow = today + datetime.timedelta(days=1)
    tomm_date_str = tomorrow.strftime("%d-%m-%Y")
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=395&date=" + tomm_date_str
    headers = {'accept': 'application/json',
               'Accept-Language': 'hi_IN'}
    response = requests.get(url, headers=headers)
    results = response.json()
    results = results['centers']
    return results


# Parse results and return available slots
def check_available(results):
    available_slots = []
    for r in results:
        for s in r['sessions']:
            if (s['min_age_limit'] <= 18 and s['available_capacity_dose1']>0 and s['vaccine']=='COVISHIELD'):
                available_slots += [(r['name'], r['address'], r['pincode'], s['available_capacity_dose1'])]
            else:
                # print('No slots available')
                pass    
    return available_slots

# send email
def send_email(available_slots):
    email_text = ""
    for a in available_slots:
        email_text = email_text + a[0] + " : " + a[1] + " : " + str(a[2])+ " : " + str(a[3]) +'\n'
    # print('Slots found - ', available_slots)
    # send email using gmail package
    email, password = read_credentials()
    gmail = GMail(email, password)
    msg = Message('Vaccine Alert',to='nehawsth07@gmail.com',text=email_text)
    gmail.send(msg)

def read_credentials():
    filename = 'C:/Users/Dell/Desktop/Study/credentials.txt'
    email = None
    password = None
    with open(filename) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    email = content[0]
    password = content[1]
    return email, password
