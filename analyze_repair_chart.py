# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os
import sys

# 设置中文字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False

# 获取桌面路径
desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
files = [f for f in os.listdir(desktop) if f.startswith('报修') and f.endswith('.xlsx')]
filepath = os.path.join(desktop, files[1])

# 读取数据
df = pd.read_excel(filepath, engine='openpyxl')

# 转换数值类型
df['响应时长(小时)'] = pd.to_numeric(df['响应时长(小时)'], errors='coerce')
df['维修完成时长(小时)'] = pd.to_numeric(df['维修完成时长(小时)'], errors='coerce')
df['维修总时长(小时)'] = pd.to_numeric(df['维修总时长(小时)'], errors='coerce')
df['评价分数(满分5分)'] = pd.to_numeric(df['评价分数(满分5分)'], errors='coerce')
df['维修费用'] = pd.to_numeric(df['维修费用'], errors='coerce')

# 选取主要供应商（工单数>=5）
provider_counts = df['服务商'].value_counts()
main_providers = provider_counts[provider_counts >= 5].index.tolist()
df_main = df[df['服务商'].isin(main_providers)]

# 按供应商统计
stats = df_main.groupby('服务商').agg({
    '序号': 'count',
    '响应时长(小时)': 'mean',
    '维修完成时长(小时)': 'mean',
    '维修总时长(小时)': 'mean',
    '评价分数(满分5分)': 'mean',
    '维修费用': 'sum'
}).round(2)

stats.columns = ['工单数', '平均响应时长(h)', '平均维修时长(h)', '平均总时长(h)', '平均评分', '总维修费用']
stats = stats.sort_values('工单数', ascending=False)

print("主要供应商统计数据：")
print(stats)

# 创建图表
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('维保供应商服务效率分析报告', fontsize=16, fontweight='bold')

# 1. 工单数量柱状图
ax1 = axes[0, 0]
providers = stats.index.tolist()
order = list(range(len(providers)))
bars1 = ax1.bar(order, stats['工单数'], color='steelblue')
ax1.set_xlabel('供应商')
ax1.set_ylabel('工单数量')
ax1.set_title('各供应商工单数量')
ax1.set_xticks(order)
ax1.set_xticklabels(providers, rotation=45, ha='right', fontsize=8)
for bar, val in zip(bars1, stats['工单数']):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, str(val), 
             ha='center', va='bottom', fontsize=8)

# 2. 平均响应时长
ax2 = axes[0, 1]
bars2 = ax2.bar(order, stats['平均响应时长(h)'], color='orange')
ax2.set_xlabel('供应商')
ax2.set_ylabel('平均响应时长(小时)')
ax2.set_title('各供应商平均响应时长')
ax2.set_xticks(order)
ax2.set_xticklabels(providers, rotation=45, ha='right', fontsize=8)
for bar, val in zip(bars2, stats['平均响应时长(h)']):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, f'{val:.1f}h', 
             ha='center', va='bottom', fontsize=8)

# 3. 平均维修时长
ax3 = axes[1, 0]
bars3 = ax3.bar(order, stats['平均维修时长(h)'], color='green')
ax3.set_xlabel('供应商')
ax3.set_ylabel('平均维修时长(小时)')
ax3.set_title('各供应商平均维修时长')
ax3.set_xticks(order)
ax3.set_xticklabels(providers, rotation=45, ha='right', fontsize=8)
for bar, val in zip(bars3, stats['平均维修时长(h)']):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'{val:.1f}h', 
             ha='center', va='bottom', fontsize=8)

# 4. 平均评分
ax4 = axes[1, 1]
scores = stats['平均评分'].fillna(0)
colors = ['red' if s < 3 else 'orange' if s < 4 else 'green' for s in scores]
bars4 = ax4.bar(order, scores, color=colors)
ax4.set_xlabel('供应商')
ax4.set_ylabel('平均评分(满分5分)')
ax4.set_title('各供应商平均评分')
ax4.set_xticks(order)
ax4.set_xticklabels(providers, rotation=45, ha='right', fontsize=8)
ax4.set_ylim(0, 5.5)
for bar, val in zip(bars4, scores):
    ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, f'{val:.2f}', 
             ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.savefig(os.path.join(desktop, '维保供应商分析图表.png'), dpi=150, bbox_inches='tight')
print(f"\n图表已保存到: {os.path.join(desktop, '维保供应商分析图表.png')}")

# 创建效率对比雷达图
fig2, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(polar=True))

# 准备雷达图数据 - 只取前6个主要供应商
top_providers = stats.head(6)
categories = ['工单数量\n(归一化)', '响应速度\n(反归一化)', '维修效率\n(反归一化)', '服务质量\n(归一化)']

# 归一化数据
from matplotlib import cm
colors = cm.Set2(range(len(top_providers)))

for idx, (provider, row) in enumerate(top_providers.iterrows()):
    # 归一化处理
    work_orders = row['工单数'] / stats['工单数'].max() * 100
    response_time = (1 - row['平均响应时长(h)'] / stats['平均响应时长(h)'].max()) * 100
    repair_time = (1 - row['平均维修时长(h)'] / stats['平均维修时长(h)'].max()) * 100
    score = (row['平均评分'] / 5) * 100 if pd.notna(row['平均评分']) else 50
    
    values = [work_orders, response_time, repair_time, score]
    values += values[:1]  # 闭合图形
    
    angles = [n / float(len(categories)) * 2 * 3.14159 for n in range(len(categories))]
    angles += angles[:1]
    
    ax.plot(angles, values, 'o-', linewidth=2, label=provider[:10], color=colors[idx])
    ax.fill(angles, values, alpha=0.1, color=colors[idx])

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, size=10)
ax.set_title('主要供应商服务效率综合对比', size=14, fontweight='bold', y=1.08)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0), fontsize=8)

plt.tight_layout()
plt.savefig(os.path.join(desktop, '维保供应商效率雷达图.png'), dpi=150, bbox_inches='tight')
print(f"雷达图已保存到: {os.path.join(desktop, '维保供应商效率雷达图.png')}")

print("\n分析完成！")
