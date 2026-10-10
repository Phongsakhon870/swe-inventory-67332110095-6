"""
ชุดแบบทดสอบอัตโนมัติ (Automated Unit Tests)
สำหรับทดสอบความถูกต้องของระบบตาม Acceptance Criteria ใน specs/spec.md
"""

import time
import unittest
from src.models import Product, TransactionType
from src.notifiers import EmailNotifier, NotifierFactory, SMSNotifier, StockObserver
from src.service import InventoryService


class MockObserver:
    """Mock Observer สำหรับดักจับการแจ้งเตือนในการทดสอบ"""

    def __init__(self) -> None:
        self.notified_products: list[Product] = []

    def on_low_stock(self, product: Product) -> None:
        self.notified_products.append(product)


class TestInventorySystem(unittest.TestCase):
    """ทดสอบการทำงานของระบบจัดการสต็อกสินค้าตามข้อกำหนดใน Spec"""

    def setUp(self) -> None:
        self.mock_observer = MockObserver()
        self.service = InventoryService(observers=[self.mock_observer])

    # ---------------------------------------------------------
    # US-01: บันทึกรับ/จ่ายสินค้า
    # ---------------------------------------------------------
    def test_us01_receive_stock_success(self) -> None:
        """Scenario: บันทึกรับสินค้าเข้าคลัง"""
        product = Product(
            product_id="WIRE-01",
            name="สายไฟ 2.5 sq.mm",
            category="Electrical",
            price=15.0,
            quantity=10,
            threshold=15,
        )
        self.service.add_product(product)

        success = self.service.receive("WIRE-01", 15)
        self.assertTrue(success)
        self.assertEqual(product.quantity, 25)

        txns = self.service.get_transactions()
        self.assertEqual(len(txns), 1)
        self.assertEqual(txns[0].transaction_type, TransactionType.RECEIVE)
        self.assertEqual(txns[0].quantity, 15)
        self.assertEqual(txns[0].balance_after, 25)

    def test_us01_issue_stock_insufficient(self) -> None:
        """Scenario: จ่ายสินค้าเมื่อสต็อกไม่เพียงพอ"""
        product = Product(
            product_id="BRK-30A",
            name="เบรกเกอร์ 30A",
            category="Electrical",
            price=120.0,
            quantity=5,
            threshold=5,
        )
        self.service.add_product(product)

        success = self.service.issue("BRK-30A", 10)
        self.assertFalse(success)
        self.assertEqual(product.quantity, 5)
        self.assertEqual(len(self.service.get_transactions()), 0)

    # ---------------------------------------------------------
    # US-02: แจ้งเตือนสต็อกต่ำ
    # ---------------------------------------------------------
    def test_us02_issue_stock_below_threshold_triggers_alert(self) -> None:
        """Scenario: จ่ายสินค้าจนสต็อกต่ำกว่า threshold"""
        product = Product(
            product_id="WIRE-01",
            name="สายไฟ 2.5 sq.mm",
            category="Electrical",
            price=15.0,
            quantity=20,
            threshold=15,
        )
        self.service.add_product(product)

        success = self.service.issue("WIRE-01", 8)
        self.assertTrue(success)
        self.assertEqual(product.quantity, 12)
        self.assertEqual(len(self.mock_observer.notified_products), 1)
        self.assertEqual(self.mock_observer.notified_products[0].product_id, "WIRE-01")

    def test_us02_issue_stock_above_threshold_no_alert(self) -> None:
        """Scenario: จ่ายสินค้าโดยสต็อกยังสูงกว่า threshold"""
        product = Product(
            product_id="WIRE-01",
            name="สายไฟ 2.5 sq.mm",
            category="Electrical",
            price=15.0,
            quantity=50,
            threshold=15,
        )
        self.service.add_product(product)

        success = self.service.issue("WIRE-01", 10)
        self.assertTrue(success)
        self.assertEqual(product.quantity, 40)
        self.assertEqual(len(self.mock_observer.notified_products), 0)

    def test_us02_issue_stock_exactly_at_threshold_no_alert(self) -> None:
        """Scenario: จ่ายสินค้าจนสต็อกเท่ากับ threshold พอดี (Edge Case)"""
        product = Product(
            product_id="WIRE-01",
            name="สายไฟ 2.5 sq.mm",
            category="Electrical",
            price=15.0,
            quantity=20,
            threshold=15,
        )
        self.service.add_product(product)

        success = self.service.issue("WIRE-01", 5)
        self.assertTrue(success)
        self.assertEqual(product.quantity, 15)
        # ต้องไม่แจ้งเตือน เพราะแจ้งเตือนเฉพาะเมื่อต่ำกว่า (< threshold) เท่านั้น
        self.assertEqual(len(self.mock_observer.notified_products), 0)

    # ---------------------------------------------------------
    # US-03: รายงานมูลค่าสต็อกแยกหมวดหมู่
    # ---------------------------------------------------------
    def test_us03_stock_value_report(self) -> None:
        """Scenario: คำนวณมูลค่ารวมแยกตามหมวดหมู่"""
        p1 = Product("P1", "สินค้า A", "Electrical", 100.0, 10)
        p2 = Product("P2", "สินค้า B", "Electrical", 200.0, 5)
        p3 = Product("P3", "สินค้า C", "Tools", 500.0, 2)
        p4 = Product("P4", "สินค้า D", "Safety", 50.0, 0)

        self.service.add_product(p1)
        self.service.add_product(p2)
        self.service.add_product(p3)
        self.service.add_product(p4)

        report = self.service.stock_value_report()
        self.assertAlmostEqual(report["Electrical"], 2000.0)
        self.assertAlmostEqual(report["Tools"], 1000.0)
        self.assertAlmostEqual(report["Safety"], 0.0)
        self.assertAlmostEqual(self.service.get_total_inventory_value(), 3000.0)

    # ---------------------------------------------------------
    # US-04: ตั้งค่า threshold รายสินค้า
    # ---------------------------------------------------------
    def test_us04_custom_threshold_update(self) -> None:
        """Scenario: ปรับเปลี่ยน threshold เฉพาะรายการสินค้า"""
        product = Product("PIPE-01", "ท่อร้อยสายไฟ", "Electrical", 80.0, 25, threshold=10)
        self.service.add_product(product)

        self.service.set_threshold("PIPE-01", 25)
        self.assertEqual(product.threshold, 25)

        # จ่ายออก 5 ชิ้น เหลือ 20 ซึ่งต่ำกว่า threshold ใหม่ (25)
        self.service.issue("PIPE-01", 5)
        self.assertEqual(product.quantity, 20)
        self.assertEqual(len(self.mock_observer.notified_products), 1)

    # ---------------------------------------------------------
    # US-05: แจ้งเตือนหลายช่องทางพร้อมกัน & Factory Pattern
    # ---------------------------------------------------------
    def test_us05_multi_channel_notification_and_factory(self) -> None:
        """Scenario: ส่งการแจ้งเตือนผ่านหลายช่องทางพร้อมกันผ่าน Factory"""
        email_notifier = NotifierFactory.create("email", "manager@shop.com")
        sms_notifier = NotifierFactory.create("sms", "0812345678")

        self.assertIsInstance(email_notifier, EmailNotifier)
        self.assertIsInstance(sms_notifier, SMSNotifier)

        service = InventoryService(observers=[email_notifier, sms_notifier])  # type: ignore[list-item]
        product = Product("P-MULTI", "สายแลน CAT6", "Network", 20.0, 10, threshold=8)
        service.add_product(product)

        # จ่ายออก 5 ชิ้น เหลือ 5 ชิ้น (< 8) ต้องส่งผ่านทั้ง email และ sms
        success = service.issue("P-MULTI", 5)
        self.assertTrue(success)

    # ---------------------------------------------------------
    # NFR-01: Performance Testing
    # ---------------------------------------------------------
    def test_nfr01_performance_large_catalog(self) -> None:
        """ทดสอบ Performance: คำนวณมูลค่าสินค้า 1,000 รายการภายใน 1 วินาที"""
        for i in range(1000):
            p = Product(f"PROD-{i}", f"Product {i}", f"Cat-{i % 10}", 50.0, 10)
            self.service.add_product(p)

        start_time = time.time()
        report = self.service.stock_value_report()
        elapsed_time = time.time() - start_time

        self.assertEqual(len(report), 10)
        self.assertLess(elapsed_time, 1.0, "การคำนวณรายงาน 1,000 รายการต้องเร็วกว่า 1 วินาที")


if __name__ == "__main__":
    unittest.main()
