with open('index.html', encoding='utf-8') as f:
    html = f.read()

pos = html.find('id="modal-token-tracker"')
print(html[pos-50:pos+1500])
