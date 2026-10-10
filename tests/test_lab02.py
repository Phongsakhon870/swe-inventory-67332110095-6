"""
ชุดทดสอบสำหรับ Lab 02: ระบบสต็อกร้านเขียนดี
"""

import json
import tempfile
import unittest
from pathlib import Path
from inventory import Inventory


class TestLab02Inventory(unittest.TestCase):
    """ทดสอบ Acceptance Criteria ของ Lab 02"""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_file = Path(self.temp_dir.name) / "test_inventory.json"

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    # -------------------------------------------------------------
    # US-01: ดูรายการสินค้าทั้งหมดพร้อมจำนวนคงเหลือ
    # -------------------------------------------------------------
    def test_us01_ac1_list_with_items(self) -> None:
        """AC-1: Given มีสินค้าอย่างน้อย 1 รายการ -> แสดงชื่อ รหัส และจำนวนคงเหลือครบทุกรายการ"""
        initial_data = [
            {"code": "P01", "name": "สมุดบันทึก", "quantity": 10, "price": 20.0},
            {"code": "P02", "name": "ปากกาน้ำเงิน", "quantity": 50, "price": 10.0},
        ]
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(initial_data, f)

        inv = Inventory(self.data_file)
        items = inv.list_items()
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["code"], "P01")
        self.assertEqual(items[1]["quantity"], 50)
        display = inv.format_list_display()
        self.assertIn("P01", display)
        self.assertIn("ปากกาน้ำเงิน", display)

    def test_us01_ac2_list_empty_system(self) -> None:
        """AC-2: Given ยังไม่มีสินค้าในระบบ -> แสดงข้อความ 'ยังไม่มีสินค้าในระบบ'"""
        inv = Inventory(self.data_file)
        items = inv.list_items()
        self.assertEqual(len(items), 0)
        display = inv.format_list_display()
        self.assertEqual(display, "ยังไม่มีสินค้าในระบบ")


if __name__ == "__main__":
    unittest.main()
