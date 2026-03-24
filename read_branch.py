# -*- coding: utf-8 -*-
import pandas as pd
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Read the new Excel file
file_path = r'C:\Users\lenovo\Desktop\运维效率提升方案\南宁分行网点设备信息表（报修信息反显）.xlsx'

# Check all sheets
xl = pd.ExcelFile(file_path)
print("Sheets:", xl.sheet_names)

# Read first sheet to see structure
for sheet in xl.sheet_names:
    print(f"\n=== Sheet: {sheet} ===")
    df = pd.read_excel(xl, sheet_name=sheet)
    print("Columns:", df.columns.tolist()[:10])
    print("Rows:", len(df))
    print(df.head(3).to_string())
