# -*- coding: utf-8 -*-
import pandas as pd

# 读取两个Excel文件
df1 = pd.read_excel(r'C:\Users\lenovo\Desktop\表1_匹配结果.xlsx')
df2 = pd.read_excel(r'C:\Users\lenovo\Desktop\桂林银行南宁分行机具数量（截至20221105）(1).xlsx', header=None)

print('表2完整内容:')
print(df2)
