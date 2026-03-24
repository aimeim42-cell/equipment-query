# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
import json

# 读取合并后的数据
df = pd.read_excel(r'C:\Users\lenovo\Desktop\表1_整理结果_合并.xlsx', sheet_name='Sheet1')

# 读取表2的固定内容
df2 = pd.read_excel(r'C:\Users\lenovo\Desktop\表2：网点设备信息表.xlsx')

# 处理表2数据
fixed_content = []
for _, row in df2.iterrows():
    fixed_content.append({
        '设备类型': '' if pd.isna(row['设备类型']) else str(row['设备类型']),
        '设备品牌': '' if pd.isna(row['设备品牌']) else str(row['设备品牌']),
        '设备维护商': '' if pd.isna(row['设备维护商']) else str(row['设备维护商']),
        '维护负责人': '' if pd.isna(row['维护负责人']) else str(row['维护负责人']),
        '联系方式': '' if pd.isna(row['联系方式']) else str(int(row['联系方式'])) if not pd.isna(row['联系方式']) else '',
        '备注': '' if pd.isna(row['备注']) else str(row['备注'])
    })

print("表2固定内容:")
for item in fixed_content:
    print(item)

# 构建数据字典
data = {}
current_org = None

for _, row in df.iterrows():
    if pd.notna(row['归属机构号']):
        # 机构号前面加0
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
            '备注': '故障请在安保APP报修'  # 添加备注
        })

# 为每个机构添加表2的固定内容
for org in data:
    data[org].extend(fixed_content)

# 生成HTML
html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>设备运维信息查询</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: "Microsoft YaHei", sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
        .container { max-width: 1100px; margin: 0 auto; }
        h1 { color: #fff; text-align: center; margin-bottom: 30px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
        .search-box { background: #fff; border-radius: 12px; padding: 30px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); }
        .search-box label { display: block; margin-bottom: 10px; font-weight: bold; color: #333; }
        .search-box input { width: 100%; padding: 12px 15px; font-size: 16px; border: 2px solid #ddd; border-radius: 8px; outline: none; transition: border-color 0.3s; }
        .search-box input:focus { border-color: #667eea; }
        .search-box button { width: 100%; margin-top: 15px; padding: 12px; font-size: 16px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #fff; border: none; border-radius: 8px; cursor: pointer; transition: transform 0.2s; }
        .search-box button:hover { transform: translateY(-2px); }
        .result { margin-top: 20px; }
        .org-header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #fff; padding: 15px 20px; border-radius: 12px 12px 0 0; }
        .org-header h2 { font-size: 20px; }
        .org-header p { font-size: 14px; opacity: 0.9; margin-top: 5px; }
        table { width: 100%; border-collapse: collapse; background: #fff; border-radius: 0 0 12px 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }
        th, td { padding: 12px 15px; text-align: left; border-bottom: 1px solid #eee; font-size: 14px; }
        th { background: #f8f9fa; font-weight: bold; color: #333; }
        tr:hover { background: #f8f9fa; }
        tr:last-child td { border-bottom: none; }
        .no-result { text-align: center; padding: 40px; color: #666; background: #fff; border-radius: 12px; }
        .tip { text-align: center; color: #fff; margin-top: 20px; font-size: 14px; }
        .quick-btns { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 15px; justify-content: center; }
        .quick-btn { padding: 6px 12px; font-size: 12px; background: #f0f0f0; border: none; border-radius: 4px; cursor: pointer; transition: background 0.2s; }
        .quick-btn:hover { background: #667eea; color: #fff; }
        .note-row { background: #fff3cd !important; }
        .note-row td { color: #856404; font-style: italic; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏢 设备运维信息查询系统</h1>
        <div class="search-box">
            <label for="orgCode">请输入机构编号（需以0开头）：</label>
            <input type="text" id="orgCode" placeholder="例如：021001" onkeyup="if(event.key==='Enter')search()">
            <button onclick="search()">查询</button>
            <div class="quick-btns">
                <button class="quick-btn" onclick="setCode('021001')">021001</button>
                <button class="quick-btn" onclick="setCode('021002')">021002</button>
                <button class="quick-btn" onclick="setCode('021003')">021003</button>
                <button class="quick-btn" onclick="setCode('021004')">021004</button>
                <button class="quick-btn" onclick="setCode('022001')">022001</button>
                <button class="quick-btn" onclick="setCode('022002')">022002</button>
                <button class="quick-btn" onclick="setCode('022003')">022003</button>
            </div>
        </div>
        <div id="result" class="result"></div>
        <p class="tip">💡 提示：输入机构号后按回车或点击查询按钮 | 共支持 ''' + str(len(data)) + ''' 个机构查询</p>
    </div>

    <script>
        // 完整数据
        const data = ''' + json.dumps(data, ensure_ascii=False) + ''';

        function setCode(code) {
            document.getElementById('orgCode').value = code;
            search();
        }

        function search() {
            const orgCode = document.getElementById('orgCode').value.trim();
            const resultDiv = document.getElementById('result');
            
            if (!orgCode) {
                resultDiv.innerHTML = '<div class="no-result">请输入机构编号</div>';
                return;
            }

            const orgData = data[orgCode];
            
            if (!orgData) {
                resultDiv.innerHTML = '<div class="no-result">机构号 <strong>' + orgCode + '</strong> 未找到，请检查输入是否正确<br><br>机构号需以0开头，如：021001</div>';
                return;
            }

            let html = `
                <div class="org-header">
                    <h2>🏢 机构编号：''' + '${orgCode}' + '''</h2>
                    <p>共 ''' + '${orgData.length}' + ''' 条设备运维信息</p>
                </div>
                <table>
                    <thead>
                        <tr>
                            <th>设备类型</th>
                            <th>设备品牌</th>
                            <th>设备维护商</th>
                            <th>维护负责人</th>
                            <th>联系方式</th>
                            <th>备注</th>
                        </tr>
                    </thead>
                    <tbody>
            `;
            
            orgData.forEach((item, index) => {
                let rowClass = '';
                if (item.备注 && item.备注 !== '故障请在安保APP报修') {
                    rowClass = 'note-row';
                }
                html += `
                    <tr class="${rowClass}">
                        <td>${item.设备类型}</td>
                        <td>${item.设备品牌}</td>
                        <td>${item.设备维护商}</td>
                        <td>${item.维护负责人}</td>
                        <td>${item.联系方式}</td>
                        <td>${item.备注 || ''}</td>
                    </tr>
                `;
            });
            
            html += '</tbody></table>';
            resultDiv.innerHTML = html;
        }
    </script>
</body>
</html>'''

# 保存HTML
with open(r'C:\Users\lenovo\Desktop\设备运维查询系统.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f'\n查询系统已更新！')
print(f'文件位置: C:\\Users\\lenovo\\Desktop\\设备运维查询系统.html')
print(f'支持查询 {len(data)} 个机构')
print('\n修改内容:')
print('1. 机构号前已加0（如21001变为021001）')
print('2. 表头已添加备注字段，设备信息备注为"故障请在安保APP报修"')
print('3. 已加入表2的固定内容到每个网点')
