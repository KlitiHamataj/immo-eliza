def scrape_listing(url, province, session):
    response = session.get(url, timeout=15)
    soup = BeautifulSoup(response.text, "html.parser")
    pass