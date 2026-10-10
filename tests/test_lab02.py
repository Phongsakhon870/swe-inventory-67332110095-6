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

    # -------------------------------------------------------------
    # US-02: เพิ่มสินค้าใหม่เข้าระบบ
    # -------------------------------------------------------------
    def test_us02_ac1_add_new_item_success(self) -> None:
        """AC-1: Given ยังไม่มีสินค้ารหัสนี้ -> บันทึกสินค้าใหม่ และแสดงเมื่อเรียก list"""
        inv = Inventory(self.data_file)
        item = inv.add_item("P99", "ยางลบ 4B", 20, 15.0)
        self.assertEqual(item["code"], "P99")
        self.assertEqual(item["name"], "ยางลบ 4B")
        self.assertEqual(item["quantity"], 20)

        # ตรวจสอบว่าแสดงใน list
        items = inv.list_items()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["code"], "P99")

    def test_us02_ac2_add_duplicate_code_rejected(self) -> None:
        """AC-2: Given มีสินค้ารหัสนี้อยู่แล้ว -> ปฏิเสธและแสดง 'รหัสสินค้าซ้ำ' โดยไม่เขียนทับ"""
        inv = Inventory(self.data_file)
        inv.add_item("P01", "สมุดโน้ต", 10, 25.0)

        with self.assertRaises(ValueError) as ctx:
            inv.add_item("P01", "สมุดโน้ตปกแข็ง", 5, 50.0)

        self.assertIn("รหัสสินค้าซ้ำ", str(ctx.exception))
        # ตรวจสอบว่าข้อมูลเดิมไม่ถูกเขียนทับ
        items = inv.list_items()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["name"], "สมุดโน้ต")
        self.assertEqual(items[0]["quantity"], 10)

    # -------------------------------------------------------------
    # US-03: แก้ไขจำนวนสินค้าเมื่อรับหรือจ่ายของ
    # -------------------------------------------------------------
    def test_us03_ac1_update_quantity_success(self) -> None:
        """AC-1: Given รับเข้าหรือจ่ายออกที่ไม่ติดลบ -> อัปเดตยอดคงเหลือและบันทึกทันที"""
        inv = Inventory(self.data_file)
        inv.add_item("P01", "ดินสอกด", 10, 35.0)

        # รับเข้า +5
        updated = inv.update_quantity("P01", 5)
        self.assertEqual(updated["quantity"], 15)

        # จ่ายออก -3
        updated = inv.update_quantity("P01", -3)
        self.assertEqual(updated["quantity"], 12)

        # ตรวจสอบการบันทึกในไฟล์
        inv2 = Inventory(self.data_file)
        self.assertEqual(inv2.list_items()[0]["quantity"], 12)

    def test_us03_ac2_excessive_deduction_rejected(self) -> None:
        """AC-2: Given จ่ายออกมากกว่าคงเหลือ -> ปฏิเสธ 'จำนวนคงเหลือไม่พอ' ยอดคงเหลือไม่เปลี่ยน"""
        inv = Inventory(self.data_file)
        inv.add_item("P02", "ไม้บรรทัด", 5, 12.0)

        with self.assertRaises(ValueError) as ctx:
            inv.update_quantity("P02", -10)

        self.assertIn("จำนวนคงเหลือไม่พอ", str(ctx.exception))
        self.assertEqual(inv.list_items()[0]["quantity"], 5)

    def test_us03_item_not_found(self) -> None:
        """ทดสอบกรณีรหัสสินค้าไม่มีอยู่ในระบบ"""
        inv = Inventory(self.data_file)
        with self.assertRaises(KeyError) as ctx:
            inv.update_quantity("NONE", 5)
        self.assertIn("ไม่พบสินค้า", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()

