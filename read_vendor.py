# -*- coding: utf-8 -*-
import pandas as pd

df = pd.read_excel(r'C:\Users\lenovo\Desktop\设备运维供应商信息表.xlsx')

# Print with UTF-8 encoding
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("列名:", df.columns.tolist())
print()
for i, row in df.iterrows():
    print(f"{i}: {row.iloc[0]} | {row.iloc[1]} | {row.iloc[2]} | {row.iloc[3]} | {row.iloc[4]} | {row.iloc[5]}")
