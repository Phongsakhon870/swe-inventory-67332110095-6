"""
ระบบจัดการสต็อกสินค้า ร้านเครื่องเขียน 'ร้านเขียนดี' (Lab 02)
รองรับการดูรายการสินค้า (US-01), เพิ่มสินค้าใหม่ (US-02), และปรับปรุงยอดสต็อก (US-03)
"""

import json
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
            with open(self.data_path, encoding="utf-8") as f:
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

    def add_item(self, code: str, name: str, quantity: int = 0, price: float = 0.0) -> dict:
        """
        US-02: เพิ่มสินค้าใหม่เข้าระบบ
        AC-1: ยังไม่มีสินค้ารหัสนี้ -> บันทึกสินค้าใหม่ และแสดงเมื่อเรียก list
        AC-2: มีสินค้ารหัสนี้อยู่แล้ว -> ปฏิเสธและแจ้ง 'รหัสสินค้าซ้ำ' โดยไม่เขียนทับ
        """
        clean_code = code.strip().upper()
        clean_name = name.strip()

        if not clean_code or not clean_name:
            raise ValueError("รหัสสินค้าและชื่อสินค้าต้องไม่ว่างเปล่า")

        if quantity < 0:
            raise ValueError("จำนวนสินค้าเริ่มต้นต้องไม่ติดลบ")

        for item in self.items:
            if item.get("code", "").upper() == clean_code:
                raise ValueError("รหัสสินค้าซ้ำ")

        new_item = {
            "code": clean_code,
            "name": clean_name,
            "quantity": quantity,
            "price": max(0.0, float(price)),
        }
        self.items.append(new_item)
        self.save_data()
        return new_item

    def update_quantity(self, code: str, change_amount: int) -> dict:
        """
        US-03: แก้ไขจำนวนสินค้าเมื่อรับหรือจ่ายของ
        AC-1: รับเข้าหรือจ่ายออกจำนวนที่ไม่ทำให้ติดลบ -> อัปเดตยอดคงเหลือและบันทึกทันที
        AC-2: จ่ายออกมากกว่าจำนวนคงเหลือ -> ปฏิเสธและแสดง 'จำนวนคงเหลือไม่พอ' ยอดคงเหลือไม่เปลี่ยน
        """
        clean_code = code.strip().upper()
        target_item = None
        for item in self.items:
            if item.get("code", "").upper() == clean_code:
                target_item = item
                break

        if target_item is None:
            raise KeyError(f"ไม่พบสินค้า '{code}' ในระบบ")

        current_qty = target_item.get("quantity", 0)
        new_qty = current_qty + change_amount

        if new_qty < 0:
            raise ValueError("จำนวนคงเหลือไม่พอ")

        target_item["quantity"] = new_qty
        self.save_data()
        return target_item

    def low_stock_items(self, threshold: int) -> list[dict]:
        """
        ค้นหารายชื่อสินค้าที่มีจำนวนคงเหลือ น้อยกว่าหรือเท่ากับ threshold

        Args:
            threshold: ระดับจำนวนสินค้าขั้นต่ำที่ต้องการตรวจสอบ

        Returns:
            รายการสินค้าที่คงเหลือน้อยกว่าหรือเท่ากับ threshold เรียงตามชื่อ (A-Z / ก-ฮ)
        """
        if threshold < 0:
            return []

        qualifying_items = [
            item for item in self.items
            if item.get("quantity", 0) <= threshold
        ]
        return sorted(qualifying_items, key=lambda item: item.get("name", ""))

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
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "list":
            print(inv.format_list_display())
        elif cmd == "add" and len(sys.argv) >= 4:
            code = sys.argv[2]
            name = sys.argv[3]
            qty = int(sys.argv[4]) if len(sys.argv) > 4 else 0
            price = float(sys.argv[5]) if len(sys.argv) > 5 else 0.0
            try:
                inv.add_item(code, name, qty, price)
                print(f"บันทึกสินค้าใหม่ '{name}' ({code}) สำเร็จ")
            except ValueError as e:
                print(f"เกิดข้อผิดพลาด: {e}")
        elif cmd == "update" and len(sys.argv) >= 4:
            code = sys.argv[2]
            amount = int(sys.argv[3])
            try:
                item = inv.update_quantity(code, amount)
                action = "รับเข้า" if amount > 0 else "จ่ายออก"
                print(f"{action}สินค้า '{item['name']}' สำเร็จ คงเหลือ {item['quantity']} ชิ้น")
            except (KeyError, ValueError) as e:
                print(f"เกิดข้อผิดพลาด: {e}")
        else:
            print("คำสั่งที่รองรับ:")
            print("  python inventory.py list")
            print("  python inventory.py add <รหัส> <ชื่อ> <จำนวน> [ราคา]")
            print("  python inventory.py update <รหัส> <จำนวนรับเข้าหรือจ่ายออก>")
    else:
        print("คำสั่งที่รองรับ: python inventory.py list, add หรือ update")


if __name__ == "__main__":
    main()
