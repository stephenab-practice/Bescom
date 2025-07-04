import json
import subprocess

query = 'from:bescomofficial'
cmd = ['snscrape', '--jsonl', '--max-results', '10', f'twitter-search "{query}"']
result = subprocess.run(cmd, capture_output=True, text=True)
tweets = []

for line in result.stdout.strip().split('\n'):
    tweet = json.loads(line)
    tweets.append({
        'date': tweet['date'],
        'content': tweet['content'],
        'url': tweet['url']
    })

with open('tweets.json', 'w') as f:
    json.dump(tweets, f, indent=2)
