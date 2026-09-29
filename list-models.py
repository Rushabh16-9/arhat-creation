import json
import urllib.request

api_key = None
with open('.env.local', 'r', encoding='utf-8') as f:
    for line in f:
        if line.startswith('GEMINI_API_KEY='):
            api_key = line.strip().split('=', 1)[1].strip().strip('"').strip("'")
            break

if not api_key:
    print("No API key found!")
    exit(1)

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
req = urllib.request.Request(url)
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        models = [m['name'] for m in data.get('models', [])]
        print("Available models:")
        for m in models:
            print(m)
except Exception as e:
    print("Failed:", e)
