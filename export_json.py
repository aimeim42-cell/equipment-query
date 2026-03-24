# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
import json

# 读取合并后的数据
df = pd.read_excel(r'C:\Users\lenovo\Desktop\表1_整理结果_合并.xlsx', sheet_name='Sheet1')

# 构建数据字典
data = {}
current_org = None

for _, row in df.iterrows():
    if pd.notna(row['归属机构号']):
        current_org = str(int(row['归属机构号']))
        if current_org not in data:
            data[current_org] = []
    
    if current_org:
        data[current_org].append({
            '设备类型': '' if pd.isna(row['设备类型']) else str(row['设备类型']),
            '设备品牌': '' if pd.isna(row['设备品牌']) else str(row['设备品牌']),
            '设备维护商': '' if pd.isna(row['设备维护商']) else str(row['设备维护商']),
            '维护负责人': '' if pd.isna(row['维护负责人']) else str(row['维护负责人']),
            '联系方式': '' if pd.isna(row['联系方式']) else str(row['联系方式'])
        })

# 保存JSON
with open(r'C:\Users\lenovo\.openclaw\workspace\data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"数据已导出，共 {len(data)} 个机构")
