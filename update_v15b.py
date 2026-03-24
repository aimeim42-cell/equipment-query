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

# Update vendor list to show full names
old_vendors = """const vendors = [
    {type:'存取款一体机/ATM',vendor:'广东奔腾达电子有限公司',contact:'周洪啸/韩东',phone:'18176252256'},
    {type:'高速大额存取款机',vendor:'广东奔腾达电子有限公司',contact:'韩东',phone:'18178601382'},
    {type:'回单机/自助终端',vendor:'广州南天电脑系统有限公司',contact:'梁太钦',phone:'13877130518'},
    {type:'综合版智能柜台',vendor:'广西佰鼎科技有限公司',contact:'莫德文',phone:'18278387986'},
    {type:'标准版智能柜台',vendor:'广东奔腾达电子有限公司',contact:'肖俊宏',phone:'13878748626'},
    {type:'网银一体机/LED走字屏',vendor:'广西佳仕运网络科技有限公司',contact:'陈剑云',phone:'13977300180'},
    {type:'空调维护',vendor:'广西南宁市源申隆贸易有限公司',contact:'陈国斌',phone:'19077164249'},
    {type:'零星维修',vendor:'广西三弦建设工程有限公司',contact:'曾海龙',phone:'13407718924'},
    {type:'叫号机/宣传屏',vendor:'桂林宇峰电子科技有限公司',contact:'唐孝纯',phone:'18178357885'},
    {type:'征信查询机',vendor:'北京信立合创信息技术有限公司',contact:'谭因金',phone:'13878372640'},
    {type:'其他',vendor:'待分配',contact:'',phone:''}
];"""

content = content.replace("""const vendors = [
    {type:'存取款一体机/ATM',vendor:'广东奔腾达电子有限公司',contact:'周洪啸/韩东',phone:'18176252256'},
    {type:'高速大额存取款机',vendor:'广东奔腾达电子有限公司',contact:'韩东',phone:'18178601382'},
    {type:'回单机/自助终端',vendor:'广州南天电脑系统有限公司',contact:'梁太钦',phone:'13877130518'},
    {type:'综合版智能柜台',vendor:'广西佰鼎科技有限公司',contact:'莫德文',phone:'18278387986'},
    {type:'标准版智能柜台',vendor:'广东奔腾达电子有限公司',contact:'肖俊宏',phone:'13878748626'},
    {type:'网银一体机/LED走字屏',vendor:'广西佳仕运网络科技有限公司',contact:'陈剑云',phone:'13977300180'},
    {type:'空调维护',vendor:'广西南宁市源申隆贸易有限公司',contact:'陈国斌',phone:'19077164249'},
    {type:'零星维修',vendor:'广西三弦建设工程有限公司',contact:'曾海龙',phone:'13407718924'},
    {type:'叫号机/宣传屏',vendor:'桂林宇峰电子科技有限公司',contact:'唐孝纯',phone:'18178357885'},
    {type:'征信查询机',vendor:'北京信立合创信息技术有限公司',contact:'谭因金',phone:'13878372640'},
    {type:'其他',vendor:'待分配',contact:'',phone:''}
];""", old_vendors)

# Add status dropdown in workorder table row
old_row = """<td>'+getStatusHtml(o.status)+'</td>"""
new_row = """<td><select class=\"form-select form-select-sm\" style=\"width:80px\" onchange=\"changeStatus('\"+o.id+\"',this.value)\"><option \"+(o.status==='响应中'?'selected':'')+\">响应中</option><option \"+(o.status==='审批中'?'selected':'')+\">审批中</option><option \"+(o.status==='已完成'?'selected':'')+\">已完成</option></select></td>"""
content = content.replace(old_row, new_row)

# Update pending detail to include more info
old_pending_detail = """return '<tr><td>'+o.id+'</td><td>'+o.dept+'</td><td>'+o.device+'</td><td>'+ct.toLocaleString()+'</td><td>'+formatDuration(duration)+'</td><td>'+getStatusHtml(o.status)+'</td></tr>';"""
new_pending_detail = """return '<tr><td>'+o.id+'</td><td>'+o.dept+'</td><td>'+o.device+'</td><td>'+(o.desc||'-')+'</td><td>'+ct.toLocaleString()+'</td><td>'+formatDuration(duration)+'</td><td>'+getStatusHtml(o.status)+'</td></tr>';"""
content = content.replace(old_pending_detail, new_pending_detail)

# Update pending table header
content = content.replace(
    '<th>工单号</th><th>机构</th><th>设备</th><th>报修时间</th><th>工单时长</th><th>状态</th>',
    '<th>工单号</th><th>机构</th><th>设备</th><th>故障</th><th>报修时间</th><th>工单时长</th><th>状态</th>'
)

content_b64 = base64.b64encode(content.encode('utf-8')).decode('utf-8')
body = json.dumps({
    'message': 'v15b - vendors + status dropdown',
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
print('v15b done, status:', r2.status)
