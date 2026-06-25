import requests
import time
import re
import os

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
INTERVAL = 120

SITES = {
    "Noriel": "https://www.noriel.ro/catalogsearch/result/?q=pokemon+tcg&in_stock=1",
    "BebeTei": "https://www.bebetei.ro/cauti/pokemon+tcg",
    "Krit": "https://www.krit.ro/cauta?q=pokemon+tcg",
    "Carturesti": "https://carturesti.ro/cautare/pokemon+tcg",
    "Smyk": "https://www.smyk.ro/search?q=pokemon+tcg",
    "LumeaJocurilor": "https://www.lumea-jocurilor.ro/search?q=pokemon+tcg",
    "TCGArena": "https://tcgarena.ro/search?q=pokemon+tcg",
    "LibHumanitas": "https://libhumanitas.ro/search?q=pokemon+tcg"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ro-RO,ro;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive"
}

def get_products(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        print(f"Status {url}: {r.status_code}", flush=True)
        matches = re.findall(r'<h2[^>]*>([^<]+)</h2>', r.text)
        if not matches:
            matches = re.findall(r'<h3[^>]*>([^<]+)</h3>', r.text)
        return [m.strip() for m in matches if len(m.strip()) > 3]
    except Exception as e:
        print(f"Eroare {url}: {e}", flush=True)
        return []

def send_telegram(msg):
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": msg})
    except Exception as e:
        print(f"Eroare Telegram: {e}", flush=True)

print("=== START MONITOR ===", flush=True)

prev = {}
for site, url in SITES.items():
    prev[site] = get_products(url)
    print(f"Start {site}: {len(prev[site])} produse", flush=True)

while True:
    time.sleep(INTERVAL)
    for site, url in SITES.items():
        current = get_products(url)
        new = [p for p in current if p not in prev[site]]
        if new:
            send_telegram(f"🎴 Pokemon NOU pe {site}!\n" + "\n".join(new))
        prev[site] = current
        print(f"Check {site}: {len(current)} produse", flush=True)
