with open('index.html', encoding='utf-8') as f:
    html = f.read()

pos = html.find('function openResolutionInspector')
print(html[pos:pos+1500])
