import requests
from bs4 import BeautifulSoup
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


PRICE_RANGES = [
    (0, 100000),
    (100000, 200000),
    (200000, 300000),
    (300000, 400000),
    (400000, 500000),
    (500000, 750000),
    (750000, 9999999),
]


# Instead of one big search per province
# Split into price ranges that each return < 1000 results


def build_url(province, page=1, min_price=None, max_price=None):
    price_param = ""
    if min_price is not None:
        price_param += f"&minprice={min_price}"
    if max_price is not None:
        price_param += f"&maxprice={max_price}"
    page_param = f"&page={page}" if page > 1 else ""
    return f"{BASE_URL}?{PARAMS}&provinces={province}{price_param}{page_param}&noindex=1"
    
    
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

        time.sleep(0.2)

    return urls


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

all_urls = collect_all_urls(session) #call the function

# save_to_txt funct
def save_to_txt(urls):
    with open("all_provinces_links", "w", encoding="utf-8") as file:
        for url in urls:
            file.write(f"{url} \n")
    print(f"File {file} created with {len(urls)} entries.")

save_to_txt(all_urls)