import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('.env.local', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for line in lines:
    line = line.strip()
    if line and not line.startswith('#'):
        print(line)
