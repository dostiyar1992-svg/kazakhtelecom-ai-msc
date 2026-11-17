with open('generate_final_index.py', encoding='utf-8') as f:
    code = f.read()

pos = code.find('<!-- Resolution Action Form (Update Stage & Add Notes) -->')
print(code[pos:pos+500])
