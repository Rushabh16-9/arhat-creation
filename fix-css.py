import re

with open('app/globals.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Fix hero button
css = css.replace('.hero-cta-primary { height:52px;', '.hero-cta-primary { display:inline-flex; align-items:center; justify-content:center; text-decoration:none; height:52px;')

# Change nav CTA color
css = css.replace('background:var(--primary); color:#fff; font-weight:600; }', 'background:#25d366; color:#fff; font-weight:600; } /* Nav CTA */')

with open('app/globals.css', 'w', encoding='utf-8') as f:
    f.write(css)

with open('app/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Change the hero badge SVG color to gold to make it look nicer
js = js.replace('fill="rgba(16,112,152,.72)" stroke="rgba(190,236,255,.6)"', 'fill="var(--gold)" stroke="none"')

with open('app/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Fixed CSS and JS!")
