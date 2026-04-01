import requests
from bs4 import BeautifulSoup

def scrape_yellowpages(city, state, max_pages=2):
    results = []
    headers = {"User-Agent": "Mozilla/5.0"}
    city_clean = city.replace('-', '_')
    for page in range(1, max_pages+1):
        url = f"https://www.yellowpages.com/search?search_terms=dentists&geo_location_terms={city_clean}%2C+{state.upper()}&page={page}"
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            break
        soup = BeautifulSoup(resp.text, "html.parser")
        cards = soup.select('div.result')
        if not cards:
            break
        for card in cards:
            name = card.select_one('a.business-name span')
            phone = card.select_one('div.phones')
            address = card.select_one('div.street-address')
            results.append({
                "平台": "YellowPages",
                "姓名": name.text.strip() if name else "",
                "电话": phone.text.strip() if phone else "",
                "地址": address.text.strip() if address else ""
            })
    return results
