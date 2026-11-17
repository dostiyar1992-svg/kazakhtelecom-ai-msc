with open('index.html', encoding='utf-8') as f:
    html = f.read()

pos = html.find('function renderMyAppealsList')
print("=== renderMyAppealsList ===")
print(html[pos:pos+2500])
