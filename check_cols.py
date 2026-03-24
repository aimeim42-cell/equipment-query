# -*- coding: utf-8 -*-
import pandas as pd

# 读取两个Excel文件
df1 = pd.read_excel(r'C:\Users\lenovo\Desktop\表1_整理结果_合并.xlsx')
df3 = pd.read_excel(r'C:\Users\lenovo\Desktop\表3：机构号网点名称对应表.xlsx')

print('表1列名:', df1.columns.tolist())
print('表3列名:', df3.columns.tolist())
print('表1行数:', len(df1))
print('表3行数:', len(df3))
