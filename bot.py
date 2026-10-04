import feedparser

RSS_URL = "https://mangaupdates.com/rss"

feed = feedparser.parse(RSS_URL)

print("RSS STATUS")
print("==========")
print(f"Feed title: {feed.feed.get('title', 'Not found')}")
print(f"Total entries: {len(feed.entries)}")
print()

if feed.entries:
    print("Latest releases:")
    print("---------------")

    for i, entry in enumerate(feed.entries[:10], 1):
        print(f"{i}. {entry.get('title', 'No title')}")
        print(f"   Link: {entry.get('link', 'No link')}")
        print()
else:
    print("❌ No RSS entries found.")
