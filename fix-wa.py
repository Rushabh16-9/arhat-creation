import re

with open('app/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace the broken whatsapp message array with safe JS unicode escapes
new_msg_array = r'''const msg = [
        '\uD83D\uDED2 *New Order - Arhat Shop*',
        '',
        `\uD83D\uDCE6 *Product:* ${product.name}`,
        `\uD83C\uDFF7\uFE0F *Category:* ${product.category || 'General'}`,
        `\uD83D\uDCB0 *Price:* \u20B9${product.price.toLocaleString('en-IN')}${discount ? ` (${discount}% OFF)` : ''}`,
        `\uD83D\uDD22 *Quantity:* ${qty}`,
        `\uD83D\uDCB8 *Total:* \u20B9${(product.price * qty).toLocaleString('en-IN')}`,
        '',
        `\uD83D\uDCCD *Delivery Location:* ${location}`,
        '',
        `\uD83D\uDCC8 *Stock Available:* ${product.stock > 0 ? product.stock + ' units' : 'Check availability'}`,
        '',
        `\u23F2\uFE0F *Order Time:* ${new Date().toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' })}`,
        '',
        '--- Sent via Arhat Shop ---'
      ].join('\n');'''

js = re.sub(
    r'const msg = \[\s*(?:\'.*?\'|`.*?`)[^\]]*\].join\(\'\\n\'\);',
    new_msg_array,
    js
)

with open('app/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("WhatsApp message text fixed!")
