import requests
from bs4 import BeautifulSoup
import csv
import time
import re


INPUT_FILE = "all_provinces_links"
OUTPUT_FILE = "listings.csv"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
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
    "plot_surface_m2",
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
    "surface area of the plot":  "plot_surface_m2",
    "number of facades":         "num_facades",
    "swimming pool":             "swimming_pool",
    "state of the property":     "state_of_building",
}

session = requests.Session()
session.headers.update(HEADERS)

APARTMENT_SUBTYPES = {"apartment", "studio", "penthouse", "duplex", "ground floor", "triplex", "loft"}
HOUSE_SUBTYPES = {"residence", "mixed building", "villa", "master house", "bungalow", "chalet", "mansion", "house"}


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
        raw = price.get_text(strip=True)
        return re.sub(r"[^\d]", "", raw)
    return None 

def extract_locality(soup):
    locality = soup.select_one(".city-line")
    if locality:
        raw_locality_data = locality.get_text(strip=True)
        indexed_locality = raw_locality_data
        return indexed_locality
    return None

def extract_fields(soup):
    fields = {}
    wrapper = soup.select_one(".general-info-wrapper")
    if not wrapper:
        return fields
    
    for div in wrapper.select(".data-row-wrapper > div"):
        h4 = div.select_one("h4")
        p = div.select_one("p")
        if h4 and p:
            label = h4.get_text(strip=True).lower()
            value = p.get_text(strip=True)
            if label in FIELD_MAP:
                clean_val = value.lower().strip()
                col = FIELD_MAP[label]

                if col == "fully_equipped_kitchen":
                    fields[col] = True
                elif clean_val == "yes":
                    fields[col] = True
                elif clean_val == "no":
                    fields[col] = False
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
    
    #get property type
    subtype_raw = parts[5] if len(parts) > 5 else None   
    
    #get price
    data["price_eur"] = extract_price(soup)

    #get locality
    data["locality"] = extract_locality(soup)

    #all other fields
    data.update(extract_fields(soup))
    
    if subtype_raw:
        subtype = subtype_raw.replace("-", " ").title()  
        data["subtype"] = subtype
        data["property_type"] = get_property_type(subtype)
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