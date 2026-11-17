with open('index.html', encoding='utf-8') as f:
    html = f.read()

pos = html.find('function renderMyAppealsList')
pos_end = html.find('function switchAppealsSubTab', pos)
print(html[pos:pos_end])
