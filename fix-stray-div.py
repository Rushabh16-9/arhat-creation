import sys

with open('app/page.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Line 237 is currently the stray </div>
# Let's verify it's a stray </div> before the Details Panel
if '{/* Details Panel */}' in lines[239]:
    del lines[236] # 0-indexed, so line 237 is index 236

with open('app/page.js', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Removed stray </div>!")
