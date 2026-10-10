"""
src/service.py
Business Logic บริการจัดการสินค้าคงคลัง (InventoryService)
ยึดหลัก Single Responsibility Principle (SRP) และ Dependency Inversion Principle (DIP)
ไม่ขึ้นกับ Concrete Implementation ของ Notifier ใดๆ โดยตรง
"""

import uuid
from typing import Sequence
from .models import Product, StockTransaction, TransactionType
from .notifiers import StockObserver


class InventoryService:
    """
    คลาสจัดการ Business Logic ของระบบสินค้าคงคลัง (Subject ใน Observer Pattern)
    รับหน้าที่ตรวจสอบสต็อก บันทึกรับ/จ่าย และแจ้งเตือน Observer เมื่อสต็อกต่ำกว่าเกณฑ์
    """

    def __init__(self, observers: Sequence[StockObserver] | None = None) -> None:
        """
        กำหนดค่าเริ่มต้นของ InventoryService

        Args:
            observers: รายการ Observers ที่ต้องการรับฟังเหตุการณ์สต็อก (Dependency Injection)
        """
        self._products: dict[str, Product] = {}
        self._transactions: list[StockTransaction] = []
        self._observers: list[StockObserver] = list(observers) if observers else []

    def add_observer(self, observer: StockObserver) -> None:
        """
        ลงทะเบียน Observer ใหม่เข้าสู่ระบบ (รองรับหลายช่องทางแจ้งเตือน - OCP)

        Args:
            observer: อ็อบเจกต์ที่สอดคล้องกับ StockObserver
        """
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer: StockObserver) -> None:
        """
        ยกเลิกการลงทะเบียน Observer

        Args:
            observer: อ็อบเจกต์ที่ต้องการยกเลิก
        """
        if observer in self._observers:
            self._observers.remove(observer)

    def add_product(self, product: Product) -> None:
        """
        เพิ่มสินค้าเข้าสู่ระบบ

        Args:
            product: ข้อมูลสินค้า
        """
        self._products[product.product_id] = product

    def get_product(self, product_id: str) -> Product | None:
        """
        ค้นหาข้อมูลสินค้าตามรหัสสินค้า

        Args:
            product_id: รหัสสินค้า

        Returns:
            Product | None: ข้อมูลสินค้า หรือ None หากไม่พบ
        """
        return self._products.get(product_id)

    def set_threshold(self, product_id: str, threshold: int) -> bool:
        """
        กำหนดเกณฑ์สต็อกต่ำขั้นต่ำเฉพาะรายการสินค้า (US-04 / FR-05)

        Args:
            product_id: รหัสสินค้า
            threshold: ค่าเกณฑ์ขั้นต่ำใหม่

        Returns:
            bool: สถานะความสำเร็จ
        """
        product = self._products.get(product_id)
        if product is None or threshold < 0:
            return False
        product.threshold = threshold
        return True

    def receive(self, product_id: str, quantity: int) -> bool:
        """
        บันทึกรับสินค้าเข้าคลัง (US-01 / FR-01)

        Args:
            product_id: รหัสสินค้า
            quantity: จำนวนที่รับเข้า (ต้องมากกว่า 0)

        Returns:
            bool: สถานะความสำเร็จ
        """
        if quantity <= 0:
            return False

        product = self._products.get(product_id)
        if product is None:
            return False

        product.quantity += quantity
        self._record_transaction(product_id, TransactionType.RECEIVE, quantity, product.quantity)
        return True

    def issue(self, product_id: str, quantity: int) -> bool:
        """
        บันทึกจ่ายสินค้าออกจากคลัง และแจ้งเตือนหากสต็อกต่ำกว่า threshold (US-01, US-02 / FR-01, FR-02, FR-03)

        Args:
            product_id: รหัสสินค้า
            quantity: จำนวนที่จ่ายออก (ต้องมากกว่า 0 และไม่เกินจำนวนคงเหลือ)

        Returns:
            bool: True หากจ่ายสำเร็จ, False หากไม่พบสินค้าหรือสต็อกไม่เพียงพอ
        """
        if quantity <= 0:
            return False

        product = self._products.get(product_id)
        if product is None:
            return False

        if product.quantity < quantity:
            return False

        product.quantity -= quantity
        self._record_transaction(product_id, TransactionType.ISSUE, quantity, product.quantity)

        # ตรวจสอบเงื่อนไขสต็อกต่ำ (< threshold) ตาม Acceptance Criteria
        if product.is_low_stock():
            self._notify_low_stock(product)

        return True

    def stock_value_report(self) -> dict[str, float]:
        """
        คำนวณและสรุปมูลค่ารวมของสินค้าในสต็อกแยกตามหมวดหมู่ (US-03 / FR-04)

        Returns:
            dict[str, float]: ดิกชันนารีแสดงหมวดหมู่และมูลค่ารวม เช่น {"Electrical": 2000.0}
        """
        report: dict[str, float] = {}
        for product in self._products.values():
            category = product.category
            report[category] = report.get(category, 0.0) + product.calculate_total_value()
        return report

    def get_total_inventory_value(self) -> float:
        """
        คำนวณมูลค่ารวมของสินค้าทั้งหมดในระบบ

        Returns:
            float: ยอดรวมมูลค่าสินค้าคงคลังทั้งหมด
        """
        return sum(self.stock_value_report().values())

    def get_transactions(self) -> list[StockTransaction]:
        """
        ดึงประวัติการทำธุรกรรมทั้งหมด

        Returns:
            list[StockTransaction]: รายการธุรกรรมสต็อก
        """
        return list(self._transactions)

    def _record_transaction(
        self, product_id: str, txn_type: TransactionType, quantity: int, balance_after: int
    ) -> None:
        """บันทึกประวัติการทำธุรกรรมลงหน่วยความจำ"""
        txn = StockTransaction(
            transaction_id=str(uuid.uuid4())[:8],
            product_id=product_id,
            transaction_type=txn_type,
            quantity=quantity,
            balance_after=balance_after,
        )
        self._transactions.append(txn)

    def _notify_low_stock(self, product: Product) -> None:
        """
        แจ้งเตือนไปยังผู้สังเกตการณ์ (Observers) ทั้งหมด
        พร้อมระบบรองรับ Reliability (NFR-03): ข้อผิดพลาดใน Observer หนึ่งจะไม่ขัดขวางตัวอื่น
        """
        for observer in self._observers:
            try:
                observer.on_low_stock(product)
            except Exception as exc:  # noqa: BLE001
                try:
                    print(f"[Warning] เกิดข้อผิดพลาดในการแจ้งเตือน: {exc}")
                except UnicodeEncodeError:
                    pass
