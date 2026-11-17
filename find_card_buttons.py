with open('index.html', encoding='utf-8') as f:
    html = f.read()

import re
matches = re.findall(r'<button[^>]*>[^<]*[Кк]арточк[^<]*</button>', html)
for m in matches:
    print(m)
