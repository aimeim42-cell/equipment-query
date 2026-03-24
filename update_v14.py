import base64
import json
import urllib.request

token = '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'

# Get current file
req = urllib.request.Request(
    'https://api.github.com/repos/aimeim42-cell/equipment-query/contents/admin.html',
    headers={'Authorization': 'token ' + token}
)
r = urllib.request.urlopen(req)
data = json.loads(r.read().decode())
sha = data['sha']
content = base64.b64decode(data['content']).decode('utf-8')

# 1. Update title
content = content.replace('<title>银行设备运维管理系统</title>', '<title>网点运维管理</title>')

# 2. Update logo text
content = content.replace('>运维</h5>', '>网点运维管理</div><a href="#" onclick="showPage')

# 3. Add fault column header in workorder table
content = content.replace(
    '<th>设备</th><th>状态</th>',
    '<th>设备</th><th>故障</th><th>状态</th>'
)

# 4. Update pending modal to include time fields
content = content.replace(
    '<th>工单号</th><th>机构</th><th>设备</th><th>状态</th>',
    '<th>工单号</th><th>机构</th><th>设备</th><th>报修时间</th><th>工单时长</th><th>状态</th>'
)

# Upload
content_b64 = base64.b64encode(content.encode('utf-8')).decode('utf-8')
body = json.dumps({
    'message': 'v14 complete - all updates',
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
print('Uploaded, status:', r2.status)
