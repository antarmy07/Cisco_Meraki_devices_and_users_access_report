#!/usr/bin/env python

import gspread
import sys, os
import requests
import json
import time
import datetime
from time import sleep
from oauth2client.service_account import ServiceAccountCredentials
import boto3
import botocore
import gspread_formatting
from gspread_formatting import *

#fetch Google api key from the encrypted S3 bucket
def get_api_key ():
    os.system('sh ./decryptingkey.sh')

def main ():
    #get Google and meraki api key from the encrypted S3 bucket and decrypts after download using local aws .config
    get_api_key ()

    #setup date and time for new sheets tittle
    date = datetime.datetime.now()
    date = date.strftime('%d/%m/%Y')
    wks_title = print(""'"'+date+""'"')   
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('./key/gspread-apikey.json', scope)
    gc = gspread.authorize(credentials)   
    wks = gc.open('Meraki User and OS Access Report') # name of the google spreadsheet can be changed to suite your choice of sheet name
    worksheet = wks.add_worksheet(title=date, rows="200", cols="20") #creates the new sheet in the spreadsheet  
    wks = wks.worksheet(date)
    wks.append_row(['id', 'Device Name', 'OS Name', 'Last User Connected'])

    #formats the tittle column to selected highlight colour
    fmt = cellFormat(
        backgroundColor=color(1, 0.9, 0.9),
        textFormat=textFormat(bold=True, foregroundColor=color(1, 0, 1)),
        horizontalAlignment='CENTER'
        )
    format_cell_range(worksheet, 'A1:D1', fmt)
    
    #get the meraki user and device data from DigitalSurgerMobile network
    meraki_key=open("./key/meraki_apikey.txt")
    mkey=meraki_key.read()
    api_key = (mkey)
    url = 'https://api.meraki.com/api/v0/networks/<Meraki MDM network ID>/sm/devices?fields=lastUser&scope=withAll,<MDM tag name for all devices>'
    meraki_headers = {'x-cisco-meraki-api-key': api_key, 'content-type': 'application/json'}
    r = requests.get(url, headers=meraki_headers)
    json_output = json.loads(r.text)
   
    #for all the data received from meraki append in the new sheet of the day
    for f in json_output["devices"]:
        deviceID = (str(f['id']))
        deviceName = (str(f['name']))
        deviceOSname = (str(f['osName']))
        deviceLastUser = (str(f['lastUser']))
        id = (deviceID)
        name = (deviceName)
        osName = (deviceOSname)
        lastuser = (deviceLastUser)
        wks.append_row([id, name, osName, lastuser]) 
        time.sleep(10)
    else:

    #remove the decrypted api keys from the folder
        os.remove("./key/meraki_apikey.txt")
        os.remove("./key/gsuite-apikey.json")
        os.remove("./key/<MerakiApiKey>")
        os.remove("./key/<GSuite-ApiKey>")

main ()