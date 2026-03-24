# -*- coding: utf-8 -*-
import pandas as pd

# 读取两个Excel文件
df1 = pd.read_excel(r'C:\Users\lenovo\Desktop\表1_匹配结果.xlsx')
df2 = pd.read_excel(r'C:\Users\lenovo\Desktop\桂林银行南宁分行机具数量（截至20221105）(1).xlsx')

print('表1（匹配结果）列名:', df1.columns.tolist())
print('表1行数:', len(df1))
print()
print('表2（机具数量）列名:', df2.columns.tolist())
print('表2行数:', len(df2))
print()
print('表2前10行:')
print(df2.head(10))
