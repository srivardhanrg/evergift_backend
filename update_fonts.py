import os

filepath = r'c:\Users\santh\Desktop\magicbf\magictales_backend\app\config\text_styling.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = [
    ('"font_size": 48', '"font_size": 110'),
    ('"font_size": 32', '"font_size": 80'),
    ('"font_size": 72', '"font_size": 240'),
    ('"max_width_percent": 75', '"max_width_percent": 70'),
    ('"max_width_percent": 70', '"max_width_percent": 65'),
    ('"offset_x": 1', '"offset_x": 3'),
    ('"offset_x": 2', '"offset_x": 4'),
    ('"offset_y": 2', '"offset_y": 5'),
    ('"blur": 3', '"blur": 6'),
    ('"blur": 4', '"blur": 8'),
    ('"blur": 5', '"blur": 10'),
]

for old, new in replacements:
    content = content.replace(old, new)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated text_styling.py successfully!')
