import requests
from bs4 import BeautifulSoup
import re
import json
import csv
import time

BASE_URL = "https://immovlan.be/en/real-estate"
PARAMS   = "transactiontypes=for-sale,in-public-sale&propertytypes=house,apartment"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}

PROVINCES = [
    "brussels",
    "antwerp",
    "east-flanders",
    "west-flanders",
    "flemish-brabant",
    "limburg",
    "liege",
    "hainaut",
    "namur",
    "luxembourg",
    "walloon-brabant",
]

session = requests.Session() #create a session
session.headers.update(HEADERS) #update headers


def build_url(province, page=1):
    page_param = f"&page={page}" if page > 1 else ""
    return f"{BASE_URL}?{PARAMS}&provinces={province}{page_param}&noindex=1"
    
    
def get_listing_urls(province, session):
    urls = [] # change this to a set for faster search
    
    for page in range(1, 51):
        url = build_url(province, page)
        
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.select("h2.card-title a[href]")
        
        for link in links:
            href = link.get("href")
            if href:
                urls.append(href)    
        time.sleep(0.2)              
    return urls

test = get_listing_urls("brussels", session)
print(test)