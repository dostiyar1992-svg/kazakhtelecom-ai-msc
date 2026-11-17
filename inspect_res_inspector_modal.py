with open('index.html', encoding='utf-8') as f:
    html = f.read()

pos = html.find('function openResolutionInspector')
pos_end = html.find('function closeResolutionInspector', pos)
print(html[pos:pos_end+500])

print("\nDoes modal-resolution-inspector exist in index.html?:", 'id="modal-resolution-inspector"' in html)
