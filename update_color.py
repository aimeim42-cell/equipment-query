import base64
import json
import urllib.request

token = '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'

req = urllib.request.Request(
    'https://api.github.com/repos/aimeim42-cell/equipment-query/contents/admin.html',
    headers={'Authorization': 'token ' + token}
)
r = urllib.request.urlopen(req)
data = json.loads(r.read().decode())
sha = data['sha']
content = base64.b64decode(data['content']).decode('utf-8')

# Apply color scheme
content = content.replace('body{background:#f5f7fa', 'body{background:#e3f2fd')
content = content.replace('.sidebar{background:#1a1a2e', '.sidebar{background:#1976d2')
content = content.replace('.sidebar .logo{background:#16213e', '.sidebar .logo{background:#1565c0')
content = content.replace('.sidebar a:hover,.sidebar a.active{background:#0f3460', '.sidebar a:hover,.sidebar a.active{background:#1e88e5')
content = content.replace('background:linear-gradient(135deg,#1a1a2e,#16213e)', 'background:linear-gradient(135deg,#1976d2,#42a5f5)')
content = content.replace('#1a1a2e', '#1976d2')
content = content.replace('#16213e', '#1565c0')
content = content.replace('#0f3460', '#1e88e5')

content_b64 = base64.b64encode(content.encode('utf-8')).decode('utf-8')
body = json.dumps({
    'message': 'v15e - colors',
    'content': content_b64,
    'sha': sha
}).encode('utf-8')

req2 = urllib.request.Request(
    'https://api.github.com/repos/aimeim42-cell/equipment-query/contents/admin.html',
    data=body,
    method='PUT',
    headers={'Authorization': 'token ' + token, 'Content-Type': 'application/json'}
)
r2 = urllib.request.urlopen(req2)
print('v15e done, status:', r2.status)
