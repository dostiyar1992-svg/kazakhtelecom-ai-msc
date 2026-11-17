with open('index.html', encoding='utf-8') as f:
    html = f.read()

pos = html.find('id="modal-appeal-resolution-inspector"')
print(html[pos-100:pos+800])
