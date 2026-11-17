with open('index.html', encoding='utf-8') as f:
    html = f.read()

import re

# Find in renderMyAppealsList
pos_my = html.find('function renderMyAppealsList')
end_my = html.find('function switchAppealsSubTab', pos_my)
my_code = html[pos_my:end_my]

print("=== BUTTONS IN renderMyAppealsList ===")
for btn in re.findall(r'<button[^>]*>.*?</button>', my_code, re.DOTALL):
    print("  ", btn.replace('\n', ' ')[:150])

# Find in renderAppealsResolutionTable
pos_res = html.find('function renderAppealsResolutionTable')
end_res = html.find('function filterAppealsResolution', pos_res)
res_code = html[pos_res:end_res]

print("\n=== BUTTONS IN renderAppealsResolutionTable ===")
for btn in re.findall(r'<button[^>]*>.*?</button>', res_code, re.DOTALL):
    print("  ", btn.replace('\n', ' ')[:150])
