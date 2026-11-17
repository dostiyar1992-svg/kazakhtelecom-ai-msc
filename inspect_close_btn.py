with open('index.html', encoding='utf-8') as f:
    html = f.read()

pos = html.find('id="inspector-category-sub"')
print(html[pos:pos+800])
