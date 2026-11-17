with open('index.html', encoding='utf-8') as f:
    html = f.read()

pos = html.find('.modal-backdrop-nudge')
print(html[pos:pos+400])
