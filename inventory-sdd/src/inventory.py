"""
ระบบจัดการสินค้าคงคลังเบื้องต้น (Baseline จาก Lab 2)
"""

class Inventory:
    """คลาสจัดการสินค้าคงคลังพื้นฐาน"""

    def __init__(self) -> None:
        self.items: dict[str, dict] = {}

    def add_item(self, item_id: str, name: str, category: str, price: float, quantity: int) -> None:
        """เพิ่มสินค้าใหม่เข้าสู่ระบบ"""
        self.items[item_id] = {
            "name": name,
            "category": category,
            "price": price,
            "quantity": quantity
        }

    def update_quantity(self, item_id: str, quantity: int) -> bool:
        """อัปเดตจำนวนสินค้า"""
        if item_id in self.items:
            self.items[item_id]["quantity"] = quantity
            return True
        return False

    def get_item(self, item_id: str) -> dict | None:
        """ดึงข้อมูลสินค้าตามรหัสสินค้า"""
        return self.items.get(item_id)
