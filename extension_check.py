import aiohttp
import asyncio
import csv
import datetime
import requests
import time
import sys

def get_bearer_token():
    payload = {'client_id': 'YOUR_CS_CLIENT_ID', 'client_secret': 'YOUR_SECRET'}
    headers = {'accet': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}

    r = requests.post("https://api.crowdstrike.com/ouath2/token", params=payload, headers=headers)

    token = r.json()['access_token']
    formattedToken = "Bearer" + " " + token
    headers = {'accept': 'application/json', 'authorization': formattedToken}

    print("Obtained Crowdstrike bearer token")
    return headers


