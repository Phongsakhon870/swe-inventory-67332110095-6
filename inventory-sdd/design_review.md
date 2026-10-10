# รายงานการประเมินการออกแบบตามหลัก SOLID (Design Review)

เอกสารการตรวจสอบและวิเคราะห์การออกแบบสถาปัตยกรรมซอฟต์แวร์ตามหลักการ **SOLID Principles** เพื่อประเมินจุดบกพร่องของโค้ดร่างแรก (`inventory_no_context.py`) และสรุปแนวทางการปรับปรุงโครงสร้าง (Refactoring) สู่สถาปัตยกรรมที่ถูกต้อง

---

## ตารางประเมินหลักการ SOLID (SOLID Review Matrix)

| หลัก SOLID | สถานะในโค้ดร่างแรก | Class / Method ที่เกี่ยวข้อง | คำอธิบายและผลกระทบเชิงลบ | แนวทางปรับปรุงและผลลัพธ์หลัง Refactor |
|---|---|---|---|---|
| **S (Single Responsibility Principle)** | **ละเมิด** ❌ | `InventoryManager.issue_stock()` ใน `inventory_no_context.py` | เมธอดเดียวรับผิดชอบหลายหน้าที่เกินไป: (1) ตรวจสอบและตัดยอดสต็อก (2) ตรวจสอบเงื่อนไขการแจ้งเตือน (3) ตัดสินใจเลือกช่องทางการแจ้งเตือน และ (4) ทำ I/O console print<br>**ผลกระทบ:** หากต้องการปรับเปลี่ยนรูปแบบข้อความ หรือแก้ไขขั้นตอนการบันทึกประวัติ มีความเสี่ยงสูงที่จะทำให้ Business Logic การตัดสต็อกเกิดข้อผิดพลาด | **แยกหน้าที่ออกเป็นโมดูลอิสระ:**<br>- `InventoryService.issue()` ทำหน้าที่เฉพาะ Business Logic การตัดสต็อกและบันทึกธุรกรรม<br>- `Product.is_low_stock()` รับผิดชอบตรวจสอบเกณฑ์สต็อกต่ำ<br>- `EmailNotifier` / `SMSNotifier` รับผิดชอบการจัดรูปแบบข้อความและการส่งข้อความเท่านั้น |
| **O (Open/Closed Principle)** | **ละเมิด** ❌ | `InventoryManager.issue_stock()` ใน `inventory_no_context.py` | มีการใช้เงื่อนไขตรวจสอบช่องทางแบบ Hardcode:<br>`if channel == "email": ... elif channel == "sms": ...`<br>**ผลกระทบ:** ทุกครั้งที่ธุรกิจต้องการเพิ่มช่องทางใหม่ (เช่น LINE Notify, Telegram, Discord, Webhook) จะต้องแก้ไขโค้ดหลักของ `InventoryManager` ส่งผลให้ระบบไม่ปิดต่อการแก้ไข (Not Closed for Modification) และอาจกระทบช่องทางเดิม | **ประยุกต์ใช้ Observer Pattern และ Factory Pattern:**<br>- `InventoryService` เปิดรับ `StockObserver` ใดๆ เข้ามาลงทะเบียนผ่าน `add_observer()` ได้อย่างอิสระโดยไม่ต้องแก้ไขโค้ดภายใน Service อีกต่อไป<br>- เพิ่มคลาส `Notifier` ใหม่ได้โดยเพียงแค่ implement `StockObserver` และเพิ่มการสร้างใน `NotifierFactory` |
| **L (Liskov Substitution Principle)** | **สอดคล้อง** ✅ | `EmailNotifier`, `SMSNotifier` | อ็อบเจกต์ของ `EmailNotifier` และ `SMSNotifier` ปฏิบัติตามสัญญา (Contract) ของ Protocol `Notifier` และ `StockObserver` ครบถ้วน สามารถแทนที่กันได้โดยไม่ทำให้พฤติกรรมของระบบผิดเพี้ยน<br>**ผลกระทบ:** ทำให้ `InventoryService` สามารถเรียกใช้งาน Observer ทุกตัวผ่าน Interface เดียวกันได้อย่างราบรื่น | **รักษาความเข้ากันได้ของ Interface:**<br>ทั้งสองคลาสรองรับเมธอด `on_low_stock(product: Product)` และคืนค่าตามมาตรฐาน ทำให้สามารถสลับหรือใช้งานร่วมกันได้ทุกสถานการณ์ |
| **I (Interface Segregation Principle)** | **สอดคล้อง** ✅ | `Notifier` และ `StockObserver` ใน `notifiers.py` | มีการแยก Protocol ออกเป็น 2 ส่วนตามบทบาทหน้าที่ที่แท้จริง:<br>1. `Notifier` สำหรับคลาสที่ต้องการฟังก์ชันการส่งข้อความ (`send`)<br>2. `StockObserver` สำหรับคลาสที่ต้องการรับฟังเหตุการณ์สต็อกต่ำ (`on_low_stock`)<br>**ผลกระทบ:** คลาสผู้ใช้งานไม่ต้องถูกบังคับให้ implement เมธอดที่ตนเองไม่ได้ใช้ | **แยกย่อย Interface ให้กระชับ:**<br>คลาสที่ต้องการเพียงแค่ส่งข้อความทั่วไปสามารถใช้เฉพาะ `Notifier` ได้ โดยไม่จำเป็นต้องผูกกับระบบ Event ของสต็อกสินค้า |
| **D (Dependency Inversion Principle)** | **ละเมิด** ❌ | `InventoryManager` ใน `inventory_no_context.py` | โมดูลระดับสูง (`InventoryManager`) ผูกติดกับรายละเอียดระดับต่ำโดยตรง (การระบุชื่อช่องทาง email/sms, ข้อมูลที่อยู่ผู้รับ, และการพิมพ์ข้อความ)<br>**ผลกระทบ:** โค้ดมี Coupling สูง ไม่สามารถนำ `InventoryManager` ไปใช้ในสภาพแวดล้อมอื่น (เช่น ส่งแจ้งเตือนผ่าน API จริง หรือรัน Automated Unit Test แบบ Mock) ได้โดยไม่กระทบโค้ดเดิม | **ประยุกต์ใช้ Dependency Injection (DI):**<br>- `InventoryService` ขึ้นต่อ Abstraction (`StockObserver` Protocol) ไม่รู้จัก `EmailNotifier` หรือ `SMSNotifier` โดยตรง<br>- ส่งรายการ Observers เข้ามาผ่าน Constructor (`__init__`) ทำให้โค้ด Loose Coupling และง่ายต่อการทดสอบ Unit Test 100% |

---

## สรุปภาพรวมเชิงสถาปัตยกรรม (Architectural Summary)

```text
[ ก่อน Refactor: High Coupling & Low Cohesion ]
InventoryManager (Monolithic) ─── Direct Dependency ───> Email / SMS / Console Print / Hardcoded Config

[ หลัง Refactor: Clean Architecture with SOLID ]
InventoryService (High-level Business Logic)
       │
       ▼ (ขึ้นกับ Abstraction ผ่าน Dependency Injection)
<<StockObserver Protocol>>
       ▲
       │ (Realization)
 ┌─────┴────────────────┐
 │                      │
EmailNotifier        SMSNotifier
 (Low-level)          (Low-level)
```

1. **SRP:** โค้ดถูกแบ่งสัดส่วนอย่างชัดเจน:
   - `models.py` รับผิดชอบ Data Structures และ Domain Validation
   - `service.py` รับผิดชอบเฉพาะ Business Rules และ Workflow การจัดการคลังสินค้า
   - `notifiers.py` รับผิดชอบเฉพาะช่องทางการส่งข้อมูลและการแปลง Event เป็น Notification
2. **OCP & DIP:** สามารถเพิ่มช่องทางการแจ้งเตือนใหม่ เช่น `LineNotifier` หรือ `SlackNotifier` ได้ทันที โดยสร้างคลาสใหม่และลงทะเบียนเข้าสู่ `InventoryService` โดยไม่มีการแตะต้องหรือแก้ไขโค้ดใน `service.py` แม้แต่บรรทัดเดียว
