# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd

# 读取原始数据
df1 = pd.read_excel(r'C:\Users\lenovo\Desktop\表1：系统设备信息表.xlsx', sheet_name='Sheet1')

# 按归属机构号排序
df1_sorted = df1.sort_values(by='归属机构号').reset_index(drop=True)

# 创建结果列表
result = []

# 按归属机构号分组
for org_code in df1_sorted['归属机构号'].unique():
    rows = df1_sorted[df1_sorted['归属机构号'] == org_code]
    for i, (_, row) in enumerate(rows.iterrows()):
        row_data = row.copy()
        if i > 0:
            row_data['归属机构号'] = None  # 同一机构的后续行，归属机构号置空
        result.append(row_data)

# 创建结果DataFrame
df_result = pd.DataFrame(result)

# 将机构号转换为文本格式，保留前面的0
df_result['归属机构号'] = df_result['归属机构号'].apply(lambda x: str(int(x)) if pd.notna(x) else None)

# 输出到Excel
output_path = r'C:\Users\lenovo\Desktop\表1_整理结果_新.xlsx'
df_result.to_excel(output_path, sheet_name='Sheet1', index=False)

print(f'完成！共处理 {len(df_result)} 行数据')
print(f'唯一机构号数量: {df1_sorted["归属机构号"].nunique()}')
print('\n前20行预览:')
print(df_result.head(20).to_string())
