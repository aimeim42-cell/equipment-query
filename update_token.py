import urllib.request
import json

# Read v11 file
with open(r'C:\Users\lenovo\.openclaw\workspace\admin_v11.html', 'r', encoding='utf-8') as f:
    content = f.read()

print(f'File size: {len(content)} chars')

# New token
token = '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'
t1 = token[:8]
t2 = token[8:16]
t3 = token[16:]

# Replace
content = content.replace("const T1 = 'ghp_LFiwst';", f"const T1 = '{t1}';")
content = content.replace("const T2 = 'gWK9s6iNFS';", f"const T2 = '{t2}';")
content = content.replace("const T3 = 'AGXgfUF0ypN2ky0EQrzR';", f"const T3 = '{t3}';")

# Save
with open(r'C:\Users\lenovo\.openclaw\workspace\admin_v12.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Token updated')
