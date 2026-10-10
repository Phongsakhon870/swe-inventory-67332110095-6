# รายงานการเปรียบเทียบ Prompt Engineering กับ Context Engineering (Lab 04)

เอกสารบันทึกการทดลองส่งคำสั่งให้ AI coding assistant ทำงานเดียวกันใน 2 รูปแบบ เพื่อศึกษาความแตกต่างระหว่างการสั่งงานแบบ **Prompt ทั่วไป (ไม่มี Context)** กับการสั่งงานแบบ **Context Engineering (เตรียมบริบทครบถ้วน)**

---

## 1. การทดลองรอบที่ 1: สั่งงานด้วย Prompt สั้น ๆ (ขาด Context)

### คำสั่ง (Prompt):
```text
เขียนฟังก์ชันสำหรับขายสินค้าหลายรายการพร้อมกัน (sell_many) ให้กับระบบจัดการคลังสินค้า Inventory ในภาษา Python
```

### ผลลัพธ์โค้ดที่ AI สร้างขึ้น (Round 1 Output):
```python
class Inventory:
    def __init__(self):
        self.stock = {}

    def sell_many(self, items):
        # AI คาดเดาโครงสร้างเอง ใช้ชื่อฟิลด์ stock แทน _items
        results = {}
        for item_name, qty in items.items():
            if item_name not in self.stock:
                raise Exception(f"Item {item_name} not found")
            if self.stock[item_name] < qty:
                raise Exception("Not enough stock")
            self.stock[item_name] -= qty
            results[item_name] = self.stock[item_name]
        return results
```

### ข้อบกพร่องและจุดที่มีปัญหาของผลลัพธ์รอบที่ 1:
1. **ไม่เข้ากับโค้ดเดิม (Interface Mismatch):** AI คาดเดาชื่อตัวแปรเป็น `self.stock` แทนที่จะเป็น `self._items` ของคลาส `Inventory` เดิม และไม่ใช้งานคลาส `InventoryItem`
2. **ละเมิดหลักการ Atomicity (ไม่มี Transaction / Rollback):** หากรายการแรกตัดสต็อกสำเร็จ แต่รายการที่สองสต็อกไม่พอ โค้ดจะโยน `Exception` ออกมาทันที ส่งผลให้รายการแรกถูกหักสต็อกไปแล้วและไม่มียอดคืน คลังสินค้าเสียหายและข้อมูลไม่สอดคล้องกัน (Partial State Mutation)
3. **ใช้ Generic Exception:** โยน `raise Exception(...)` แทนที่จะใช้ `KeyError` หรือ `ValueError` ตามมาตรฐานของระบบเดิม
4. **ขาด Type Hints และ Docstring:** ไม่มี Type Annotations ที่รัดกุม

---

## 2. การทดลองรอบที่ 2: สั่งงานแบบมี Context ครบถ้วน (Context Engineering)

### คำสั่งและบริบทที่แนบไป (Prompt with Full Context):
````text
ปรับปรุงเมธอด sell() ของคลาส Inventory ด้านล่างให้รองรับการขายหลายรายการพร้อมกันในคลาสเดิม

[บริบทโค้ดเดิม inventory.py]
class InventoryItem:
    def __init__(self, name: str, quantity: int, price: float):
        if not name or not name.strip():
            raise ValueError("ชื่อสินค้าต้องไม่ว่างเปล่า")
        if quantity < 0:
            raise ValueError("จำนวนสินค้าต้องไม่ติดลบ")
        if price <= 0:
            raise ValueError("ราคาต้องมากกว่าศูนย์")
        self.name = name.strip()
        self.quantity = quantity
        self.price = price

class Inventory:
    def __init__(self):
        self._items: dict[str, InventoryItem] = {}
    ...

[ข้อกำหนด (Requirements & Constraints)]
1. เพิ่มเมธอด `sell_many(orders: dict[str, int]) -> dict[str, int]` คืนค่าเป็น `{ชื่อสินค้า: จำนวนคงเหลือ}`
2. ความเป็นหนึ่งเดียว (Atomicity): ถ้ามีรายการใดรายการหนึ่งไม่มีในระบบ หรือ stock ไม่พอ จะต้องยกเลิกการทำรายการทั้งหมด และต้องไม่มีรายการใดถูกหักยอดออกเด็ดขาด (All-or-Nothing / Rollback)
3. การจัดการข้อผิดพลาด: ใช้ชนิดของ Exception แบบเดียวกับระบบเดิม คือ `KeyError` เมื่อไม่พบสินค้า และ `ValueError` เมื่อจำนวนที่สั่งซื้อไม่ถูกต้องหรือสต็อกไม่เพียงพอ
4. ห้ามติดตั้งหรือใช้ library ภายนอกเพิ่มเติม
5. ใช้ Type Hints และเขียน Docstring ภาษาไทยกำกับ

[ชุดการทดสอบที่โค้ดต้องผ่าน (Acceptance Tests)]
- กรณีขายหลายรายการสำเร็จ: หักสต็อกครบถ้วน และคืนยอดคงเหลือถูกต้อง
- กรณีรายการที่ 2 สต็อกไม่พอ: ต้อง raise ValueError และสต็อกของรายการที่ 1 ต้องไม่ลดลง
````

### ผลลัพธ์โค้ดที่ AI สร้างขึ้น (Round 2 Output):
```python
    def sell_many(self, orders: dict[str, int]) -> dict[str, int]:
        """
        บันทึกการขายสินค้าหลายรายการพร้อมกัน โดยมีคุณสมบัติ Atomicity (All-or-Nothing)
        หากรายการใดรายการหนึ่งไม่สามารถขายได้ จะต้องไม่มีการตัดสต็อกสินค้าใดๆ เลย

        Args:
            orders: ดิกชันนารี {ชื่อสินค้า: จำนวนที่ต้องการซื้อ}

        Returns:
            dict[str, int]: ดิกชันนารี {ชื่อสินค้า: จำนวนคงเหลือหลังการขาย}

        Raises:
            KeyError: เมื่อไม่พบชื่อสินค้าในระบบ
            ValueError: เมื่อจำนวนที่ระบุ <= 0 หรือสินค้าในสต็อกไม่เพียงพอ
        """
        if not orders:
            return {}

        # ขั้นตอนที่ 1: ตรวจสอบความถูกต้องและสต็อกทั้งหมดล่วงหน้า (Validation Phase)
        for name, amount in orders.items():
            if name not in self._items:
                raise KeyError(f"ไม่พบสินค้า '{name}' ในระบบ")
            if amount <= 0:
                raise ValueError(f"จำนวนที่ขายสำหรับสินค้า '{name}' ต้องมากกว่าศูนย์")
            current_qty = self._items[name].quantity
            if current_qty < amount:
                raise ValueError(
                    f"สินค้า '{name}' คงเหลือ {current_qty} ชิ้น ไม่เพียงพอสำหรับการขาย {amount} ชิ้น"
                )

        # ขั้นตอนที่ 2: ดำเนินการตัดสต็อกเมื่อมั่นใจว่าทุกรายการผ่านเงื่อนไข 100% (Execution Phase)
        results: dict[str, int] = {}
        for name, amount in orders.items():
            self._items[name].quantity -= amount
            results[name] = self._items[name].quantity

        return results
```

---

## 3. สรุปการเปรียบเทียบและการวิเคราะห์ (Key Insights)

| มิติการเปรียบเทียบ | รอบที่ 1 (Prompt Only) | รอบที่ 2 (Context Engineering) |
|---|---|---|
| **ความเข้ากันได้กับระบบ (Compatibility)** | ❌ ล้มเหลว (ตั้งชื่อฟิลด์และเมธอดใหม่เอง) | ✅ สมบูรณ์แบบ (ต่อยอดจาก `self._items` และ `InventoryItem`) |
| **ความถูกต้องของตรรกะ (Atomicity)** | ❌ ล้มเหลว (ตัดสต็อกครึ่งๆ กลางๆ ข้อมูลค้าง) | ✅ ถูกต้อง 100% (แยก Validation Phase และ Execution Phase) |
| **Exception Handling** | ❌ ใช้ `Exception` ทั่วไป | ✅ สอดคล้องกับโค้ดเดิม (`KeyError`, `ValueError`) |
| **Type Safety & Documentation** | ❌ ขาด Type Hints | ✅ มี Type Hints และ Docstring ภาษาไทยครบถ้วน |

### 💡 ปัจจัยสำคัญที่ทำให้ผลลัพธ์แตกต่างกัน:
1. **Context คือรากฐานของความถูกต้อง:** AI ไม่สามารถเดาโครงสร้างเดิมของโปรเจกต์ได้ การแนบโค้ดเดิมช่วยตีกรอบให้ AI อยู่ในสถาปัตยกรรมที่ถูกต้อง
2. **การระบุ Test Case และ Edge Case ใน Prompt:** การระบุว่า *"ถ้ารายการที่ 2 ไม่พอ รายการที่ 1 ต้องไม่ถูกหัก"* ทำให้ AI ตระหนักถึงปัญหาเรื่อง State Mutation และเลือกใช้แพทเทิร์น Two-Phase Commit เพื่อแก้ปัญหาเรื่อง Atomicity ได้อย่างแม่นยำ
