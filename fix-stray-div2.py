with open('app/page.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '{/* Details Panel */}' in line:
        # The line right before it should be an empty line, and before that is the stray </div>
        # Let's just find the stray </div> directly
        stray_idx = i - 2
        if '</div>' in lines[stray_idx]:
            del lines[stray_idx]
            print("Deleted stray div!")
        break

with open('app/page.js', 'w', encoding='utf-8') as f:
    f.writelines(lines)

