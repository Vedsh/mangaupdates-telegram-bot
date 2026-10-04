import json
import os
import feedparser
import requests

RSS_URL = "https://mangaupdates.com/rss"

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

SEEN_FILE = "seen.json"


def load_seen():
    if not os.path.exists(SEEN_FILE):
        return set()

    with open(SEEN_FILE, "r", encoding="utf-8") as f:
        return set(json.load(f))


def save_seen(seen):
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        json.dump(list(seen), f, ensure_ascii=False, indent=2)


def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": message,
            "disable_web_page_preview": True
        },
        timeout=30
    )

    response.raise_for_status()


feed = feedparser.parse(RSS_URL)
seen = load_seen()

new_items = []

for entry in feed.entries:
    entry_id = (
        entry.get("id")
        or entry.get("guid")
        or entry.get("link")
        or entry.get("title")
    )

    if entry_id not in seen:
        new_items.append((entry_id, entry))


if not seen:
    for entry_id, entry in new_items:
        seen.add(entry_id)

    save_seen(seen)
    print("Initial setup complete. Existing releases marked as seen.")
    exit()


for entry_id, entry in reversed(new_items):

    title = entry.get("title", "New Release")
    link = entry.get("link", "")

    message = f"""📚 NEW MANGA RELEASE

{title}

🔗 MangaUpdates:
{link}
"""

    send_telegram(message)
    seen.add(entry_id)


save_seen(seen)

print(f"New releases sent: {len(new_items)}")
