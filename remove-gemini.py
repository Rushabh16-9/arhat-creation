with open('app/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re

# Remove the Gemini Insights UI block
js = re.sub(
    r'\{\/\* AI Insights Card \*\/\}.*?view360Data && \([^)]*Gemini AI Insights[^)]*\)\s*\}',
    '',
    js,
    flags=re.DOTALL
)

# Also remove any remaining Gemini UI code just in case the regex missed it
js = re.sub(
    r'\{\/\* AI Insights Card \*\/\}.*?\{\s*view360Data && \(\s*<div[^>]*>.*?<\/div>\s*\)\s*\}',
    '',
    js,
    flags=re.DOTALL
)

# And another pass for good measure, specifically targeting the view360Data block
js = re.sub(
    r'\{\/\* AI Insights Card \*\/\}\s*\{view360Data && \(.*?<\/div>\s*\)\}',
    '',
    js,
    flags=re.DOTALL
)

# Now remove the API call in useEffect
js = re.sub(
    r'if \(\(product\.image_url \|\| product\.enhanced_image_url\) && !view360Data\) \{\s*load360Description\(\);\s*\}',
    '',
    js,
    flags=re.DOTALL
)

# And remove the load360Description function entirely
js = re.sub(
    r'async function load360Description\(\) \{.*?\} finally \{\s*setLoadingGemini\(false\);\s*\}\s*\}',
    '',
    js,
    flags=re.DOTALL
)

with open('app/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Gemini AI Insights removed!")
