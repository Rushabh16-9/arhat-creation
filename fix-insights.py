import re

with open('app/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

new_insights = '''              {view360Data && (
                <div style={{ marginTop: '24px', padding: '16px 20px', background: 'linear-gradient(135deg, #f0fdf4 0%, #e0f2fe 100%)', borderRadius: '16px', border: '1px solid rgba(0, 150, 255, 0.1)', width: '100%', boxShadow: '0 4px 12px rgba(0,0,0,0.03)' }}>
                  <div style={{ fontSize: '11px', letterSpacing: '0.15em', color: '#0369a1', textTransform: 'uppercase', marginBottom: '12px', fontWeight: '800', display: 'flex', alignItems: 'center', gap: '6px' }}>
                    \u2728 Gemini AI Insights
                  </div>
                  {view360Data.overallImpression && (
                    <p style={{ fontSize: '14px', color: '#334155', lineHeight: '1.6', fontWeight: '500', marginBottom: '12px' }}>
                      {view360Data.overallImpression}
                    </p>
                  )}
                  {view360Data.uniqueFeature && (
                    <p style={{ fontSize: '13px', color: '#0ea5e9', fontStyle: 'italic', fontWeight: '600', paddingLeft: '8px', borderLeft: '3px solid #38bdf8' }}>
                      {view360Data.uniqueFeature}
                    </p>
                  )}
                </div>
              )}'''

js = re.sub(
    r'\{view360Data\ \&\&\ \(\s*<div.*?\{view360Data\.uniqueFeature\}\}</p>\s*\)\}\s*</div>\s*\)\}',
    new_insights,
    js,
    flags=re.DOTALL
)

with open('app/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Fixed Gemini AI Insights styling!")
