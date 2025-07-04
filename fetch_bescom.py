import json
import subprocess

query = 'from:bescomofficial'
cmd = ['snscrape', '--jsonl', '--max-results', '10', f'twitter-search {query}']
result = subprocess.run(cmd, capture_output=True, text=True)

# 🔍 Check if scraping failed
if result.returncode != 0:
    print("snscrape failed:", result.stderr)
    exit(1)

lines = result.stdout.strip().split('\n')
tweets = []

for line in lines:
    if not line.strip():  # skip empty lines
        continue
    try:
        tweet = json.loads(line)
        tweets.append({
            'date': tweet['date'],
            'content': tweet['content'],
            'url': tweet['url']
        })
    except json.JSONDecodeError:
        print("❌ Failed to parse line:", line)
        continue

with open('tweets.json', 'w') as f:
    json.dump(tweets, f, indent=2)

print(f"✅ Scraped {len(tweets)} tweets")
