"""
src/notifiers.py
โมดูลการแจ้งเตือนและการจัดการ Observer / Factory Pattern
ออกแบบตามหลัก SOLID (SRP, OCP, LSP, ISP, DIP)
"""

from typing import Protocol, runtime_checkable
from .models import Product


@runtime_checkable
class Notifier(Protocol):
    """
    Protocol สำหรับการส่งข้อความแจ้งเตือน (Notifier Abstraction)
    """

    def send(self, recipient: str, message: str) -> bool:
        """
        ส่งข้อความแจ้งเตือนไปยังผู้รับ

        Args:
            recipient: ข้อมูลผู้รับ (เช่น ที่อยู่อีเมล หรือ เบอร์โทรศัพท์)
            message: เนื้อหาข้อความที่ต้องการแจ้งเตือน

        Returns:
            bool: สถานะการส่งสำเร็จหรือไม่
        """
        ...


@runtime_checkable
class StockObserver(Protocol):
    """
    Observer Protocol สำหรับการรับฟังเหตุการณ์การเปลี่ยนแปลงของสต็อกสินค้า
    """

    def on_low_stock(self, product: Product) -> None:
        """
        ทำงานเมื่อสินค้ามีสต็อกคงเหลือต่ำกว่าเกณฑ์ขั้นต่ำ (Threshold)

        Args:
            product: อ็อบเจกต์สินค้าที่มีสต็อกต่ำ
        """
        ...


class EmailNotifier:
    """
    ผู้ให้บริการแจ้งเตือนผ่านช่องทาง Email (จำลองผลลัพธ์ผ่าน Console)
    """

    def __init__(self, recipient: str) -> None:
        """
        กำหนดค่าเริ่มต้นของ EmailNotifier

        Args:
            recipient: ที่อยู่อีเมลของผู้รับปลายทาง
        """
        self.recipient = recipient

    def send(self, recipient: str, message: str) -> bool:
        """
        ส่งข้อความทาง Email (จำลองด้วย print ตามกฎข้อห้ามของโปรเจกต์)
        """
        text = f"[Email] ถึง {recipient}: {message}"
        try:
            print(text)
        except UnicodeEncodeError:
            print(text.encode("utf-8", errors="replace").decode("utf-8", errors="replace"))
        return True

    def on_low_stock(self, product: Product) -> None:
        """
        รับการแจ้งเตือนเหตุการณ์สต็อกต่ำ และส่งข้อความทาง Email
        """
        message = (
            f"แจ้งเตือนสต็อกต่ำ! สินค้า '{product.name}' (ID: {product.product_id}) "
            f"คงเหลือ {product.quantity} ชิ้น (ต่ำกว่าเกณฑ์ {product.threshold} ชิ้น)"
        )
        self.send(self.recipient, message)


class SMSNotifier:
    """
    ผู้ให้บริการแจ้งเตือนผ่านช่องทาง SMS (จำลองผลลัพธ์ผ่าน Console)
    """

    def __init__(self, recipient: str) -> None:
        """
        กำหนดค่าเริ่มต้นของ SMSNotifier

        Args:
            recipient: หมายเลขโทรศัพท์ของผู้รับปลายทาง
        """
        self.recipient = recipient

    def send(self, recipient: str, message: str) -> bool:
        """
        ส่งข้อความทาง SMS (จำลองด้วย print ตามกฎข้อห้ามของโปรเจกต์)
        """
        text = f"[SMS] ถึง {recipient}: {message}"
        try:
            print(text)
        except UnicodeEncodeError:
            print(text.encode("utf-8", errors="replace").decode("utf-8", errors="replace"))
        return True

    def on_low_stock(self, product: Product) -> None:
        """
        รับการแจ้งเตือนเหตุการณ์สต็อกต่ำ และส่งข้อความทาง SMS
        """
        message = (
            f"แจ้งเตือนสต็อกต่ำ! สินค้า '{product.name}' (ID: {product.product_id}) "
            f"คงเหลือ {product.quantity} ชิ้น (ต่ำกว่าเกณฑ์ {product.threshold} ชิ้น)"
        )
        self.send(self.recipient, message)


class NotifierFactory:
    """
    Factory Class สำหรับสร้าง Notifier ตามช่องทางที่ต้องการ (Factory Pattern)
    ช่วยให้เพิ่มช่องทางการแจ้งเตือนใหม่ได้ง่ายโดยไม่กระทบ Business Logic (OCP)
    """

    @staticmethod
    def create(channel: str, recipient: str) -> Notifier:
        """
        สร้าง Notifier ตาม channel ที่ระบุ

        Args:
            channel: ช่องทางการแจ้งเตือน เช่น 'email', 'sms'
            recipient: ผู้รับปลายทาง

        Returns:
            Notifier: อ็อบเจกต์ที่สอดคล้องกับ Notifier protocol

        Raises:
            ValueError: เมื่อระบุช่องทางที่ไม่รองรับ
        """
        normalized_channel = channel.strip().lower()
        if normalized_channel == "email":
            return EmailNotifier(recipient=recipient)
        elif normalized_channel == "sms":
            return SMSNotifier(recipient=recipient)
        else:
            raise ValueError(f"ไม่รองรับช่องทางการแจ้งเตือน: '{channel}'")
