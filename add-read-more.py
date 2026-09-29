import re

with open('app/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Add state
js = js.replace(
    '  const [qty, setQty] = useState(1);',
    '  const [qty, setQty] = useState(1);\n  const [isExpanded, setIsExpanded] = useState(false);'
)

# Replace description rendering
old_desc = '''            {product.description && (

              <p className="modal-desc" style={{ display: "-webkit-box", WebkitLineClamp: 3, WebkitBoxOrient: "vertical", overflow: "hidden", textOverflow: "ellipsis" }}>{product.description}</p>

            )}'''

new_desc = '''            {product.description && (
              <div style={{ marginBottom: '8px' }}>
                <p className="modal-desc" style={{ display: isExpanded ? 'block' : '-webkit-box', WebkitLineClamp: isExpanded ? 'unset' : 3, WebkitBoxOrient: 'vertical', overflow: 'hidden', textOverflow: 'ellipsis', margin: 0, transition: 'all 0.3s ease' }}>{product.description}</p>
                {product.description.length > 100 && (
                  <button onClick={() => setIsExpanded(!isExpanded)} style={{ background: 'transparent', border: 'none', color: 'var(--primary)', fontSize: '13px', fontWeight: '700', cursor: 'pointer', padding: 0, marginTop: '8px', display: 'flex', alignItems: 'center', gap: '4px' }}>
                    {isExpanded ? 'Read Less' : 'Read More'}
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" style={{ transform: isExpanded ? 'rotate(180deg)' : 'none', transition: 'transform 0.2s' }}><path d="m6 9 6 6 6-6"></path></svg>
                  </button>
                )}
              </div>
            )}'''

# Since line breaks might be slightly different, use a robust replace
js = re.sub(
    r'\{product\.description && \(\s*<p className="modal-desc"[^>]*>\{product\.description\}<\/p>\s*\)\}',
    lambda _: new_desc,
    js,
    flags=re.DOTALL
)

with open('app/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Read More toggle added!")
