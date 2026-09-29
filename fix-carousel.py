import re

with open('app/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

new_cards = '''  let CARDS = [];
  if (products && products.length > 0) {
    while (CARDS.length < 16) {
      CARDS = [...CARDS, ...products];
    }
    // Add unique keys so React doesn't complain about duplicates
    CARDS = CARDS.map((p, i) => ({ ...p, unique_key: p.id + '_' + i }));
  } else {
    CARDS = Array(16).fill(null).map((_,i) => ({
      id: i, name: Product , unique_key: 'null_'+i,
      image_url: null,
      color: ['#1a2535','#2b1535','#1a3520','#352515','#153035','#301530','#153525','#302515','#152535','#251535'][i % 10]
    }));
  }

  const n = CARDS.length;
  const R = 891;
  const step = 360 / n;'''

js = re.sub(
    r'const CARDS = products \&\& products\.length > 0 \? products : Array\(10\).*?const step = 360 / n;',
    new_cards,
    js,
    flags=re.DOTALL
)

# Also fix the key in the map function!
js = js.replace('key={product?.id ?? i}', 'key={product?.unique_key ?? i}')

with open('app/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Fixed RingCarousel array length!")
