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

# Update renderWorkorders to include fault column
old_render = """<td>'+o.device+'</td><td>'+getStatusHtml(o.status)+'</td>"""
new_render = """<td>'+o.device+'</td><td>'+(o.desc||'').substring(0,12)+'</td><td>'+getStatusHtml(o.status)+'</td>"""
content = content.replace(old_render, new_render)

# Update showPendingDetail to include time fields
old_pending = """document.querySelector('#pending-table tbody').innerHTML=os.map(o=>'<tr><td>'+o.id+'</td><td>'+o.dept+'</td><td>'+o.device+'</td><td>'+o.status+'</td></tr>').join('');"""
new_pending = """const n = new Date();
    document.querySelector('#pending-table tbody').innerHTML = os.map(o => {
        const ct = new Date(o.createTime);
        const dur = n - ct;
        return '<tr><td>'+o.id+'</td><td>'+o.dept+'</td><td>'+o.device+'</td><td>'+ct.toLocaleString()+'</td><td>'+formatDuration(dur)+'</td><td>'+getStatusHtml(o.status)+'</td></tr>';
    }).join('');"""
content = content.replace(old_pending, new_pending)

# Add formatDuration function if not exists
if 'function formatDuration' not in content:
    # Insert after getStatusHtml
    idx = content.find('function getStatusHtml')
    if idx > 0:
        end = content.find('}', idx) + 1
        func = '''
function formatDuration(ms) {
    if(!ms) return '-';
    const h = Math.floor(ms/3600000);
    const m = Math.floor((ms%3600000)/60000);
    if(h > 24) return Math.floor(h/24) + '天' + (h%24) + 'h';
    return h + 'h' + m + 'm';
}'''
        content = content[:end] + func + content[end:]

# Upload
content_b64 = base64.b64encode(content.encode('utf-8')).decode('utf-8')
body = json.dumps({
    'message': 'v14 JS update',
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
print('Done, status:', r2.status)
