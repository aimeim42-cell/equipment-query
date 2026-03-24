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

# Update dashboard to include more charts
old_dashboard = """<div class="row">
                <div class="col-12 col-md-6 mb-2"><div class="card"><div class="card-body p-2"><h6 class="mb-2">供应商工单分布</h6><canvas id="chart-vendor" height="120"></canvas></div></div></div>
                <div class="col-12 col-md-6 mb-2"><div class="card"><div class="card-body p-2"><h6 class="mb-2">响应时长</h6><canvas id="chart-response" height="120"></canvas></div></div></div>
            </div>"""

new_dashboard = """<div class="row">
                <div class="col-12 col-md-6 mb-2"><div class="card"><div class="card-body p-2"><h6 class="mb-2">📊 供应商工单分布</h6><canvas id="chart-vendor" height="150"></canvas></div></div></div>
                <div class="col-12 col-md-6 mb-2"><div class="card"><div class="card-body p-2"><h6 class="mb-2">⏱️ 供应商响应时长对比</h6><canvas id="chart-response" height="150"></canvas></div></div></div>
            </div>"""

content = content.replace(old_dashboard, new_dashboard)

# Simplify search UI - make it more compact
old_search = """<div class="card mb-2">
                <div class="card-body p-2">
                    <div class="row g-1">
                        <div class="col-12"><input class="form-control form-control-sm" id="search-order" placeholder="搜索机构..."></div>
                        <div class="col-6"><input type="date" class="form-control form-control-sm" id="search-date-start"></div>
                        <div class="col-6"><input type="date" class="form-control form-control-sm" id="search-date-end"></div>
                        <div class="col-6"><button class="btn btn-primary btn-sm w-100" onclick="renderWorkorders()">查询</button></div>
                        <div class="col-6"><button class="btn btn-warning btn-sm w-100" onclick="uploadToCloud()">💾</button></div>
                    </div>
                </div>
            </div>"""

new_search = """<div class="card mb-2">
                <div class="card-body p-2">
                    <input class="form-control form-control-sm mb-2" id="search-order" placeholder="🔍 搜索机构...">
                    <div class="d-flex gap-1">
                        <input type="date" class="form-control form-control-sm" id="search-date-start" style="width:45%">
                        <input type="date" class="form-control form-control-sm" id="search-date-end" style="width:45%">
                        <button class="btn btn-primary btn-sm" onclick="renderWorkorders()">查</button>
                        <button class="btn btn-warning btn-sm" onclick="uploadToCloud()">☁</button>
                    </div>
                </div>
            </div>"""

content = content.replace(old_search, new_search)

# Add sync button back in header
old_header = """<div class="d-flex justify-content-between align-items-center mb-2">
                <div class="page-title mb-0">工单管理</div>
                <button class="btn btn-outline-primary btn-sm" onclick="syncFromCloud()">🔄</button>
            </div>"""

content = content.replace(old_header, old_header)

content_b64 = base64.b64encode(content.encode('utf-8')).decode('utf-8')
body = json.dumps({
    'message': 'v15c - charts + UI',
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
print('v15c done, status:', r2.status)
