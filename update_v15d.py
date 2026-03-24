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

# Fix status dropdown
old_status = """<td>'+getStatusHtml(o.status)+'</td>"""
new_status = """<td><select class=\"form-select form-select-sm py-0\" style=\"width:70px;font-size:11px\" onchange=\"changeStatus('\"+o.id+\"',this.value)\"><option \"+(o.status==='响应中'?'selected':'')+\">响应</option><option \"+(o.status==='审批中'?'selected':'')+\">审批</option><option \"+(o.status==='已完成'?'selected':'')+\">完成</option></select></td>"""
content = content.replace(old_status, new_status)

content_b64 = base64.b64encode(content.encode('utf-8')).decode('utf-8')
body = json.dumps({
    'message': 'v15d - status dropdown fix',
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
print('v15d done, status:', r2.status)
