import json
import requests
from bs4 import BeautifulSoup

mirrors = [
    'https://nitter.privacydev.net',
    'https://nitter.poast.org',
    'https://nitter.pufe.org',
    'https://nitter.1d4.us',
    'https://nitter.unixfox.eu'
]

tweets = []
headers = {'User-Agent': 'Mozilla/5.0'}

for mirror in mirrors:
    try:
        url = f'{mirror}/bescomofficial'
        print(f"Trying {url}")
        res = requests.get(url, headers=headers, timeout=10)

        if res.status_code != 200:
            print(f"⚠️ {mirror} returned status {res.status_code}")
            continue

        soup = BeautifulSoup(res.text, 'html.parser')
        items = soup.select('.timeline-item')

        if not items:
            print(f"⚠️ No tweets found at {mirror}")
            continue

        for item in items[:10]:
            content_elem = item.select_one('.tweet-content')
            date_elem = item.select_one('a.tweet-date')

            content = content_elem.text.strip() if content_elem else ''
            date = date_elem['title'] if date_elem and 'title' in date_elem.attrs else ''
            tweet_url = mirror + date_elem['href'] if date_elem and 'href' in date_elem.attrs else ''

            tweets.append({
                'content': content,
                'date': date,
                'url': tweet_url
            })

        if tweets:
            print(f"✅ Successfully scraped from {mirror}")
            break  # stop trying once one mirror works

    except Exception as e:
        print(f"❌ Failed on {mirror}: {str(e)}")

if not tweets:
    print("❌ All mirrors failed. Exiting.")
    exit(1)

with open('tweets.json', 'w') as f:
    json.dump(tweets, f, indent=2)

print(f"✅ Saved {len(tweets)} tweets to tweets.json")
