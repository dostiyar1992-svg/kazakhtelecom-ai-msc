with open('index.html', encoding='utf-8') as f:
    html = f.read()

pos = html.find('id="modal-appeal-resolution-inspector"')
end = html.find('<!-- ========================================================================= -->\n  <!-- MODAL: REGION INSPECTOR', pos)
if end == -1:
    end = pos + 4000
print(html[pos:end])
