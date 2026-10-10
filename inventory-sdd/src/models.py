"""
src/models.py
โมเดลข้อมูลสำหรับระบบจัดการสต็อกสินค้า (Inventory Domain Models)
รองรับหลักการ Single Responsibility Principle (SRP) และ Type Hints ครบถ้วน
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class TransactionType(Enum):
    """ประเภทรายการธุรกรรมสต็อกสินค้า"""
    RECEIVE = "RECEIVE"
    ISSUE = "ISSUE"


@dataclass
class Product:
    """
    ข้อมูลสินค้าในระบบจัดการสินค้าคงคลัง
    """
    product_id: str
    name: str
    category: str
    price: float
    quantity: int
    threshold: int = 10

    def is_low_stock(self) -> bool:
        """
        ตรวจสอบว่าสินค้ามีสต็อกต่ำกว่าเกณฑ์ขั้นต่ำหรือไม่
        ตาม Acceptance Criteria: แจ้งเตือนเมื่อคงเหลือน้อยกว่า (<) threshold เท่านั้น
        """
        return self.quantity < self.threshold

    def calculate_total_value(self) -> float:
        """คำนวณมูลค่ารวมของสินค้าชิ้นนี้ในสต็อก"""
        return self.price * self.quantity


@dataclass
class StockTransaction:
    """
    บันทึกประวัติธุรกรรมการรับ/จ่ายสินค้า
    """
    transaction_id: str
    product_id: str
    transaction_type: TransactionType
    quantity: int
    balance_after: int
    timestamp: datetime = field(default_factory=datetime.now)
