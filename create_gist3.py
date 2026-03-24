import urllib.request
import json

# 先检查用户
req = urllib.request.Request('https://api.github.com/user', headers={'Authorization': 'token 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'})
r = urllib.request.urlopen(req)
print('User:', json.loads(r.read().decode())['login'])

# 创建Gist
data = json.dumps({
    "description": "工单数据备份",
    "public": False,
    "files": {
        "workorders.json": {"content": '{"workorders":[],"updateTime":"2026-03-23"}'}
    }
}).encode('utf-8')

req = urllib.request.Request('https://api.github.com/gists', data=data, method='POST', headers={'Authorization': 'token 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', 'Content-Type': 'application/json'})
r = urllib.request.urlopen(req)
result = json.loads(r.read().decode())
print('Gist ID:', result['id'])
print('URL:', result['html_url'])
