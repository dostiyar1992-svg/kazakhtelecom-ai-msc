with open('index.html', encoding='utf-8') as f:
    html = f.read()

pos = html.find('tbody.innerHTML = filtered.map(a => {')
pos_end = html.find('}).join(\'\');', pos)
print(html[pos:pos_end+20])
