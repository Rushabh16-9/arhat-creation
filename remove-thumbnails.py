with open('app/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re

# Remove the thumbnail strip block
old_strip_regex = r'\{\/\* Thumbnail Strip \*\/\}\s*\{\(product\.enhanced_image_url \|\| product\.image_url\) && \(\s*<div.*?\{\[1, 2, 3\]\.map.*?</div>\s*\)\}\s*</div>\s*\)\}\s*</div>'

# We have to be careful with the regex to not delete the parent </div>. 
# It is better to use replace on the exact substring.

exact_str = """{/* Thumbnail Strip */}

{(product.enhanced_image_url || product.image_url) && (

<div style={{ display: 'flex', gap: '12px', marginTop: '16px', justifyContent: 'center' }}>

{[1, 2, 3].map(i => (

<div key={i} style={{ width: '64px', height: '64px', borderRadius: '10px', overflow: 'hidden', border: i === 1 ? '2px solid var(--primary)' : '1px solid var(--border)', cursor: 'pointer', opacity: i === 1 ? 1 : 0.6, transition: 'all 0.2s' }}>

<img src={product.enhanced_image_url || product.image_url} alt="" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />

</div>

))}

</div>

)}"""

if exact_str in js:
    js = js.replace(exact_str, "")
    with open('app/page.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Thumbnail strip removed successfully!")
else:
    # Try an alternative matching strategy
    import re
    js = re.sub(r'\{\/\* Thumbnail Strip \*\/\}.*?\}\)\}', '', js, flags=re.DOTALL)
    with open('app/page.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Thumbnail strip removed using regex!")

