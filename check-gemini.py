with open('app/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

if 'Gemini AI Insights' in js:
    print('Gemini UI STILL EXISTS!')
else:
    print('Gemini UI is gone!')

if 'load360Description' in js:
    print('API call STILL EXISTS!')
else:
    print('API call is gone!')
