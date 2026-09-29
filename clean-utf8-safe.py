with open('app/page.js', 'rb') as f:
    raw = f.read()

# Decode ignoring strict errors and replacing bad surrogates
text = raw.decode('utf-8', errors='replace')

# The bad surrogates probably turned into \ufffd ()
count = text.count("\ufffd")
print(f"Found {count} corrupted characters!")

# Wipe the corrupted characters completely
text = text.replace("\ufffd", "")

with open('app/page.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("File decoded and cleaned successfully!")
