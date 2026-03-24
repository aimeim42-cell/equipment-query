import urllib.request
import base64
import json

token = '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'

# Get file
req = urllib.request.Request('https://api.github.com/repos/aimeim42-cell/equipment-query/contents/admin.html', headers={'Authorization': 'token ' + token})
r = urllib.request.urlopen(req)
data = json.loads(r.read().decode())
content = base64.b64decode(data['content']).decode('utf-8')

# Fix duplicate 'now' declaration - remove the second one
content = content.replace('const now=new Date();\n    const now = new Date();', 'const now = new Date();')

# Upload
sha = data['sha']
content_b64 = base64.b64encode(content.encode('utf-8')).decode('utf-8')
body = json.dumps({'message': 'Fix duplicate now', 'content': content_b64, 'sha': sha}).encode('utf-8')
req2 = urllib.request.Request('https://api.github.com/repos/aimeim42-cell/equipment-query/contents/admin.html', data=body, method='PUT', headers={'Authorization': 'token ' + token, 'Content-Type': 'application/json'})
r2 = urllib.request.urlopen(req2)
print('Fixed, status:', r2.status)
