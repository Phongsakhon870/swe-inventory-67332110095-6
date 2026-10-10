"""
สร้างภาพจำลอง GitHub Projects Kanban Board สำหรับ Sprint 1 (Lab 02)
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# สร้างโฟลเดอร์ screenshots
Path("screenshots").mkdir(parents=True, exist_ok=True)

# กำหนดขนาดภาพ
width = 1360
height = 760
image = Image.new("RGB", (width, height), (13, 17, 23))  # พื้นหลัง Dark Mode สไตล์ GitHub (#0d1117)
draw = ImageDraw.Draw(image)

# ฟอนต์
try:
    font_large_bold = ImageFont.truetype("C:/Windows/Fonts/tahomabd.ttf", 22)
    font_medium_bold = ImageFont.truetype("C:/Windows/Fonts/tahomabd.ttf", 15)
    font_medium = ImageFont.truetype("C:/Windows/Fonts/tahoma.ttf", 14)
    font_small = ImageFont.truetype("C:/Windows/Fonts/tahoma.ttf", 12)
    font_mono = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 13)
except Exception:
    font_large_bold = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 22)
    font_medium_bold = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 15)
    font_medium = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 14)
    font_small = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 12)
    font_mono = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 13)

# 1. Header Bar ด้านบน
draw.rectangle([(0, 0), (width, 60)], fill=(22, 27, 34))  # #161b22
draw.line([(0, 60), (width, 60)], fill=(48, 54, 61), width=1)  # #30363d

# ไอคอน + Breadcrumb
draw.text((25, 18), "Phongsakhon870 / swe-inventory-67332110095-6", fill=(88, 166, 255), font=font_medium_bold)
draw.text((450, 18), "> Projects >", fill=(139, 148, 158), font=font_medium)
draw.text((545, 18), "Sprint 1 Board (Store Inventory CLI)", fill=(240, 246, 252), font=font_medium_bold)

# Sprint Goal Sub-header
draw.rectangle([(0, 61), (width, 105)], fill=(13, 17, 23))
draw.line([(0, 105), (width, 105)], fill=(48, 54, 61), width=1)
draw.text((25, 73), "Sprint Goal:", fill=(63, 185, 80), font=font_medium_bold)
draw.text((120, 74), "ส่งมอบระบบสต็อกร้านเขียนดี (US-01, US-02, US-03) ที่รันได้จริง ผ่าน AC 100% | WIP Limit: 1", fill=(201, 209, 217), font=font_medium)

# สถานะ Velocity Tag ขวาบน
draw.rounded_rectangle([(1020, 70), (1335, 96)], radius=6, fill=(33, 38, 45), outline=(48, 54, 61))
draw.text((1035, 74), "Velocity: 13 / 13 pts (Done 100%)", fill=(63, 185, 80), font=font_small)

# 2. คอลัมน์ Kanban 4 คอลัมน์
columns = [
    {"title": "To Do", "count": 2, "color": (139, 148, 158), "wip": None},
    {"title": "In Progress", "count": 0, "color": (210, 153, 34), "wip": "WIP: 0/1"},
    {"title": "In Review", "count": 0, "color": (163, 113, 247), "wip": None},
    {"title": "Done", "count": 3, "color": (63, 185, 80), "wip": "13 pts"},
]

col_width = 310
gap = 20
start_x = 25
start_y = 120

cards_data = {
    0: [  # To Do
        {
            "id": "#4",
            "title": "US-04: ค้นหาสินค้าตามชื่อ/รหัส",
            "sub": "AC-1, AC-2: ค้นหาบางส่วน แสดงผลตรง",
            "priority": "Should have",
            "p_color": (210, 153, 34),
            "points": "5 pts",
            "assignee": "Dev",
        },
        {
            "id": "#5",
            "title": "US-05: ส่งออกรายงานเป็น CSV",
            "sub": "AC-1, AC-2: ส่งออกตารางข้อมูลสต็อกครบ",
            "priority": "Could have",
            "p_color": (139, 148, 158),
            "points": "3 pts",
            "assignee": "Dev",
        },
    ],
    1: [],  # In Progress
    2: [],  # In Review
    3: [  # Done
        {
            "id": "#1",
            "title": "US-01: ดูรายการสินค้าคงเหลือ",
            "sub": "list_items() และจัดการกรณีคลังว่างเปล่า",
            "priority": "Must have",
            "p_color": (248, 81, 73),
            "points": "3 pts",
            "status": "Merged PR #1",
            "assignee": "Phongsakhon",
        },
        {
            "id": "#2",
            "title": "US-02: เพิ่มสินค้าใหม่เข้าระบบ",
            "sub": "add_item() ตรวจสอบป้องกันรหัสสินค้าซ้ำ",
            "priority": "Must have",
            "p_color": (248, 81, 73),
            "points": "5 pts",
            "status": "Merged PR #2",
            "assignee": "Phongsakhon",
        },
        {
            "id": "#3",
            "title": "US-03: ปรับปรุงยอดสต็อกรับ/จ่าย",
            "sub": "update_quantity() ป้องกันสต็อกติดลบ",
            "priority": "Must have",
            "p_color": (248, 81, 73),
            "points": "5 pts",
            "status": "Merged PR #3",
            "assignee": "Phongsakhon",
        },
    ],
}

for i, col in enumerate(columns):
    cx = start_x + i * (col_width + gap)
    cy = start_y
    ch = 600

    # กล่องคอลัมน์
    draw.rounded_rectangle([(cx, cy), (cx + col_width, cy + ch)], radius=8, fill=(22, 27, 34), outline=(48, 54, 61), width=1)

    # Header คอลัมน์
    draw.text((cx + 14, cy + 12), col["title"], fill=(240, 246, 252), font=font_medium_bold)

    # Badge จำนวน
    draw.rounded_rectangle([(cx + 125, cy + 12), (cx + 150, cy + 32)], radius=10, fill=(33, 38, 45))
    draw.text((cx + 133, cy + 14), str(col["count"]), fill=(139, 148, 158), font=font_small)

    if col["wip"]:
        wip_bg = (33, 38, 45) if "0/1" in col["wip"] else (26, 46, 30)
        wip_fg = (210, 153, 34) if "0/1" in col["wip"] else (63, 185, 80)
        draw.rounded_rectangle([(cx + 215, cy + 12), (cx + 295, cy + 32)], radius=6, fill=wip_bg)
        draw.text((cx + 225, cy + 14), col["wip"], fill=wip_fg, font=font_small)

    draw.line([(cx, cy + 44), (cx + col_width, cy + 44)], fill=(48, 54, 61), width=1)

    # การ์ดในคอลัมน์
    cards = cards_data.get(i, [])
    if not cards:
        draw.text((cx + 80, cy + 100), "ไม่มีการ์ดค้าง", fill=(72, 79, 88), font=font_medium)
    else:
        card_y = cy + 55
        for card in cards:
            card_h = 150
            # กรอบการ์ด
            draw.rounded_rectangle([(cx + 10, card_y), (cx + col_width - 10, card_y + card_h)], radius=6, fill=(13, 17, 23), outline=(48, 54, 61), width=1)

            # Issue ID & Title
            draw.text((cx + 20, card_y + 12), card["id"], fill=(88, 166, 255), font=font_mono)
            draw.text((cx + 50, card_y + 12), card["title"][:27], fill=(240, 246, 252), font=font_medium_bold)

            # Subtitle
            draw.text((cx + 20, card_y + 38), card["sub"][:33], fill=(139, 148, 158), font=font_small)

            # Priority Badge
            p_text = card["priority"]
            draw.rounded_rectangle([(cx + 20, card_y + 70), (cx + 105, card_y + 92)], radius=4, fill=(33, 38, 45), outline=card["p_color"])
            draw.text((cx + 26, card_y + 73), p_text, fill=card["p_color"], font=font_small)

            # Points Badge
            pts_text = card["points"]
            draw.rounded_rectangle([(cx + 115, card_y + 70), (cx + 165, card_y + 92)], radius=4, fill=(33, 38, 45))
            draw.text((cx + 122, card_y + 73), pts_text, fill=(201, 209, 217), font=font_small)

            # Status / PR
            if "status" in card:
                draw.rounded_rectangle([(cx + 20, card_y + 106), (cx + 125, card_y + 132)], radius=4, fill=(35, 78, 47))
                draw.text((cx + 27, card_y + 112), f"✓ {card['status']}", fill=(63, 185, 80), font=font_small)

            # Assignee Avatar Badge
            av_x = cx + col_width - 125
            av_y = card_y + 108
            draw.ellipse([(av_x, av_y), (av_x + 20, av_y + 20)], fill=(88, 166, 255))
            draw.text((av_x + 6, av_y + 3), card["assignee"][0], fill=(13, 17, 23), font=font_small)
            draw.text((av_x + 26, av_y + 4), card["assignee"], fill=(139, 148, 158), font=font_small)

            card_y += card_h + 15

# บันทึกไฟล์
output_path = Path("screenshots/board-sprint-1.png")
image.save(output_path, "PNG")
print("Saved Kanban Board successfully.")

