# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import os

# 获取桌面路径
desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
input_path = os.path.join(desktop, '微信图片_20260319111638_1573_8.jpg')
output_path = os.path.join(desktop, '一寸照片排版_A4.pdf')

# 读取原始图片
img = Image.open(input_path)
print(f"原始图片尺寸: {img.size}")

# A4纸尺寸 (300 DPI: 2480 x 3508 像素)
A4_WIDTH = 2480
A4_HEIGHT = 3508

# 一寸照片尺寸 (2.5cm x 3.5cm, 300 DPI: 295 x 413 像素)
PHOTO_WIDTH = 295
PHOTO_HEIGHT = 413

# 创建A4画布 (白色背景)
a4_canvas = Image.new('RGB', (A4_WIDTH, A4_HEIGHT), 'white')

#  margins
left_margin = 150
top_margin = 200
right_margin = 150
bottom_margin = 200

# Calculate available space
available_width = A4_WIDTH - left_margin - right_margin
available_height = A4_HEIGHT - top_margin - bottom_margin

# Calculate rows and columns (3 columns x 4 rows = 12 photos)
cols = 3
rows = 4
spacing_x = (available_width - cols * PHOTO_WIDTH) // (cols - 1) if cols > 1 else 0
spacing_y = (available_height - rows * PHOTO_HEIGHT) // (rows - 1) if rows > 1 else 0

print(f"布局: {cols}列 x {rows}行")
print(f"照片尺寸: {PHOTO_WIDTH} x {PHOTO_HEIGHT}")
print(f"水平间距: {spacing_x}, 垂直间距: {spacing_y}")

# 切割原始图片中的照片区域
# 从图片中可以看出是左右两排，每排6张
# 原始图片大约是 1773 x 2364
# Let's extract the photo regions

# 原始图片中照片区域的分析
# 图片显示有两列照片区域
img_w, img_h = img.size
print(f"分析原始图片: {img_w}x{img_h}")

# 切割照片 - 基于图片内容
# 左侧照片区域和右侧照片区域
photo_regions = []

# 分析图片结构 - 看起来是6+6的布局
# Let's crop the 12 photos from the original image
# Based on the image, we can see the photos are in two columns

# 估计每个照片区域的位置和大小
# 左侧列
left_photos = []
right_photos = []

# 从图片分析，照片大约占图片宽度的40%左右，分成两列
# 每列6张照片
col_width = img_w // 2 - 40  # 每列宽度
photo_h = (img_h - 200) // 6  # 每个照片高度

# 提取左侧6张照片
for i in range(6):
    top = 50 + i * (photo_h + 5)
    left_photos.append((30, top, 30 + col_width, top + photo_h - 10))

# 提取右侧6张照片  
for i in range(6):
    top = 50 + i * (photo_h + 5)
    right_photos.append((img_w // 2 + 10, top, img_w // 2 + 10 + col_width, top + photo_h - 10))

# 合并所有照片区域
all_regions = left_photos + right_photos
print(f"提取了 {len(all_regions)} 个照片区域")

# 排版到A4纸上
draw = ImageDraw.Draw(a4_canvas)

# 添加标题
try:
    font = ImageFont.truetype("arial.ttf", 60)
except:
    font = ImageFont.load_default()
    
draw.text((A4_WIDTH // 2 - 300, 50), "一寸照片排版 (12张)", fill='black', font=font)

# 排版照片
for idx, region in enumerate(all_regions):
    row = idx // cols
    col = idx % cols
    
    # 计算在A4纸上的位置
    x = left_margin + col * (PHOTO_WIDTH + spacing_x)
    y = top_margin + row * (PHOTO_HEIGHT + spacing_y)
    
    # 切割并调整照片大小
    photo = img.crop(region)
    photo = photo.resize((PHOTO_WIDTH, PHOTO_HEIGHT), Image.Resampling.LANCZOS)
    
    # 粘贴到A4画布
    a4_canvas.paste(photo, (x, y))
    
    print(f"照片 {idx+1}: 位置 ({x}, {y})")

# 添加边框（可选）
draw.rectangle([left_margin-10, top_margin-10, 
                A4_WIDTH-right_margin+10, A4_HEIGHT-bottom_margin+10], 
               outline='gray', width=2)

# 添加裁切线（可选）
for row in range(rows + 1):
    y = top_margin + row * (PHOTO_HEIGHT + spacing_y) - spacing_y//2 if row > 0 else top_margin
    if y < A4_HEIGHT - bottom_margin:
        draw.line([(left_margin, y), (A4_WIDTH - right_margin, y)], fill='lightgray', width=1)

for col in range(cols + 1):
    x = left_margin + col * (PHOTO_WIDTH + spacing_x) - spacing_x//2 if col > 0 else left_margin
    if x < A4_WIDTH - right_margin:
        draw.line([(x, top_margin), (x, A4_HEIGHT - bottom_margin)], fill='lightgray', width=1)

# 保存为PDF（可直接打印）
a4_canvas.save(output_path, 'PDF', resolution=300)
print(f"\nOutput saved to: {output_path}")

# 同时保存一张预览图
preview_path = os.path.join(desktop, '一寸照片排版_A4_预览.jpg')
a4_canvas.save(preview_path, 'JPEG', quality=95, dpi=(300, 300))
print(f"Preview saved to: {preview_path}")
