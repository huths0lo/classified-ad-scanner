#!/usr/bin/python3

#Version 1.0
#written by Huth S0lo - August 23, 2022

import requests
from bs4 import BeautifulSoup
from twilio.rest import Client
from twilio import twiml
from dotenv import load_dotenv
from datetime import datetime
from time import sleep

found_ads = []
all_items = []

load_dotenv()

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
    found_ads = []
    found_ads = classified_scan(found_ads)
    print(found_ads)
    total_items = len(found_ads)
    total_scans = 0
    new_finds = 0
    while True:
        total_scans += 1
        found_ads = classified_scan(found_ads)
        if len(found_ads) > total_items:
            print('add text alert here')
            print(found_ads)
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
                        found_ads.append(item)
    return found_ads



#run_scanner()