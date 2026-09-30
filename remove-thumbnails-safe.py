with open('app/page.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    if '{/* Thumbnail Strip */}' in line:
        skip = True
        
    if skip:
        if '</div>' in line and i > 237: # We know the end is around line 238
            # wait, it's safer to just skip until we see the start of the next section
            pass
        if '{/* Details Panel */}' in line:
            skip = False
            
    if not skip:
        new_lines.append(line)

with open('app/page.js', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Thumbnails removed safely!")
