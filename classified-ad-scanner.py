#!/usr/bin/python3

#Version 1.0
#written by Huth S0lo - August 23, 2022

import requests
from bs4 import BeautifulSoup
from twilio.rest import Client
from dotenv import load_dotenv
from datetime import datetime
from time import sleep
import os

load_dotenv()


account_sid = os.getenv('account_sid')
auth_token = os.getenv('auth_token')
client = Client(account_sid, auth_token)
sms_number = os.getenv('sms_number')
to_number = os.getenv('to_number')

found_ads = []
all_items = []



search_criteria = {
    'spektrum': {
        'https://www.rcgroups.com/aircraft-general-radio-equipment-fs-w-215/',
        'https://www.helifreak.com/forumdisplay.php?f=51'
    },
    'sab': {
        'https://www.rcgroups.com/aircraft-electric-helis-fs-w-44/',
        'https://www.helifreak.com/forumdisplay.php?f=88'
    }
}


def run_scanner():
    global total_scans
    total_scans = 0
    new_finds = 0
    found_ads = []
    found_ads = classified_scan(found_ads)
    startup = 'Ad scanner started'
    send_text(to_number, startup)
    print(found_ads)
    total_items = len(found_ads)
    while True:
        total_scans += 1
        found_ads = classified_scan(found_ads)
        if len(found_ads) > total_items:
            new_finds += (len(found_ads) - total_items)
            total_items = len(found_ads)
        current_time = datetime.now().strftime("%m-%d-%Y_%Hh%Mm%Ss")
        print(f'Total Scans = {total_scans}.  Found since startup = {new_finds}.  Current Time = {current_time}')
        sleep(60)




def classified_scan(found_ads):
    for key, value in search_criteria.items():
        search_term, urls = key, value
        for url in urls:
            reqs = requests.get(url)
            soup = BeautifulSoup(reqs.text, 'lxml')
            all_items = []
            for heading in soup.find_all(["h1", "h2", "h3"]):
                heading_name = heading.text.strip()
                all_items.append(heading_name.lower())
            for item in all_items:
                if search_term in item:
                    if item not in found_ads:
                        if total_scans != 0:
                            message_body = f'A new "{item}" found'
                            send_text(to_number, message_body)
                        found_ads.append(item)
    return found_ads



def send_text(to_number, message_body):
    message = client.messages.create(body=message_body, from_=sms_number, to=to_number)
    print(message.sid)


#run_scanner()