import json
import subprocess

username = 'bescomofficial'
cmd = ['snscrape', '--jsonl', '--max-results', '10', 'twitter-user', username]
result = subprocess.run(cmd, capture_output=True, text=True)

# Check if snscrape ran successfully
if result.returncode != 0:
    print("snscrape failed:", result.stderr)
    exit(1)

lines = result.stdout.strip().split('\n')
tweets = []

for line in lines:
    if not line.strip():
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
