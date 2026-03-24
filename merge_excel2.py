# -*- coding: utf-8 -*-
import pandas as pd

# 读取两个Excel文件
df1 = pd.read_excel(r'C:\Users\lenovo\Desktop\表1_整理结果_合并.xlsx')
df3 = pd.read_excel(r'C:\Users\lenovo\Desktop\表3：机构号网点名称对应表.xlsx')

# 重命名列
df1.columns = ['机构编号', '设备名称', '设备品牌', '设备维护方', '维护人员', '联系方式', '备注']
df3.columns = ['机构编号', '网点名称']

# 转换机构编号为整数类型（用于匹配）
df1['机构编号'] = pd.to_numeric(df1['机构编号'], errors='coerce')
df3['机构编号'] = pd.to_numeric(df3['机构编号'], errors='coerce')

# 合并两个表
result = pd.merge(df1, df3, on='机构编号', how='left')

# 把网点名称放到第一列（设备名称前面）
cols = result.columns.tolist()
# 重新排列：机构编号, 网点名称, 其他
new_cols = ['机构编号', '网点名称', '设备名称', '设备品牌', '设备维护方', '维护人员', '联系方式', '备注']
result = result[new_cols]

# 保存结果
result.to_excel(r'C:\Users\lenovo\Desktop\表1_匹配结果.xlsx', index=False)

print('匹配完成！')
print('总行数:', len(result))
print('成功匹配的行数:', result['网点名称'].notna().sum())
print()
print('前10行预览:')
print(result.head(10))
