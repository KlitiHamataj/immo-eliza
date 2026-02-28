# 🏠 Immovlan Real Estate Scraper

A web scraper for collecting real estate listings from [immovlan.be](https://immovlan.be/en) — targeting houses and apartments listed for sale across all Belgian provinces.

---

## 📋 Project Overview

This scraper collects property listings (houses & apartments for sale) from Immovlan across **all provinces**, paginating through pages filtered by price range to bypass the 50-page limit — yielding approximately **26,000 listings**.

---

## 🌐 Target URLs

| Parameter | Value |
|---|---|
| Base URL | `https://immovlan.be/en` |
| Transaction Types | `for-sale` |
| Property Types | `house`, `apartment` |
| Provinces | Brussels *(+ 10 others)* |
| Results per page | 20 |
| Pages per price range | up to 50 |

### URL Structure

```
# Page 1
https://immovlan.be/en/real-estate?transactiontypes=for-sale,in-public-sale&propertytypes=house,apartment&provinces={province}&noindex=1

# Page N (N > 1)
https://immovlan.be/en/real-estate?transactiontypes=for-sale,in-public-sale&propertytypes=house,apartment&provinces={province}&page={N}&noindex=1
```

> **Note:** To overcome the 50-page / 1,000 listing cap per query, the scraper segments requests by **price range**, collecting all pages within each segment and merging the results.

---

## 🗺️ Provinces Covered

| # | Province | URL Slug |
|---|---|---|
| 1 | Brussels | `brussels` |
| 2 | *(Province 2)* | `...` |
| 3 | *(Province 3)* | `...` |

---

## 📊 Scale

```
11 provinces
× multiple price range segments
× up to 50 pages per segment
× 20 listings per page
≈ 26,000 total listings
```

---

## 📁 Project Structure

```
├── 📁 data
│   ├── 📁 processed
│   │   └── 📄 listings.csv
│   └── 📁 raw
│       └── 📄 all_provinces_links.csv
├── 📁 src
│   ├── 🐍 config.py
│   ├── 🐍 parser.py
│   └── 🐍 scraper.py
├── ⚙️ .gitignore
├── 📝 README.md
├── 🐍 main.py
└── 📄 requirements.txt
```

---

## ⚙️ Configuration (`config.py`)

```python
BASE_URL = "https://immovlan.be/en/real-estate"

PROVINCES = ["brussels", "province-2", "province-3..."]

PARAMS = {
    "transactiontypes": "for-sale",
    "propertytypes": "house,apartment",
    "noindex": 1,
}

PRICE_RANGES = [
    (0, 100_000),
    (100_000, 200_000),
    (200_000, 300_000),
    (300_000, 500_000),
    (500_000, 750_000),
    (750_000, 9_999_999),
]

MAX_PAGES = 50
RESULTS_PER_PAGE = 20
REQUEST_DELAY = 1.5  # seconds between requests (be respectful)
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/KlitiHamataj/immo-eliza.git
cd immo-eliza
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the scraper

```bash
python main.py
```

---

## 📦 Dependencies

```txt
beautifulsoup4==4.14.3
certifi==2026.1.4
charset-normalizer==3.4.4
idna==3.11
lxml==6.0.2
python-dateutil==2.9.0.post0
pytz==2025.2
requests==2.32.5
six==1.17.0
soupsieve==2.8.3
typing_extensions==4.15.0
tzdata==2025.3
urllib3==2.6.3
```

---

## 📤 Output

Results are saved to `data/processed/listings.csv`. Below is the full schema with example values:

| Column | Type | Description | Example |
|---|---|---|---|
| `locality` | `str` | Postal code + city name | `7540 Kain` |
| `property_type` | `str` | High-level type | `House`, `Apartment` |
| `subtype` | `str` | Detailed subtype | `Villa`, `Apartment` |
| `price_eur` | `int` | Listing price in euros | `370000` |
| `type_of_sale` | `str` | Sale method | `for sale` |
| `num_rooms` | `float` | Number of bedrooms | `3.0` |
| `living_area_m2` | `float` | Living surface in m² | `130.0` |
| `fully_equipped_kitchen` | `float/None` | Kitchen fully equipped flag | `None`, `1.0` |
| `furnished` | `float/None` | Furnished flag | `None`, `1.0` |
| `terrace` | `float/None` | Terrace present flag | `1.0`, `None` |
| `terrace_area_m2` | `float/None` | Terrace area in m² | `None` |
| `garden` | `float/None` | Garden present flag | `1.0`, `0.0` |
| `garden_area_m2` | `float/None` | Garden area in m² | `None` |
| `land_surface_m2` | `float/None` | Total plot area in m² | `1328.0` |
| `num_facades` | `float/None` | Number of building facades | `4.0` |
| `swimming_pool` | `float/None` | Swimming pool flag | `None`, `1.0` |
| `state_of_building` | `str/None` | Condition of the property | `Normal`, `Good` |

### Sample rows

| locality | property_type | subtype | price_eur | type_of_sale | num_rooms | living_area_m2 | fully_equipped_kitchen | furnished | terrace | terrace_area_m2 | garden | garden_area_m2 | land_surface_m2 | num_facades | swimming_pool | state_of_building |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 7540 Kain | House | Villa | 370000 | for sale | 3.0 | 130.0 | None | None | 1.0 | None | 1.0 | None | 1328.0 | 4.0 | None | Normal |
| 6000 Charleroi | Apartment | Apartment | 104000 | for sale | 2.0 | 85.0 | None | 1.0 | 1.0 | None | 0.0 | None | None | None | None | Normal |

---
## Contributors: 
[Kliti Hamataj](https://github.com/KlitiHamataj/)
[Jonbes Ahmadzai](https://github.com/JonbeshAhmadzai) 
[Mohamed Toukane](https://github.com/modev-git)
[Fernand Gatera](https://github.com/ndinhoo)

---
## ⚠️ Disclaimer

This scraper is intended for **personal research and analysis** only. Always respect the website's `robots.txt` and Terms of Service. Add appropriate delays between requests to avoid overloading the server.


---
## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
