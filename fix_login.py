import base64
import json
import urllib.request
import ssl

# Create SSL context that doesn't verify certificates
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

token = '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'

# Use urllib with SSL context
import urllib.request
req = urllib.request.Request(
    'https://api.github.com/repos/aimeim42-cell/equipment-query/contents/admin.html',
    headers={'Authorization': 'token ' + token}
)

# Try with https handler
import urllib.request
opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ssl_context))
r = opener.open(req)
data = json.loads(r.read().decode())
sha = data['sha']
content = base64.b64decode(data['content']).decode('utf-8')

# Fix login - add onclick to form
old_form = '<form id="login-form">'
new_form = '<form id="login-form" onsubmit="return handleLogin(event)">'
content = content.replace(old_form, new_form)

# Add handleLogin function
old_check = 'checkLogin();'
new_check = '''function handleLogin(e){
    e.preventDefault();
    const u=document.getElementById('login-username').value;
    const p=document.getElementById('login-password').value;
    const s=JSON.parse(localStorage.getItem('settings')||'{}');
    if(!s.username){
        localStorage.setItem('settings',JSON.stringify({username:u,password:p}));
        alert('设置成功！');
        document.getElementById('login-page').style.display='none';
        document.getElementById('main-system').style.display='block';
    }else if(u===s.username && p===s.password){
        document.getElementById('login-page').style.display='none';
        document.getElementById('main-system').style.display='block';
    }else{
        alert('错误');
    }
}
checkLogin();'''

content = content.replace(old_check, new_check)

# Upload
content_b64 = base64.b64encode(content.encode('utf-8')).decode('utf-8')
body = json.dumps({
    'message': 'Fix login handler',
    'content': content_b64,
    'sha': sha
}).encode('utf-8')

req2 = urllib.request.Request(
    'https://api.github.com/repos/aimeim42-cell/equipment-query/contents/admin.html',
    data=body,
    method='PUT',
    headers={'Authorization': 'token ' + token, 'Content-Type': 'application/json'}
)
r2 = opener.open(req2)
print('Done, status:', r2.status)
