with open('index.html', encoding='utf-8') as f:
    html = f.read()

pos = html.find('function openTokenModal')
print(html[pos:pos+1500])
