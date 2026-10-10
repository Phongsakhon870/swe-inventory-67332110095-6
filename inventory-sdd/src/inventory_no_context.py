"""
src/inventory_no_context.py
โค้ดที่สร้างโดย AI ในขั้นที่ 4 (ก่อนมีไฟล์กฎโปรเจกต์ .ai-rules.md)
แสดงตัวอย่างโค้ดที่มีปัญหาด้านการออกแบบ ละเมิดหลัก SOLID และ hardcode ค่าคงที่
"""

import smtplib  # noqa: F401 (ละเมิดกฎข้อห้าม: นำเข้าไลบรารีส่งเมลจริงและไม่ได้ใช้งาน)


class InventoryManager:
    """
    คลาสรวมศูนย์ (Monolithic Class) ที่ทำหน้าที่ทุกอย่างในไฟล์เดียว
    ละเมิดหลัก SRP โดยรวมทั้งการคำนวณสต็อก การจัดเก็บข้อมูล และการส่งแจ้งเตือน
    """

    def __init__(self):
        # ปัญหา: ขาด Type hints, ใช้ dictionary ธรรมดา และ hardcode ข้อมูลการติดต่อ
        self.products = {}
        self.default_threshold = 10
        self.manager_email = "manager@engineering-shop.com"
        self.manager_phone = "081-234-5678"

    def add_product(self, product_id, name, category, price, quantity, threshold=None):
        self.products[product_id] = {
            "name": name,
            "category": category,
            "price": price,
            "quantity": quantity,
            "threshold": threshold if threshold is not None else self.default_threshold,
        }

    def receive_stock(self, product_id, amount):
        if product_id in self.products:
            self.products[product_id]["quantity"] += amount
            return True
        return False

    def issue_stock(self, product_id, amount, channel="email"):
        """
        ตัดสต็อกและส่งข้อความแจ้งเตือนใน method เดียวกัน
        ปัญหา:
        1. ละเมิด SRP: คำนวณสต็อก + ตัดสินใจเลือกช่องทาง + I/O print ปนกัน
        2. ละเมิด OCP: มีเงื่อนไข if/elif ตาม channel หากเพิ่ม Line ต้องมาแก้โค้ดที่นี่
        3. ละเมิด DIP: ผูกติดกับการพิมพ์และช่องทาง email/sms โดยตรง
        4. Bug: ใช้ <= แทนที่จะเป็น < ตามที่ spec กำหนด
        """
        if product_id not in self.products:
            print("ไม่พบสินค้าในระบบ")
            return False

        item = self.products[product_id]
        if item["quantity"] < amount:
            print("สินค้าในสต็อกไม่เพียงพอ")
            return False

        item["quantity"] -= amount

        # ปัญหา Edge Case: ใช้ <= ทำให้กรณีที่สต็อกเหลือเท่ากับ threshold พอดีก็แจ้งเตือน (ขัดกับ spec)
        if item["quantity"] <= item["threshold"]:
            message = (
                f"แจ้งเตือนสต็อกต่ำ: สินค้า {item['name']} (ID: {product_id}) "
                f"คงเหลือ {item['quantity']} ต่ำกว่าหรือเท่ากับเกณฑ์ {item['threshold']}"
            )
            # ปัญหา: Hardcode ช่องทางการแจ้งเตือน
            if channel == "email":
                print(f"[Email ส่งถึง {self.manager_email}] {message}")
            elif channel == "sms":
                print(f"[SMS ส่งถึง {self.manager_phone}] {message}")
            else:
                print(f"[Alert] {message}")

        return True

    def get_stock_value_report(self):
        """คำนวณมูลค่าสต็อกรวมแยกตามหมวดหมู่"""
        report = {}
        for _, item in self.products.items():
            cat = item["category"]
            val = item["price"] * item["quantity"]
            report[cat] = report.get(cat, 0.0) + val
        return report
