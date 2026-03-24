# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
import json

# 读取表3 机构号与网点名称对应表
df3 = pd.read_excel(r'C:\Users\lenovo\Desktop\表3：机构号网点名称对应表.xlsx')

# 构建机构号-网点名称映射
org_map = {}
for _, row in df3.iterrows():
    org_code = '0' + str(int(row['归属机构号'])) if pd.notna(row['归属机构号']) else None
    org_name = str(row['归属机构名称']) if pd.notna(row['归属机构名称']) else ''
    if org_code:
        org_map[org_code] = org_name

# 读取合并后的数据
df = pd.read_excel(r'C:\Users\lenovo\Desktop\表1_整理结果_合并.xlsx', sheet_name='Sheet1')

# 读取表2的固定内容
df2 = pd.read_excel(r'C:\Users\lenovo\Desktop\表2：网点设备信息表.xlsx')

# 需要添加备注的设备类型
note_types = ['空调维护', '零星维修', '叫号机/宣传屏', '征信查询机', '移动营销/底座/GPS']

# 处理表2数据
fixed_content = []
for _, row in df2.iterrows():
    device_type = '' if pd.isna(row['设备类型']) else str(row['设备类型'])
    remark = ''
    if pd.isna(row['备注']) and device_type in note_types:
        remark = '分行后勤维修群报修'
    else:
        remark = '' if pd.isna(row['备注']) else str(row['备注'])
    
    fixed_content.append({
        '设备类型': device_type,
        '设备品牌': '' if pd.isna(row['设备品牌']) else str(row['设备品牌']),
        '设备维护商': '' if pd.isna(row['设备维护商']) else str(row['设备维护商']),
        '维护负责人': '' if pd.isna(row['维护负责人']) else str(row['维护负责人']),
        '联系方式': '' if pd.isna(row['联系方式']) else str(int(row['联系方式'])),
        '备注': remark
    })

# 构建数据字典
data = {}
current_org = None

for _, row in df.iterrows():
    if pd.notna(row['归属机构号']):
        current_org = '0' + str(int(row['归属机构号']))
        if current_org not in data:
            data[current_org] = []
    
    if current_org:
        data[current_org].append({
            '设备类型': '' if pd.isna(row['设备类型']) else str(row['设备类型']),
            '设备品牌': '' if pd.isna(row['设备品牌']) else str(row['设备品牌']),
            '设备维护商': '' if pd.isna(row['设备维护商']) else str(row['设备维护商']),
            '维护负责人': '' if pd.isna(row['维护负责人']) else str(row['维护负责人']),
            '联系方式': '' if pd.isna(row['联系方式']) else str(int(row['联系方式'])),
            '备注': '故障请在安保APP报修'
        })

# 为每个机构添加表2的固定内容
for org in data:
    data[org].extend(fixed_content)

# 生成HTML（支持模糊查询，添加序号）
html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>设备运维查询</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Microsoft YaHei", sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 15px; margin: 0; }
        .container { max-width: 650px; margin: 0 auto; }
        h1 { color: #fff; text-align: center; margin-bottom: 15px; font-size: 22px; }
        .search-box { background: #fff; border-radius: 12px; padding: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.15); }
        .search-box input { width: 100%; padding: 12px; font-size: 16px; border: 2px solid #ddd; border-radius: 8px; outline: none; box-sizing: border-box; text-align: center; margin-bottom: 10px; }
        .search-box input:focus { border-color: #667eea; }
        .search-box button { width: 100%; padding: 12px; font-size: 16px; background: #667eea; color: #fff; border: none; border-radius: 8px; cursor: pointer; }
        .result { margin-top: 15px; }
        .org-header { background: #667eea; color: #fff; padding: 12px 15px; border-radius: 10px 10px 0 0; }
        .org-header h2 { font-size: 17px; margin: 0; }
        .org-header p { font-size: 13px; margin: 5px 0 0 0; opacity: 0.9; }
        table { width: 100%; border-collapse: collapse; background: #fff; border-radius: 0 0 10px 10px; overflow: hidden; }
        th, td { padding: 8px 4px; text-align: center; border-bottom: 1px solid #eee; font-size: 11px; word-break: break-all; }
        th { background: #f5f5f5; font-weight: bold; color: #333; }
        th:first-child, td:first-child { width: 35px; text-align: center; }
        td { text-align: center; }
        td:nth-child(3), td:nth-child(4) { text-align: left; }
        th:nth-child(3), th:nth-child(4) { text-align: left; }
        .no-result { text-align: center; padding: 25px; color: #666; background: #fff; border-radius: 12px; }
        .suggestions { background: #fff; border-radius: 0 0 10px 10px; max-height: 200px; overflow-y: auto; display: none; }
        .suggestions div { padding: 10px 15px; border-bottom: 1px solid #eee; cursor: pointer; }
        .suggestions div:hover { background: #f5f5f5; }
        .suggestions .code { color: #667eea; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏢 设备运维查询</h1>
        <div class="search-box">
            <input type="text" id="searchInput" placeholder="请输入机构号或网点名称" oninput="showSuggestions()" onkeyup="if(event.key==='Enter')search()">
            <div id="suggestions" class="suggestions"></div>
            <button onclick="search()">查询</button>
        </div>
        <div id="result"></div>
    </div>
    <script>
        const data = ''' + json.dumps(data, ensure_ascii=False) + ''';
        const orgMap = ''' + json.dumps(org_map, ensure_ascii=False) + ''';
        
        function showSuggestions() {
            const input = document.getElementById('searchInput').value.trim().toLowerCase();
            const sugDiv = document.getElementById('suggestions');
            if (!input) { sugDiv.style.display = 'none'; return; }
            let matches = [];
            for (let code in orgMap) {
                if (code.toLowerCase().includes(input) || orgMap[code].toLowerCase().includes(input)) {
                    matches.push({code: code, name: orgMap[code]});
                }
            }
            if (matches.length === 0) { sugDiv.style.display = 'none'; return; }
            let html = '';
            matches.slice(0, 10).forEach(m => {
                html += '<div onclick="selectCode(\\'' + m.code + '\\')"><span class="code">' + m.code + '</span> - ' + m.name + '</div>';
            });
            sugDiv.innerHTML = html;
            sugDiv.style.display = 'block';
        }
        
        function selectCode(code) {
            document.getElementById('searchInput').value = code;
            document.getElementById('suggestions').style.display = 'none';
            search();
        }
        
        function search() {
            const code = document.getElementById('searchInput').value.trim();
            const div = document.getElementById('result');
            document.getElementById('suggestions').style.display = 'none';
            if (!code) { div.innerHTML = '<div class="no-result">请输入机构号或网点名称</div>'; return; }
            let matchedCode = null;
            if (data[code]) { matchedCode = code; }
            else {
                for (let c in orgMap) {
                    if (c === code || orgMap[c].includes(code)) { matchedCode = c; break; }
                }
            }
            if (!matchedCode) { div.innerHTML = '<div class="no-result">未找到匹配结果<br>机构号需以0开头</div>'; return; }
            const arr = data[matchedCode];
            const orgName = orgMap[matchedCode] || '';
            let h = '<div class="org-header"><h2>🏢 ' + orgName + '</h2><p>机构号：' + matchedCode + ' | 共' + arr.length + '条设备信息</p></div><table><thead><tr><th>序号</th><th>类型</th><th>品牌</th><th>维护商</th><th>负责人</th><th>电话</th><th>备注</th></tr></thead><tbody>';
            arr.forEach((i, idx) => { h += '<tr><td>' + (idx+1) + '</td><td>' + i.设备类型 + '</td><td>' + i.设备品牌 + '</td><td>' + i.设备维护商 + '</td><td>' + i.维护负责人 + '</td><td>' + i.联系方式 + '</td><td>' + (i.备注||'') + '</td></tr>'; });
            h += '</tbody></table>';
            div.innerHTML = h;
        }
    </script>
</body>
</html>'''

# 保存HTML
html_path = r'C:\Users\lenovo\Desktop\设备运维查询.html'
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print('完成！')
print(f'文件: {html_path}')
print('\n已添加序号字段，从1开始排序，表头居中显示')
