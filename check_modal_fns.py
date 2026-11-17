with open('index.html', encoding='utf-8') as f:
    html = f.read()

import re

for fn in ['openResolutionInspector', 'openTokenModalWithCode', 'openTokenModal']:
    matches = [m.start() for m in re.finditer(r'function\s+' + fn, html)]
    print(f"Function {fn}: found {len(matches)} definitions at {matches}")
