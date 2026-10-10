"""
ระบบจัดการสต็อกสินค้า ร้านเครื่องเขียน 'ร้านเขียนดี' (Lab 02)
รองรับการดูรายการสินค้า (US-01), เพิ่มสินค้าใหม่ (US-02), และปรับปรุงยอดสต็อก (US-03)
"""

import json
import os
import sys
from pathlib import Path

# ปรับปรุงการแสดงผลภาษาไทยบน Windows Console
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


DEFAULT_DATA_PATH = Path("data/inventory.json")


class Inventory:
    """คลาสจัดการสินค้าคงคลังร้านเขียนดี จัดเก็บข้อมูลในรูปแบบไฟล์ JSON"""

    def __init__(self, data_path: Path | str = DEFAULT_DATA_PATH) -> None:
        self.data_path = Path(data_path)
        self.items: list[dict] = []
        self.load_data()

    def load_data(self) -> list[dict]:
        """อ่านข้อมูลสินค้าจากไฟล์ JSON"""
        if not self.data_path.exists():
            self.items = []
            return self.items

        try:
            with open(self.data_path, "r", encoding="utf-8") as f:
                self.items = json.load(f)
        except (json.JSONDecodeError, OSError):
            self.items = []
        return self.items

    def save_data(self) -> None:
        """บันทึกข้อมูลสินค้าลงไฟล์ JSON"""
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(self.items, f, ensure_ascii=False, indent=2)

    def list_items(self) -> list[dict]:
        """
        US-01: ดูรายการสินค้าทั้งหมดพร้อมจำนวนคงเหลือ
        AC-1: มีสินค้าอย่างน้อย 1 รายการ -> แสดงชื่อ รหัส และจำนวนคงเหลือครบทุกรายการ
        AC-2: ยังไม่มีสินค้าในระบบ -> คืนค่าลิสต์ว่าง
        """
        return list(self.items)

    def format_list_display(self) -> str:
        """จัดรูปแบบการแสดงผลรายการสินค้าสำหรับ CLI Interface"""
        items = self.list_items()
        if not items:
            return "ยังไม่มีสินค้าในระบบ"

        lines = [
            "=" * 60,
            f"{'รหัสสินค้า':<12} {'ชื่อสินค้า':<32} {'คงเหลือ':>10}",
            "-" * 60,
        ]
        for item in items:
            code = item.get("code", "-")
            name = item.get("name", "-")
            qty = item.get("quantity", 0)
            lines.append(f"{code:<12} {name:<32} {qty:>10}")
        lines.append("=" * 60)
        return "\n".join(lines)


def main() -> None:
    inv = Inventory()
    if len(sys.argv) > 1 and sys.argv[1] == "list":
        print(inv.format_list_display())
    else:
        print("คำสั่งที่รองรับ: python inventory.py list")


if __name__ == "__main__":
    main()
