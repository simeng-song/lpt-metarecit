import requests
import json
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL = "http://search.people.cn/search-platform/front/search"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json;charset=utf-8",
    "Origin": "http://search.people.cn",
}

def fetch_page(page_no):
    payload = {
        "key": "人类命运共同体",
        "page": page_no,
        "limit": 20,
        "hasTitle": True,
        "hasContent": True,
        "isFuzzy": False,
        "type": 7,
        "domain": "cpc.people.com.cn",
        "sources": None,
        "sortType": 0,
        "startTime": 0,
        "endTime": 0
    }
    r = requests.post(URL, headers=HEADERS, data=json.dumps(payload))
    return r.json()

def parse_article(url):
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        r.encoding = "utf-8"
    except Exception as e:
        print("Erreur:", url)
        return {}
    soup = BeautifulSoup(r.text, "html.parser")
    data = {}

    # Titre
    h1 = soup.find("h1")
    data["full_title"] = h1.get_text(strip=True) if h1 else ""

    # Auteur
    author = soup.find("p", class_="sou1")
    data["author"] = author.get_text(strip=True) if author else ""

    # Date et source
    sou = soup.find("p", class_="sou")
    data["meta"] = sou.get_text(" ", strip=True) if sou else ""

    # Contenu
    content_div = soup.find("div", class_="show_text")
    paragraphs = []
    if content_div:
        for p in content_div.find_all("p"):
            text = p.get_text(" ", strip=True)
            if text:
                paragraphs.append(text)
    data["full_content"] = "\n".join(paragraphs)

    edit = soup.find("div", class_="edit")
    data["editor"] = edit.get_text(strip=True) if edit else ""

    return data

def crawl_all():
    page = 1
    all_results = []

    MAX_PAGES = 80

    while True:
        if page > MAX_PAGES:
            print(f"\nArrivé à {MAX_PAGES}")
            break

        data = fetch_page(page)
        results = data.get("data", {}).get("records", [])

        if not results:
            print("Pas d'autres page")
            break

        for item in results:
            url = item.get("url")

            record = {
                "title": item.get("title"),
                "url": url,
                "summary": item.get("content"),
                "pubTime": item.get("pubTime"),
                "source": item.get("source"),
            }

            detail = parse_article(url)
            record.update(detail)

            all_results.append(record)

            time.sleep(0.3)

        page += 1
        time.sleep(0.5)

    return all_results

if __name__ == "__main__":
    data = crawl_all()
    print(f"\n {len(data)} articles sont récupérés")

    with open("corpus.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Enreigistré dans corpus.json")