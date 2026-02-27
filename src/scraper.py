import requests
from bs4 import BeautifulSoup

import time
import random
from src.config import BASE_URL, PARAMS, HEADERS, PROVINCES, PRICE_RANGES


session = requests.Session() #create a session
session.headers.update(HEADERS) #update headers


# Constructs and returns the precise target URL by injecting province, page, and price parameters.
def build_url(province, page=1, min_price=None, max_price=None):
    price_param = ""
    if min_price is not None:
        price_param += f"&minprice={min_price}"
    if max_price is not None:
        price_param += f"&maxprice={max_price}"
    page_param = f"&page={page}" if page > 1 else ""
    return f"{BASE_URL}?{PARAMS}&provinces={province}{price_param}{page_param}&noindex=1"
    
# Scrapes all listing URLs for one province and one price range
def get_listing_urls(province, session, min_price=None, max_price=None):
    urls = []

    for page in range(1, 51):
        url      = build_url(province, page, min_price, max_price)
        response = session.get(url, timeout=15)
        soup     = BeautifulSoup(response.text, "html.parser")
        links    = soup.select("h2.card-title a[href]")

        if not links:
            break

        for link in links:
            href = link.get("href")
            if href and "/projectdetail/" not in href:
                urls.append(href)

        time.sleep(random.uniform(0.1, 0.3)) # changed to 0.3 because 0.2 got blocked

    return urls

# Collects listing URLs for all provinces and price ranges
def collect_all_urls(session):
    all_urls = []

    for province in PROVINCES:
        for min_price, max_price in PRICE_RANGES:
            print(f"Scraping links for: {province} | {min_price}€ - {max_price}€ ...")

            province_urls = get_listing_urls(province, session, min_price, max_price)
            print(f"Collected {len(province_urls)} from {province} {min_price}-{max_price}")

            all_urls.extend(province_urls)

    all_urls = list(set(all_urls))
    print(f"Done! Collected {len(all_urls)} links in total.")
    return all_urls

# Saves all collected URLs into a text file
def save_to_txt(urls):
    with open("all_provinces_links", "w", encoding="utf-8") as file:
        for url in urls:
            file.write(f"{url} \n")
    print(f"File {file} created with {len(urls)} entries.")

