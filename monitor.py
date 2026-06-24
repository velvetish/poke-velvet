import requests
import time
import re
import os

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
INTERVAL = 300

SITES = {
    "Noriel": "https://www.noriel.ro/catalogsearch/result/?q=pokemon+tcg",
    "BebeTei": "https://comenzi.bebetei.ro/cauti/pokemon%20tcg?stoc=1",
    "Krit": "https://www.krit.ro/search?q=pokemon+tcg",
    "Carturesti": "https://carturesti.ro/cauta/pokemon+tcg",
    "Smyk": "https://www.smyk.ro/search?q=pokemon+tcg",
    "LumeaJocurilor": "https://www.lumea-jocurilor.ro/search?q=pokemon+tcg",
    "TCGArena": "https://tcgarena.ro/search?q=pokemon+tcg",
    "LibHumanitas": "https://libhumanitas.ro/search?q=pokemon+tcg"
}

def get_products(url):
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        matches = re.findall(r'<h2[^>]*>([^<]+)</h2>', r.text)
        if not matches:
            matches = re.findall(r'<h3[^>]*>([^<]+)</h3>', r.text)
        return [m.strip() for m in matches if len(m.strip()) > 3]
    except:
        return []

def send_telegram(msg):
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": msg})

prev = {}
for site, url in SITES.items():
    prev[site] = get_products(url)
    print(f"Start {site}: {len(prev[site])} produse")

while True:
    time.sleep(INTERVAL)
    for site, url in SITES.items():
        current = get_products(url)
        new = [p for p in current if p not in prev[site]]
        if new:
            send_telegram(f"🎴 Pokemon NOU pe {site}!\n" + "\n".join(new))
        prev[site] = current
        print(f"Check {site}: {len(current)} produse")
