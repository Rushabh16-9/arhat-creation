import re

with open('app/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

new_logo = """function LogoMark() {
  return (
    <svg className="nav-logo-mark" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="logo-grad" x1="0" y1="0" x2="48" y2="48" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stopColor="#1e293b"/>
          <stop offset="100%" stopColor="#0f172a"/>
        </linearGradient>
        <linearGradient id="logo-gold" x1="0" y1="0" x2="48" y2="48" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stopColor="#f59e0b"/>
          <stop offset="100%" stopColor="#b45309"/>
        </linearGradient>
      </defs>
      <rect width="48" height="48" rx="14" fill="url(#logo-grad)" stroke="rgba(245, 158, 11, 0.2)" strokeWidth="1"/>
      <path d="M24 10L10 38H16.5L20 29H28L31.5 38H38L24 10ZM24 17.5L26.5 24H21.5L24 17.5Z" fill="url(#logo-gold)"/>
      <circle cx="24" cy="24" r="18" stroke="url(#logo-gold)" strokeWidth="1.5" strokeDasharray="3 4" opacity="0.4"/>
    </svg>
  );
}"""

js = re.sub(r'function LogoMark\(\) \{.*?</svg>\s*\)', new_logo, js, flags=re.DOTALL)

with open('app/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Logo updated!")
