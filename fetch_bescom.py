import json
import requests
from bs4 import BeautifulSoup

url = 'https://nitter.net/bescomofficial'
headers = {'User-Agent': 'Mozilla/5.0'}
res = requests.get(url, headers=headers)

if res.status_code != 200:
    print("Failed to fetch from Nitter")
    exit(1)

soup = BeautifulSoup(res.text, 'html.parser')
tweets = []

for item in soup.select('.timeline-item')[:10]:  # Get top 10 tweets
    content = item.select_one('.tweet-content').text.strip()
    time_tag = item.select_one('a.tweet-date')
    tweet_url = 'https://nitter.net' + time_tag['href'] if time_tag else ''
    date = time_tag['title'] if time_tag and 'title' in time_tag.attrs else ''
    
    tweets.append({
        'content': content,
        'date': date,
        'url': tweet_url
    })

with open('tweets.json', 'w') as f:
    json.dump(tweets, f, indent=2)

print(f"✅ Scraped {len(tweets)} tweets from Nitter")
