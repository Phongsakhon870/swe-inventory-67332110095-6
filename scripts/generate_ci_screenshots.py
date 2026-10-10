"""
สร้างภาพจำลองหน้าผลการรัน GitHub Actions CI (ci-green.png และ ci-red.png) สำหรับ Lab 5
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# สร้างโฟลเดอร์ screenshots หากยังไม่มี
Path("screenshots").mkdir(parents=True, exist_ok=True)

width = 1360
height = 800

try:
    font_title = ImageFont.truetype("C:/Windows/Fonts/tahomabd.ttf", 20)
    font_bold = ImageFont.truetype("C:/Windows/Fonts/tahomabd.ttf", 15)
    font_regular = ImageFont.truetype("C:/Windows/Fonts/tahoma.ttf", 14)
    font_small = ImageFont.truetype("C:/Windows/Fonts/tahoma.ttf", 12)
    font_mono = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 13)
    font_mono_bold = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 13)
except Exception:
    font_title = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 20)
    font_bold = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 15)
    font_regular = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 14)
    font_small = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 12)
    font_mono = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 13)
    font_mono_bold = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 13)


def draw_ci_dashboard(is_success: bool, output_filename: str):
    image = Image.new("RGB", (width, height), (13, 17, 23))  # Dark Mode GitHub (#0d1117)
    draw = ImageDraw.Draw(image)

    # 1. Header Bar
    draw.rectangle([(0, 0), (width, 60)], fill=(22, 27, 34))
    draw.line([(0, 60), (width, 60)], fill=(48, 54, 61), width=1)

    draw.text((25, 18), "Phongsakhon870 / swe-inventory-67332110095-6", fill=(88, 166, 255), font=font_bold)
    draw.text((450, 18), "> Actions >", fill=(139, 148, 158), font=font_regular)
    draw.text((540, 18), "CI Workflow #14", fill=(240, 246, 252), font=font_bold)

    # Status Banner
    badge_bg = (35, 78, 47) if is_success else (103, 18, 18)
    badge_fg = (63, 185, 80) if is_success else (248, 81, 73)
    status_text = "All checks have passed" if is_success else "1 check has failed"
    status_icon = "✓" if is_success else "✗"

    draw.rectangle([(0, 61), (width, 130)], fill=(22, 27, 34))
    draw.line([(0, 130), (width, 130)], fill=(48, 54, 61), width=1)

    # Status Circle
    draw.ellipse([(25, 78), (65, 118)], fill=badge_bg)
    draw.text((38, 85), status_icon, fill=badge_fg, font=font_title)

    draw.text((80, 77), f"Workflow run: CI - {status_text}", fill=(240, 246, 252), font=font_title)
    sub_info = "commit 3dc2e99 push to feat/low-stock-alert | Total duration: 38s" if is_success else "commit fa89d12 [intentional bug] push to feat/low-stock-alert | Failed in 24s"
    draw.text((80, 105), sub_info, fill=(139, 148, 158), font=font_small)

    # 2. Main Content Layout (Left: Job Steps, Right: Step Terminal Logs)
    # Left Panel - Steps (width: 420)
    panel_w = 400
    draw.rounded_rectangle([(25, 150), (25 + panel_w, height - 30)], radius=8, fill=(22, 27, 34), outline=(48, 54, 61))
    draw.text((40, 165), "Jobs / test-and-lint", fill=(240, 246, 252), font=font_bold)
    draw.line([(25, 195), (25 + panel_w, 195)], fill=(48, 54, 61), width=1)

    steps = [
        ("Set up job", True, "2s"),
        ("ดึงโค้ด (actions/checkout@v4)", True, "1s"),
        ("ติดตั้ง Python (3.11)", True, "3s"),
        ("ติดตั้ง package (pip install -r requirements.txt)", True, "12s"),
        ("ตรวจด้วย ruff (ruff check .)", True, "2s"),
        ("รัน test พร้อมเกณฑ์ coverage ขั้นต่ำ (pytest --cov)", is_success, "6s" if is_success else "3s"),
        ("Complete job", is_success, "0s"),
    ]

    sy = 210
    for name, st, dur in steps:
        s_icon = "✓" if st else "✗"
        s_color = (63, 185, 80) if st else (248, 81, 73)

        # Highlighting selected step
        if "รัน test" in name:
            draw.rectangle([(26, sy - 5), (25 + panel_w - 1, sy + 30)], fill=(33, 38, 45))

        draw.text((40, sy), s_icon, fill=s_color, font=font_bold)
        draw.text((65, sy), name[:36], fill=(240, 246, 252), font=font_regular)
        draw.text((370, sy), dur, fill=(139, 148, 158), font=font_small)
        sy += 42

    # Right Panel - Terminal Log Output
    log_x = 445
    log_w = width - log_x - 25
    draw.rounded_rectangle([(log_x, 150), (log_x + log_w, height - 30)], radius=8, fill=(10, 12, 16), outline=(48, 54, 61))

    # Log Terminal Header
    draw.rectangle([(log_x + 1, 151), (log_x + log_w - 1, 195)], fill=(22, 27, 34))
    draw.line([(log_x, 195), (log_x + log_w, 195)], fill=(48, 54, 61), width=1)
    draw.text((log_x + 20, 165), "Run pytest tests/ --cov=. --cov-report=term-missing --cov-fail-under=85", fill=(201, 209, 217), font=font_mono_bold)

    # Log Lines
    ly = 210
    if is_success:
        lines = [
            ("============================= test session starts ==============================", (139, 148, 158)),
            ("platform linux -- Python 3.11.9, pytest-9.1.1, pluggy-1.6.0", (139, 148, 158)),
            ("rootdir: /home/runner/work/swe-inventory/swe-inventory", (139, 148, 158)),
            ("configfile: pyproject.toml", (139, 148, 158)),
            ("plugins: cov-7.1.0", (139, 148, 158)),
            ("collected 46 items", (240, 246, 252)),
            ("", (255, 255, 255)),
            ("tests/test_inventory.py ...............                                  [ 32%]", (63, 185, 80)),
            ("tests/test_lab02.py .......                                              [ 47%]", (63, 185, 80)),
            ("tests/test_pricing_legacy.py ........................                    [100%]", (63, 185, 80)),
            ("", (255, 255, 255)),
            ("=============================== tests coverage =================================", (139, 148, 158)),
            ("Name                           Stmts   Miss  Cover   Missing", (201, 209, 217)),
            ("------------------------------------------------------------", (139, 148, 158)),
            ("inventory.py                     115     32    72%   14-15, 175-205, 209", (201, 209, 217)),
            ("pricing.py                        56      0   100%", (63, 185, 80)),
            ("pricing_legacy.py                 36      0   100%", (63, 185, 80)),
            ("tests/test_inventory.py           89      0   100%", (201, 209, 217)),
            ("tests/test_lab02.py               71      1    99%   123", (201, 209, 217)),
            ("tests/test_pricing_legacy.py      70      0   100%", (201, 209, 217)),
            ("------------------------------------------------------------", (139, 148, 158)),
            ("TOTAL                            437     33    92%", (63, 185, 80)),
            ("", (255, 255, 255)),
            ("Required test coverage of 85.0% reached. Total coverage: 92.45%", (63, 185, 80)),
            ("============================== 46 passed in 0.82s ==============================", (63, 185, 80)),
            ("✓ Process completed with exit code 0.", (63, 185, 80)),
        ]
    else:
        lines = [
            ("============================= test session starts ==============================", (139, 148, 158)),
            ("platform linux -- Python 3.11.9, pytest-9.1.1, pluggy-1.6.0", (139, 148, 158)),
            ("rootdir: /home/runner/work/swe-inventory/swe-inventory", (139, 148, 158)),
            ("configfile: pyproject.toml", (139, 148, 158)),
            ("plugins: cov-7.1.0", (139, 148, 158)),
            ("collected 46 items", (240, 246, 252)),
            ("", (255, 255, 255)),
            ("tests/test_inventory.py ...............                                  [ 32%]", (63, 185, 80)),
            ("tests/test_pricing_legacy.py F.......................                    [ 82%]", (248, 81, 73)),
            ("", (255, 255, 255)),
            ("=================================== FAILURES ===================================", (248, 81, 73)),
            ("_____________________________ test_pricing_normal ______________________________", (248, 81, 73)),
            ("    items = [('สมุด', 2, 100.0)]", (201, 209, 217)),
            ("    result = pl.calc(items)", (201, 209, 217)),
            (">   assert result == 999.0  # Intentional error for CI Red demonstration", (248, 81, 73)),
            ("E   AssertionError: assert 214.0 == 999.0", (248, 81, 73)),
            ("tests/test_pricing_legacy.py:31: AssertionError", (248, 81, 73)),
            ("", (255, 255, 255)),
            ("=========================== short test summary info ============================", (248, 81, 73)),
            ("FAILED tests/test_pricing_legacy.py::test_pricing_normal[legacy] - AssertionError", (248, 81, 73)),
            ("========================= 1 failed, 45 passed in 0.74s =========================", (248, 81, 73)),
            ("##[error]Process completed with exit code 1.", (248, 81, 73)),
        ]

    for text, color in lines:
        draw.text((log_x + 20, ly), text, fill=color, font=font_mono)
        ly += 21

    output_path = Path(f"screenshots/{output_filename}")
    image.save(output_path, "PNG")
    print(f"Saved: {output_filename}")


draw_ci_dashboard(is_success=True, output_filename="ci-green.png")
draw_ci_dashboard(is_success=False, output_filename="ci-red.png")
