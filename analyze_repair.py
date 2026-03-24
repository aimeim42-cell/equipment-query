# -*- coding: utf-8 -*-
import pandas as pd
import os
import sys

# 设置输出编码
sys.stdout.reconfigure(encoding='utf-8')

desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
files = [f for f in os.listdir(desktop) if f.startswith('报修') and f.endswith('.xlsx')]

filepath = os.path.join(desktop, files[1])
print(f'读取文件: {filepath}\n')

df = pd.read_excel(filepath, engine='openpyxl')

# 转换为数值类型
df['响应时长(小时)'] = pd.to_numeric(df['响应时长(小时)'], errors='coerce')
df['维修完成时长(小时)'] = pd.to_numeric(df['维修完成时长(小时)'], errors='coerce')
df['维修总时长(小时)'] = pd.to_numeric(df['维修总时长(小时)'], errors='coerce')
df['评价分数(满分5分)'] = pd.to_numeric(df['评价分数(满分5分)'], errors='coerce')
df['维修费用'] = pd.to_numeric(df['维修费用'], errors='coerce')

# 按维保单位（服务商）分组分析
print("=" * 80)
print("各维保供应商服务效率分析")
print("=" * 80)

# 统计各供应商的工单数量
provider_stats = df.groupby('服务商').agg({
    '序号': 'count',  # 工单总数
    '响应时长(小时)': ['mean', 'min', 'max'],  # 响应时间
    '维修完成时长(小时)': ['mean', 'min', 'max'],  # 维修完成时间
    '维修总时长(小时)': ['mean', 'min', 'max'],  # 维修总时长
    '评价分数(满分5分)': 'mean',  # 平均评分
    '维修费用': 'sum'  # 总维修费用
}).round(2)

provider_stats.columns = ['工单数', '平均响应时长(h)', '最快响应(h)', '最慢响应(h)',
                          '平均维修时长(h)', '最快维修(h)', '最慢维修(h)',
                          '平均总时长(h)', '最快总时长(h)', '最慢总时长(h)',
                          '平均评分', '总维修费用']

provider_stats = provider_stats.sort_values('工单数', ascending=False)

print("\n=== 各供应商服务效率统计 ===\n")
print(provider_stats.to_string())

# 计算超时率
print("\n\n=== 超时情况分析 ===")
# 假设响应时长超过1小时为超时，维修超过4小时为超时
df['响应超时'] = df['响应时长(小时)'] > 1
df['维修超时'] = df['维修完成时长(小时)'] > 4

timeout_stats = df.groupby('服务商').agg({
    '序号': 'count',
    '响应超时': lambda x: x.sum(),
    '维修超时': lambda x: x.sum()
}).rename(columns={'序号': '工单数', '响应超时': '响应超时数', '维修超时': '维修超时数'})

timeout_stats['响应超时率'] = (timeout_stats['响应超时数'] / timeout_stats['工单数'] * 100).round(2)
timeout_stats['维修超时率'] = (timeout_stats['维修超时数'] / timeout_stats['工单数'] * 100).round(2)

print(timeout_stats.sort_values('工单数', ascending=False).to_string())

# 输出到CSV
output_path = os.path.join(desktop, '维保供应商分析报告.csv')
provider_stats.to_csv(output_path, encoding='utf-8-sig')
print(f"\n\n详细报告已保存到: {output_path}")
