import requests
from bs4 import BeautifulSoup

def scrape_healthgrades(city, state, max_pages=2):
    results = []
    headers = {"User-Agent": "Mozilla/5.0"}
    for page in range(1, max_pages+1):
        url = f"https://www.healthgrades.com/dentistry-general-directory/{state}-{city}?pageNum={page}"
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            break
        soup = BeautifulSoup(resp.text, "html.parser")
        cards = soup.select('div.search-card-content')
        if not cards:
            break
        for card in cards:
            name = card.select_one('a span[data-qa-target="provider-name"]')
            phone = card.select_one('a[data-qa-target="provider-details-phone"]')
            address = card.select_one('p[data-qa-target="provider-details-address"]')
            results.append({
                "平台": "Healthgrades",
                "姓名": name.text.strip() if name else "",
                "电话": phone.text.strip() if phone else "",
                "地址": address.text.strip() if address else ""
            })
    return results
