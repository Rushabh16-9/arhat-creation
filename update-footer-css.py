# -*- coding: utf-8 -*-
with open('app/globals.css', 'r', encoding='utf-8') as f:
    css = f.read()

import re
css = re.sub(
    r'\.footer-inner \{ max-width:1100px; margin:0 auto; display:grid; grid-template-columns:1\.5fr 1fr 1fr; gap:48px; \}',
    '.footer-inner { max-width:1100px; margin:0 auto; display:grid; grid-template-columns:2fr 1fr 1fr 1fr; gap:48px; }',
    css
)

# Also ensure it stacks cleanly on mobile
css += """
@media (max-width: 768px) {
  .footer-inner {
    grid-template-columns: 1fr 1fr;
    gap: 32px;
  }
  .footer-col-brand {
    grid-column: 1 / -1;
  }
}

@media (max-width: 480px) {
  .footer-inner {
    grid-template-columns: 1fr;
  }
}
"""

with open('app/globals.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Footer CSS updated!")
