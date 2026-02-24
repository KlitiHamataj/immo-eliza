import requests
from bs4 import BeautifulSoup
import re
import json
import csv
import time
import pandas as pd

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
    "vlaams-brabant",
    "limburg",
    "liege",
    "hainaut",
    "namur",
    "luxembourg",
    "brabant-wallon",
]



session = requests.Session() #create a session
session.headers.update(HEADERS) #update headers




def build_url(province, page=1):
    page_param = f"&page={page}" if page > 1 else ""
    return f"{BASE_URL}?{PARAMS}&provinces={province}{page_param}&noindex=1"
    
    
def get_listing_urls(province, session):
    urls = []
    
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


all_urls = []

# This loop moves to the next province automatically
for province in PROVINCES:
    print(f"Scraping links for: {province}...")

    province_urls = get_listing_urls(province, session)
    print(f"Collected {len(province_urls)} from {province}")
    
    all_urls.extend(province_urls)

print(f"Done! Collected {len(all_urls)} links in total.")




