# AI Iteration Log: บันทึกการทำงานร่วมกับ AI (Context Engineering)

เอกสารบันทึกการส่งคำสั่ง (Prompts), การเปรียบเทียบผลลัพธ์ของโค้ดก่อนและหลังมี Context และประวัติการปรับปรุง Spec / Rules เพื่อควบคุมผลลัพธ์ของ AI ตามแนวทาง **Spec-Driven Development (SDD)**

---

## 1. ข้อมูลเครื่องมือและสภาพแวดล้อม AI
- **เครื่องมือ / โมเดลที่ใช้:** Google DeepMind Gemini 3.8 Flash (High) / Antigravity IDE
- **ภาษาโปรแกรม:** Python 3.11+
- **ผู้บันทึก:** Phongsakhon870 (นักศึกษาวิศวกรรมคอมพิวเตอร์ / ซอฟต์แวร์)

---

## 2. ตารางเปรียบเทียบผลลัพธ์: ก่อนมี Context (ขั้นที่ 4) vs หลังมี Context (ขั้นที่ 6)

| ประเด็นการตรวจสอบ | ขั้นที่ 4 ก่อนมี Context (`inventory_no_context.py`) | ขั้นที่ 6 หลังมี Context (`models.py`, `notifiers.py`, `service.py`) |
|---|---|---|
| **การแยกไฟล์และแยกหน้าที่ (Modularity & SRP)** | รวมทุกอย่างไว้ในคลาสเดียว (`InventoryManager`) ไฟล์เดียว | แยกเป็น 3 โมดูลชัดเจน: `models.py`, `notifiers.py`, `service.py` แต่ละคลาสมีหน้าที่เดียว |
| **Type Hints & Docstrings** | ขาด Type Hints ในฟังก์ชัน และไม่มี Docstring อธิบายการทำงาน | มี Type Hints ครบทุก signature และมี Docstring ภาษาไทยทุก public method |
| **การเชื่อมต่อระหว่าง Service กับ Notifier (DIP / Coupling)** | `InventoryManager` ผูกติดกับการ print และช่องทาง email/sms โดยตรง | `InventoryService` ขึ้นกับ Abstraction (`StockObserver` protocol) ผ่าน Dependency Injection |
| **การ Hardcode ค่าคงที่และ Config** | Hardcode เบอร์โทร, อีเมลผู้จัดการ และข้อความไว้ใน logic โดยตรง | ไม่มีการ Hardcode ข้อมูลผู้รับใน service โดยส่งผ่าน Constructor ของ Notifier |
| **ความสอดคล้องกับ Design Patterns** | ไม่มีการใช้ Pattern เป็น procedural/monolithic | ใช้ **Observer Pattern** (กระจายเหตุการณ์) และ **Factory Pattern** (สร้าง notifier) |
| **การจัดการเงื่อนไขสต็อกต่ำ (Business Rule)** | ใช้ `<=` ทำให้เตือนผิดเมื่อสต็อกเท่ากับ threshold พอดี | ตรวจสอบเงื่อนไขอย่างถูกต้องตามเกณฑ์ `< threshold` เท่านั้น |

---

## 3. บันทึกการแก้ไข (Iteration Cycles) โดยแก้ที่ Spec และ Context
ตามหลักการ Spec-Driven Development เมื่อพบผลลัพธ์ที่ไม่ตรงตามต้องการ **ห้ามแก้ไขโค้ดด้วยมือ** แต่ให้วิเคราะห์ว่าปัญหาเกิดจาก Spec หรือ Context แล้วจึงแก้ไขที่ต้นทาง

### 🔁 รอบที่ 1: การแก้ไขปัญหาเงื่อนไขสต็อกต่ำ (Threshold Edge Case)
- **ผลที่ผิด:** เมื่อทดสอบกรณีจ่ายสินค้าจนสต็อกเหลือเท่ากับ threshold พอดี (เช่น สต็อกเดิม 20 จ่าย 5 เหลือ 15 และ threshold = 15) ระบบกลับพิมพ์ข้อความแจ้งเตือนสต็อกต่ำออกมา ทั้งที่สต็อกยังไม่ต่ำกว่าเกณฑ์
- **สาเหตุ:**
  1. ใน `specs/spec.md` เดิมไม่ได้ระบุ Scenario สำหรับกรณี `current_quantity == threshold` ไว้อย่างชัดเจน ทำให้ AI ตีความคำว่า "ต่ำกว่า" เป็น "น้อยกว่าหรือเท่ากับ" (`<=`)
  2. ใน `.ai-rules.md` ยังไม่ได้ระบุเน้นย้ำความแตกต่างระหว่าง `<` กับ `<=`
- **วิธีแก้ที่ Spec หรือ Context:**
  1. เพิ่ม Acceptance Criteria ใน `specs/spec.md` (Scenario: จ่ายสินค้าจนสต็อกเท่ากับ threshold พอดี ต้องไม่ส่งการแจ้งเตือน)
  2. เพิ่มข้อกำหนดใน `.ai-rules.md` หัวข้อข้อห้าม: *"แจ้งเตือนเมื่อสต็อกคงเหลือน้อยกว่า threshold เท่านั้น (`current_quantity < threshold`) ไม่ใช่ `<="*
- **ผลหลังแก้:** AI ปรับปรุงโค้ดใน `models.py` และ `service.py` โดยใช้เงื่อนไข `self.quantity < self.threshold` อย่างถูกต้อง ผ่านการทดสอบ Edge Case 100%

---

### 🔁 รอบที่ 2: การแก้ไขการ Hardcode ช่องทางแจ้งเตือน และการละเมิด Open/Closed Principle
- **ผลที่ผิด:** ใน `service.py` เวอร์ชันแรกที่ AI สร้างขึ้น มีการเขียนบล็อกเงื่อนไข:
  ```python
  if channel == "email":
      EmailNotifier().send(...)
  elif channel == "sms":
      SMSNotifier().send(...)
  ```
  และมีการ `import smtplib` เตรียมไว้ ซึ่งทำให้ `InventoryService` รู้จัก Concrete Notifier โดยตรง และหากต้องการเพิ่มช่องทางแจ้งเตือนใหม่ (เช่น LINE) จะต้องกลับมาแก้โค้ดใน `service.py` เสมอ
- **สาเหตุ:**
  1. กฎใน `.ai-rules.md` ยังไม่ได้กำหนดชัดเจนเรื่องการใช้ Observer Pattern และ Dependency Injection
  2. ไม่ได้กำหนดข้อห้ามการ import โมดูลเน็ตเวิร์กจริง (`smtplib`) อย่างชัดเจน
- **วิธีแก้ที่ Spec หรือ Context:**
  1. ปรับปรุง `.ai-rules.md` เพิ่มข้อห้าม: *"ห้ามให้ InventoryService รู้จัก EmailNotifier/SMSNotifier โดยตรง", "ห้ามส่ง email/sms จริง ใช้ print แทน", "รับ dependency ผ่าน constructor"*
  2. อัปเดตระบุในหลักการออกแบบของ `.ai-rules.md`: *"ใช้ Factory pattern สร้าง notifier และใช้ Observer pattern สำหรับกระจายการแจ้งเตือนหลายช่องทางพร้อมกัน"*
- **ผลหลังแก้:** AI ปรับโค้ดให้ `InventoryService` รับ `observers: list[StockObserver]` ผ่าน Constructor และใช้ `NotifierFactory` แยกต่างหาก ทำให้ `InventoryService` ปฏิบัติตามหลัก SRP, OCP และ DIP อย่างสมบูรณ์

---

## 4. บันทึกคำสั่ง Prompts ที่ใช้จริงในแต่ละขั้น

### Prompt ขั้นที่ 3 (Review Spec):
```text
ฉันกำลังทำ Spec-Driven Development ช่วยรีวิว spec ด้านล่างนี้ในฐานะ
senior software engineer ตอบเป็นภาษาไทย โดยชี้เฉพาะจุดที่:
1. acceptance criteria ข้อใดยัง "กำกวม" หรือ "ไม่ testable"
2. มี requirement ใดที่ขัดแย้งกันเองหรือซ้ำซ้อน
3. มี edge case สำคัญใดที่ spec ยังไม่ครอบคลุม (เช่น จ่ายเท่ากับ threshold พอดี)
อย่าเพิ่งเขียนโค้ด ให้เสนอเป็น checklist สั้น ๆ ว่าควรแก้ spec ตรงไหน

[แนบเนื้อหา specs/spec.md]
```

### Prompt ขั้นที่ 4 (No Context Implementation):
```text
จาก spec นี้ ช่วยเขียนโค้ด Python สำหรับฟีเจอร์แจ้งเตือนสต็อกต่ำ

[แนบเนื้อหา specs/spec.md]
```

### Prompt ขั้นที่ 6 (Implement with Context):
```text
คุณคือ AI coding agent ของโปรเจกต์นี้ ทำตามกฎใน .ai-rules.md อย่างเคร่งครัด
implement ฟีเจอร์ตาม spec ด้านล่าง โดยแยกไฟล์ตามที่กฎกำหนด (models / notifiers / service)
ทุก acceptance criteria ใน spec ต้อง implement ครบ

[แนบเนื้อหา .ai-rules.md]
---
[แนบเนื้อหา specs/spec.md]
```

### Prompt ขั้นที่ 8 (Generate Diagrams):
```text
จากโค้ดใน models.py, notifiers.py, service.py ด้านล่าง
สร้าง Class Diagram เป็น Mermaid (classDiagram) แสดง class, attribute,
method, visibility และความสัมพันธ์ (composition, dependency, realization)

[แนบโค้ดทั้ง 3 ไฟล์]
```
และ
```text
สร้าง Sequence Diagram เป็น Mermaid (sequenceDiagram) แสดง flow เมื่อ
พนักงานจ่ายสินค้าจนสต็อกต่ำกว่า threshold ตั้งแต่ InventoryService.issue()
จนถึงการเรียก notifier.send()
```

### Prompt ขั้นที่ 10 (Refactor with Factory + Observer):
```text
จากผลการตรวจ SOLID design นี้ละเมิด OCP และ DIP เพราะ InventoryService
สร้าง notifier เอง ช่วย refactor ตามนี้:
1. ใช้ Factory pattern: NotifierFactory.create(channel) คืน Notifier
2. InventoryService รับ Notifier ผ่าน constructor (DIP)
3. รองรับหลายปลายทางพร้อมกันด้วย Observer pattern: InventoryService เก็บ
   list ของ observer และเรียก notify ทุกตัวเมื่อสต็อกต่ำกว่า threshold
   โดยไม่รู้ว่าแต่ละ observer เป็นช่องทางอะไร
อย่าแก้ business logic การคำนวณสต็อก ให้แก้เฉพาะส่วน notification
```
