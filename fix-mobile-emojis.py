with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'admin-mobile-nav' in line:
        start_idx = i
        break

# Safely replace within the admin-mobile-nav block
for i in range(start_idx, start_idx + 20):
    if 'Products' in lines[i+1] and '??' in lines[i]:
        lines[i] = lines[i].replace('??', '\U0001F4E6')
    elif 'Add' in lines[i+1] and '?' in lines[i]:
        lines[i] = lines[i].replace('?', '\u2795')
    elif 'POS' in lines[i+1] and '??' in lines[i]:
        lines[i] = lines[i].replace('??', '\U0001F9FE')
    elif 'Logout' in lines[i+1] and '??' in lines[i]:
        lines[i] = lines[i].replace('??', '\U0001F6AA')

with open('app/admin/page.js', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Mobile nav emojis fixed!")
