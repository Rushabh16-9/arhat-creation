with open('app/globals.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Add display block for mobile menu button in the mobile query
css = css.replace(
    '/* Navbar */\n  .nav-links { display: none; }',
    '/* Navbar */\n  .nav-links { display: none; }\n  .mobile-menu-btn { display: block !important; }'
)

with open('app/globals.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("CSS updated for mobile menu button!")
