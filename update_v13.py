# Read v12
with open(r'C:\Users\lenovo\.openclaw\workspace\admin_v12.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Change title
content = content.replace('<title>银行设备运维管理系统</title>', '<title>网点运维管理</title>')

# 2. Change logo  
content = content.replace('<h5>运维</h5>', '网点运维管理')

# 3. Add fault description column to table header
content = content.replace('<th>设备</th><th>状态</th>', '<th>设备</th><th>故障</th><th>状态</th>')

# 4. Update pending detail modal to include time info
# Find and update the pending-table header
content = content.replace(
    '<th>工单号</th><th>机构</th><th>设备</th><th>状态</th>',
    '<th>工单号</th><th>机构</th><th>设备</th><th>报修时间</th><th>工单时长</th><th>状态</th>'
)

# Save
with open(r'C:\Users\lenovo\.openclaw\workspace\admin_v13.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done, length:', len(content))
