# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
import json
import qrcode

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

# 生成简化版HTML
html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>设备运维查询</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Microsoft YaHei", sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; margin: 0; }
        .container { max-width: 600px; margin: 0 auto; }
        h1 { color: #fff; text-align: center; margin-bottom: 20px; font-size: 24px; }
        .search-box { background: #fff; border-radius: 12px; padding: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.15); }
        .search-box input { width: 100%; padding: 14px; font-size: 18px; border: 2px solid #ddd; border-radius: 8px; outline: none; box-sizing: border-box; text-align: center; }
        .search-box input:focus { border-color: #667eea; }
        .search-box button { width: 100%; margin-top: 12px; padding: 14px; font-size: 18px; background: #667eea; color: #fff; border: none; border-radius: 8px; cursor: pointer; }
        .result { margin-top: 15px; }
        .org-header { background: #667eea; color: #fff; padding: 12px 15px; border-radius: 10px 10px 0 0; }
        .org-header h2 { font-size: 18px; margin: 0; }
        .org-header p { font-size: 14px; margin: 5px 0 0 0; opacity: 0.9; }
        table { width: 100%; border-collapse: collapse; background: #fff; border-radius: 0 0 10px 10px; overflow: hidden; }
        th, td { padding: 10px 8px; text-align: left; border-bottom: 1px solid #eee; font-size: 13px; word-break: break-all; }
        th { background: #f5f5f5; font-weight: bold; color: #333; }
        .no-result { text-align: center; padding: 30px; color: #666; background: #fff; border-radius: 12px; }
        .tip { text-align: center; color: #fff; margin-top: 15px; font-size: 13px; opacity: 0.9; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏢 设备运维查询</h1>
        <div class="search-box">
            <input type="text" id="orgCode" placeholder="请输入机构编号（如：021001）" onkeyup="if(event.key==='Enter')search()">
            <button onclick="search()">查询</button>
        </div>
        <div id="result"></div>
        <p class="tip">共支持 ''' + str(len(data)) + ''' 个机构</p>
    </div>
    <script>
        const data = ''' + json.dumps(data, ensure_ascii=False) + ''';
        function search() {
            const code = document.getElementById('orgCode').value.trim();
            const div = document.getElementById('result');
            if (!code) { div.innerHTML = '<div class="no-result">请输入机构编号</div>'; return; }
            const arr = data[code];
            if (!arr) { div.innerHTML = '<div class="no-result">未找到机构号 <strong>' + code + '</strong><br>请检查是否以0开头</div>'; return; }
            let h = '<div class="org-header"><h2>机构：' + code + '</h2><p>共 ' + arr.length + ' 条设备信息</p></div><table><thead><tr><th>设备类型</th><th>品牌</th><th>维护商</th><th>负责人</th><th>电话</th><th>备注</th></tr></thead><tbody>';
            arr.forEach(i => { h += '<tr><td>' + i.设备类型 + '</td><td>' + i.设备品牌 + '</td><td>' + i.设备维护商 + '</td><td>' + i.维护负责人 + '</td><td>' + i.联系方式 + '</td><td>' + (i.备注||'') + '</td></tr>'; });
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

# 生成二维码
qr = qrcode.QRCode(box_size=10, border=2)
qr.add_data('file:///' + html_path.replace('\\', '/'))
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")

# 保存二维码
qr_path = r'C:\Users\lenovo\Desktop\设备运维查询_二维码.png'
img.save(qr_path)

print('完成！')
print(f'查询页面: {html_path}')
print(f'二维码: {qr_path}')
print('\n修改内容:')
print('1. 表2中空调维护等5项已添加备注"分行后勤维修群报修"')
print('2. 页面已简化，只保留输入框、按钮、结果')
print('3. 已生成二维码，手机扫码即可打开查询页面')
