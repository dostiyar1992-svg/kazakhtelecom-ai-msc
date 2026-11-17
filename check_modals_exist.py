with open('index.html', encoding='utf-8') as f:
    html = f.read()

print("modal-appeal-resolution-inspector in html:", 'id="modal-appeal-resolution-inspector"' in html)
print("modal-token-tracker in html:", 'id="modal-token-tracker"' in html)
