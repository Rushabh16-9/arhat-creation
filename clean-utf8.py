with open('app/page.js', 'rb') as f:
    raw = f.read()

# Decode ignoring strict errors and replacing bad surrogates
text = raw.decode('utf-8', errors='replace')

# The bad surrogates probably turned into \ufffd ()
# But let's just make sure we wipe out the entire WhatsApp message block and write it safely
# Actually, since the file is corrupted, let's just find all  and replace them with empty strings,
# OR we can just write the whole file safely if we know where the  are.
# Wait, let's see how many  are in the text.
count = text.count("\ufffd")
print(f"Found {count} corrupted characters!")

# We can fix the WhatsApp msg block by finding it and replacing it.
import re
text = re.sub(r'const msg = \[[^\]]+\]\.join\(\'\\n\'\);', '''const msg = [
        '\uD83D\uDED2 *New Order - Arhat Shop*',
        '',
        `\uD83D\uDCE6 *Product:* ${product.name}`,
        `\uD83C\uDFF7\uFE0F *Category:* ${product.category || 'General'}`,
        `\uD83D\uDCB0 *Price:* {"\\u20B9"}${product.price.toLocaleString('en-IN')}${discount ? ` (${discount}% OFF)` : ''}`,
        `\uD83D\uDD22 *Quantity:* ${qty}`,
        `\uD83D\uDCB8 *Total:* {"\\u20B9"}${(product.price * qty).toLocaleString('en-IN')}`,
        '',
        `\uD83D\uDCCD *Delivery Location:* ${location}`,
        '',
        `\uD83D\uDCC8 *Stock Available:* ${product.stock > 0 ? product.stock + ' units' : 'Check availability'}`,
        '',
        `\u23F2\uFE0F *Order Time:* ${new Date().toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' })}`,
        '',
        '--- Sent via Arhat Shop ---'
      ].join('\\n');''', text)

# Let's completely wipe any remaining corrupted characters just in case!
text = text.replace("\ufffd", "")

with open('app/page.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("File decoded and cleaned successfully!")
