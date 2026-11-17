with open('index.html', encoding='utf-8') as f:
    html = f.read()

pos = html.find('function openResolutionInspector')
pos_end = html.find('function saveAppealResolutionStage', pos)
print(html[pos:pos_end])
