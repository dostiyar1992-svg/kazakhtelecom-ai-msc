with open('index.html', encoding='utf-8') as f:
    html = f.read()

pos = html.find('<!-- Resolution Action Form (Update Stage & Add Notes) -->')
print(html[pos:pos+1500])
