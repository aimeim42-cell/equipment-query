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

# 1. Update color scheme - light blue + white
content = content.replace('background:#f5f7fa', 'background:#e3f2fd')
content = content.replace('background:#1a1a2e', 'background:#1976d2')
content = content.replace('#1a1a2e', '#1976d2')
content = content.replace('#16213e', '#1565c0')
content = content.replace('#0f3460', '#1e88e5')
content = content.replace('background:linear-gradient(135deg,#1a1a2e,#16213e)', 'background:linear-gradient(135deg,#1976d2,#42a5f5)')

# 2. Add icons to page titles
content = content.replace('工单生成</div>', '📝 工单生成</div>')
content = content.replace('工单管理</div>', '📋 工单管理</div>')
content = content.replace('数据看板</div>', '📊 数据看板</div>')
content = content.replace('运维商</div>', '👥 运维商</div>')
content = content.replace('系统设置</div>', '⚙️ 系统设置</div>')

# Upload
content_b64 = base64.b64encode(content.encode('utf-8')).decode('utf-8')
body = json.dumps({
    'message': 'v15 - colors + icons',
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
print('v15 uploaded, status:', r2.status)
