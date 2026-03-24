# -*- coding: utf-8 -*-
from PIL import Image
import os

# 获取桌面路径
desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
input_path = os.path.join(desktop, '微信图片_20260319111638_1573_8.jpg')
output_path = os.path.join(desktop, '一寸照片排版_A4_重复.pdf')

# 读取原始图片
img = Image.open(input_path)
img_w, img_h = img.size
print(f"Original image size: {img_w}x{img_h}")

# A4纸尺寸 (300 DPI: 2480 x 3508 像素)
A4_WIDTH = 2480
A4_HEIGHT = 3508

# 一寸照片尺寸 (2.5cm x 3.5cm, 300 DPI: 295 x 413 像素)
PHOTO_WIDTH = 295
PHOTO_HEIGHT = 413

# 创建A4画布 (白色背景)
a4_canvas = Image.new('RGB', (A4_WIDTH, A4_HEIGHT), 'white')

# 边距
left_margin = 180
top_margin = 220
right_margin = 180
bottom_margin = 220

# 计算布局 - 3列 x 4行 = 12张
cols = 3
rows = 4
spacing_x = 80
spacing_y = 80

# 从原图中提取单个照片区域
# 基于图片结构，取右侧第一张照片（人物照片）
# 原图大约是 1773x2364，分两列，每列6张
col_width = (img_w - 60) // 2
photo_height = (img_h - 100) // 6

# 提取右侧第一张照片（人物清晰的一张）
# 位置：右侧列，第2-3张比较清晰
region = (img_w//2 + 15, photo_height + 20, 
          img_w//2 + 15 + col_width - 10, photo_height + 20 + photo_height - 15)

print(f"Extracting region: {region}")
single_photo = img.crop(region)
print(f"Single photo size: {single_photo.size}")

# 调整为一寸照片尺寸
photo = single_photo.resize((PHOTO_WIDTH, PHOTO_HEIGHT), Image.Resampling.LANCZOS)
print(f"Resized photo: {photo.size}")

# 排版12张相同的照片到A4纸上
for idx in range(12):
    row = idx // cols
    col = idx % cols
    
    # 计算在A4纸上的位置
    x = left_margin + col * (PHOTO_WIDTH + spacing_x)
    y = top_margin + row * (PHOTO_HEIGHT + spacing_y)
    
    # 粘贴照片到A4画布
    a4_canvas.paste(photo, (x, y))
    
    print(f"Photo {idx+1}: position ({x}, {y})")

# 添加简单的裁切辅助线（浅色）
from PIL import ImageDraw
draw = ImageDraw.Draw(a4_canvas)

# 绘制外框
draw.rectangle([left_margin-5, top_margin-5, 
                A4_WIDTH-right_margin+5, A4_HEIGHT-bottom_margin+5], 
               outline='#cccccc', width=1)

# 保存为PDF
a4_canvas.save(output_path, 'PDF', resolution=300)
print(f"\nOutput saved: {output_path}")

# 保存预览图
preview_path = os.path.join(desktop, '一寸照片排版_A4_重复_预览.jpg')
a4_canvas.save(preview_path, 'JPEG', quality=95)
print(f"Preview saved: {preview_path}")
