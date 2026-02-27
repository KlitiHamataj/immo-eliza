import requests
from bs4 import BeautifulSoup
import csv
import time
<<<<<<< HEAD
import random
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd

INPUT_FILE = "all_provinces_links"
OUTPUT_FILE = "listings.csv"
NUM_WORKERS = 10 # workers for threadpoolexec
=======
import re


INPUT_FILE = "all_provinces_links"
OUTPUT_FILE = "listings.csv"
>>>>>>> 2f6476f05414d4504449aa769803a6ea5039415d

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
<<<<<<< HEAD
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
=======
    )
>>>>>>> 2f6476f05414d4504449aa769803a6ea5039415d
}

COLUMNS = [
    "locality",
    "property_type",
    "subtype",
    "price_eur",
    "type_of_sale",
    "num_rooms",
    "living_area_m2",
    "fully_equipped_kitchen",
    "furnished",
    "terrace",
    "terrace_area_m2",
    "garden",
    "garden_area_m2",
    "land_surface_m2",
<<<<<<< HEAD
=======
    "plot_surface_m2",
>>>>>>> 2f6476f05414d4504449aa769803a6ea5039415d
    "num_facades",
    "swimming_pool",
    "state_of_building",
]

FIELD_MAP = {
    "number of bedrooms":        "num_rooms",
    "livable surface":           "living_area_m2",
    "kitchen equipment":         "fully_equipped_kitchen",
    "furnished":                 "furnished",
    "terrace":                   "terrace",
    "surface terrace":           "terrace_area_m2",
    "garden":                    "garden",
    "surface garden":            "garden_area_m2",
    "total land surface":        "land_surface_m2",
<<<<<<< HEAD
=======
    "surface area of the plot":  "plot_surface_m2",
>>>>>>> 2f6476f05414d4504449aa769803a6ea5039415d
    "number of facades":         "num_facades",
    "swimming pool":             "swimming_pool",
    "state of the property":     "state_of_building",
}

session = requests.Session()
session.headers.update(HEADERS)

APARTMENT_SUBTYPES = {"apartment", "studio", "penthouse", "duplex", "ground floor", "triplex", "loft"}
HOUSE_SUBTYPES = {"residence", "mixed building", "villa", "master house", "bungalow", "chalet", "mansion", "house"}

<<<<<<< HEAD
# read all urls
def load_urls(filename):
    with open(filename, "r", encoding="utf-8") as f:
        urls = [
            line.strip() for line in f
            if line.strip()
            and "/detail/" in line
            and "/projectdetail/" not in line   # filters projectdetail
        ]
    return urls

#fetch (used by each thread)
def fetch_page(url, session):
    try:
        response = session.get(url, timeout=15)
        if response.status_code != 200:
            print(f" Skipping {url} — status {response.status_code}")
            return None
        return response.text
    except requests.RequestException as e:
        print(f"  ✗ Could not fetch {url}: {e}")
        return None

# ─────────────────────────────────────────────
# Parse helpers
# ─────────────────────────────────────────────
=======

#fetch page
def fetch_page(url, session):
    try:
        response = session.get(url, timeout=15)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f" Could not fetch {url}: {e}")
        return None

# read all urls
def load_urls(filename):
    with open(filename, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip() and "/detail/" in line and "/projectdetail/" not in line] #to change in phase1
    return urls
>>>>>>> 2f6476f05414d4504449aa769803a6ea5039415d

def get_property_type(subtype):
    s = subtype.lower().strip()
    if s in APARTMENT_SUBTYPES:
        return "Apartment"
    elif s in HOUSE_SUBTYPES:
        return "House"
    else:
        return "Other"
    
    
def extract_price(soup):
    price = soup.select_one(".detail__header_price_data")
    if price:
<<<<<<< HEAD
        raw     = price.get_text(strip=True)
        cleaned =  re.sub(r"[^\d]", "", raw)
        return cleaned if cleaned else None
=======
        raw = price.get_text(strip=True)
        return re.sub(r"[^\d]", "", raw)
>>>>>>> 2f6476f05414d4504449aa769803a6ea5039415d
    return None 

def extract_locality(soup):
    locality = soup.select_one(".city-line")
    if locality:
        raw_locality_data = locality.get_text(strip=True)
<<<<<<< HEAD
        indexed_locality  = raw_locality_data
=======
        indexed_locality = raw_locality_data
>>>>>>> 2f6476f05414d4504449aa769803a6ea5039415d
        return indexed_locality
    return None

def extract_fields(soup):
<<<<<<< HEAD
    fields  = {}
=======
    fields = {}
>>>>>>> 2f6476f05414d4504449aa769803a6ea5039415d
    wrapper = soup.select_one(".general-info-wrapper")
    if not wrapper:
        return fields
    
    for div in wrapper.select(".data-row-wrapper > div"):
        h4 = div.select_one("h4")
<<<<<<< HEAD
        p  = div.select_one("p")
=======
        p = div.select_one("p")
>>>>>>> 2f6476f05414d4504449aa769803a6ea5039415d
        if h4 and p:
            label = h4.get_text(strip=True).lower()
            value = p.get_text(strip=True)
            if label in FIELD_MAP:
                clean_val = value.lower().strip()
<<<<<<< HEAD
                col        = FIELD_MAP[label]

                if col == "fully_equipped_kitchen":
                    fields[col] = 1
                elif clean_val == "yes":
                    fields[col] = 1
                elif clean_val == "no":
                    fields[col] = 0
=======
                col = FIELD_MAP[label]

                if col == "fully_equipped_kitchen":
                    fields[col] = True
                elif clean_val == "yes":
                    fields[col] = True
                elif clean_val == "no":
                    fields[col] = False
>>>>>>> 2f6476f05414d4504449aa769803a6ea5039415d
                elif any(char.isdigit() for char in clean_val):
                    num_only = re.sub(r"[^\d]", "", clean_val)
                    fields[col] = int(num_only) if num_only else None
                else:
                    fields[col] = value

    return fields    


def parse_listing(html, url):
    soup = BeautifulSoup(html, "html.parser")
    parts = url.split("/")
    
    data = {col: None for col in COLUMNS} #None for empty values
    
    #get type of sale
    data["type_of_sale"] = parts[6].replace("-", " ") if len(parts) > 6 else None
<<<<<<< HEAD
    #get price
    data["price_eur"] = extract_price(soup)
    #get locality
    data["locality"] = extract_locality(soup)
    
    
    data.update(extract_fields(soup))
    
    
    #get property type
    subtype_raw = parts[5] if len(parts) > 5 else None   
=======
    
    #get property type
    subtype_raw = parts[5] if len(parts) > 5 else None   
    
    #get price
    data["price_eur"] = extract_price(soup)

    #get locality
    data["locality"] = extract_locality(soup)

    #all other fields
    data.update(extract_fields(soup))
    
>>>>>>> 2f6476f05414d4504449aa769803a6ea5039415d
    if subtype_raw:
        subtype = subtype_raw.replace("-", " ").title()  
        data["subtype"] = subtype
        data["property_type"] = get_property_type(subtype)
<<<<<<< HEAD
    return data  

# ─────────────────────────────────────────────
# Worker — one thread runs this per URL
# ─────────────────────────────────────────────

def scrape_one(args):
    url, session, index, total = args
    print(f"  [{index}/{total}] Fetching: {url}")
    time.sleep(random.uniform(0.5, 1.0))
    
    html = fetch_page(url, session)
    if not html:
        return None
    data = parse_listing(html, url)
    print(f"  [{index}/{total}] ✓ {data['locality']} | {data['price_eur']}€ | {data['property_type']}")
    return data  

# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

def main():
    all_urls = load_urls(INPUT_FILE)[:100]   # remove [:100] to scrape everything
    total    = len(all_urls)
    print(f"Loaded {total} URLs — scraping with 10 threads")

    # Each thread gets its own session
    sessions = [requests.Session() for _ in range(NUM_WORKERS)]
    for s in sessions:
        s.headers.update(HEADERS)

    jobs = []
    for i, url in enumerate(all_urls):
        session = sessions[i % NUM_WORKERS]   # pick a session
        index   = i + 1              # display number
        jobs.append((url, session, index, total))


    all_data = []
    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        futures = [executor.submit(scrape_one, job) for job in jobs]
        for future in as_completed(futures):
            result = future.result()
            if result:
                all_data.append(result)

    # Save with pandas
    df = pd.DataFrame(all_data, columns=COLUMNS)
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig", na_rep="None")
    print(f"\nDone! {len(df)} listings saved to {OUTPUT_FILE}")


main()   
=======
    return data    

#just for testing. later implement pandas for rows and columns

#save one row to csv
def save_to_csv(data, file):
    writer = csv.DictWriter(file, fieldnames=COLUMNS)
    writer.writerow(data)
    file.flush
    
    
all_urls = load_urls(INPUT_FILE)[:50] #delete [:10] to get all lisitings
print(f"Loaded {len(all_urls)} URLs from {INPUT_FILE}")

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=COLUMNS)
    writer.writeheader()

    for i, url in enumerate(all_urls, 1):
        print(f"[{i}/{len(all_urls)}] {url}")

        html = fetch_page(url, session)
        if not html:
            continue

        data = parse_listing(html, url)
        save_to_csv(data, f)

        print(f"  ✓ {data['locality']} | {data['price_eur']}€ | {data['property_type']}")
        time.sleep(0.2)

print(f"\nDone! {len(all_urls)} listings saved to {OUTPUT_FILE}")    
>>>>>>> 2f6476f05414d4504449aa769803a6ea5039415d
