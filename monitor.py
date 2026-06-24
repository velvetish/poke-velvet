import requests
import time
import re
import os

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
INTERVAL = 30

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
