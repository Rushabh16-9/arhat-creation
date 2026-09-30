import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    # lines to delete: 929, 930, 931, 932 (1-indexed) => 928, 929, 930, 931 (0-indexed)
    if i in [928, 929, 930, 931]:
        continue
    new_lines.append(line)

with open('app/admin/page.js', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Duplicate Bulk button inside the billing <li> has been successfully deleted!")
