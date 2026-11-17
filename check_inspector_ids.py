with open('index.html', encoding='utf-8') as f:
    html = f.read()

import re

# extract all document.getElementById('...') from openResolutionInspector
pos = html.find('function openResolutionInspector')
pos_end = html.find('function closeResolutionInspector', pos)
fn_code = html[pos:pos_end]

ids_in_fn = re.findall(r"document\.getElementById\(['\"]([^'\"]+)['\"]\)", fn_code)
print(f"IDs used in openResolutionInspector: {len(ids_in_fn)}")
for elem_id in ids_in_fn:
    found = f'id="{elem_id}"' in html
    print(f"  {elem_id}: {'FOUND' if found else 'MISSING IN HTML!'}")
