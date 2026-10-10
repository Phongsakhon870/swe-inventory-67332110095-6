# ระบบจัดการสินค้าคงคลัง (Inventory Management System)

โครงการพัฒนาระบบสินค้าคงคลังด้วยกระบวนการ **Spec-Driven Development (SDD)** และ **Context Engineering**
สำหรับรายวิชา **Software Engineering in AI Era (Lab 3)** — มหาวิทยาลัยเทคโนโลยีราชมงคลอีสาน

---

## 📌 ภาพรวมโครงการ (Project Overview)
โครงการนี้เป็นการต่อยอดและพัฒนาระบบคลังสินค้าด้วยการเขียน Specification กำกับ AI ก่อนการสร้างโค้ดจริง (Spec-First) แทนการปล่อยให้ AI คาดเดา โดยครอบคลุม:
1. **การกำหนด Spec และ Acceptance Criteria:** ในรูปแบบ Given-When-Then ตามเกณฑ์ MASTER
2. **Context Engineering:** การสร้างไฟล์ข้อกำหนด `.ai-rules.md` เพื่อควบคุมคุณภาพ สถาปัตยกรรม และมาตรฐานของโค้ด
3. **การประเมินและปรับปรุงตามหลัก SOLID:** SRP, OCP, LSP, ISP, DIP
4. **การประยุกต์ใช้ Design Patterns:** Observer Pattern สำหรับระบบแจ้งเตือนหลายช่องทาง และ Factory Pattern สำหรับการสร้าง Notifier

---

## 📂 โครงสร้างไดเรกทอรี (Directory Structure)

```text
Inventory Management System/
│
├── .gitignore                      # กำหนดไฟล์ที่ไม่ต้องการให้ Git ติดตาม
├── README.md                       # เอกสารแนะนำโครงการและสรุปผลงาน
│
└── inventory-sdd/                  # โฟลเดอร์งาน Lab 3 Spec-Driven Development
    │
    ├── .ai-rules.md                # ไฟล์กฎและ Context สำหรับกำกับ AI Agent
    ├── AI_ITERATION_LOG.md         # บันทึก Prompts, ผลลัพธ์ก่อน/หลัง context และรอบการปรับปรุง
    ├── design_review.md            # ตารางวิเคราะห์การออกแบบตามหลัก SOLID ทั้ง 5 ข้อ
    │
    ├── specs/
    │   └── spec.md                 # เอกสาร Specification (User Stories, AC, FR, NFR)
    │
    ├── diagrams/
    │   ├── class.md                # Class Diagram แสดงโครงสร้างและ Design Patterns (Mermaid)
    │   └── sequence.md             # Sequence Diagram แสดง Flow การตัดสต็อกและแจ้งเตือน (Mermaid)
    │
    ├── src/
    │   ├── inventory.py            # โค้ดตั้งต้นจาก Lab 2 (Baseline)
    │   ├── inventory_no_context.py # โค้ดผลลัพธ์จาก AI ขั้นที่ 4 ก่อนมีไฟล์กฎ (Monolithic/Violations)
    │   ├── models.py               # Domain Models: Product, Category, StockTransaction
    │   ├── notifiers.py            # Observer & Factory: Notifier Protocol, Email, SMS, NotifierFactory
    │   └── service.py              # Business Logic: InventoryService (SOLID Compliant)
    │
    └── tests/
        └── test_inventory.py       # ชุด Automated Unit Tests ครอบคลุมทุก Acceptance Criteria
```

---

## 🚀 ฟีเจอร์หลักของระบบ (Features)

1. **บันทึกรับ/จ่ายสินค้า (US-01 / FR-01, FR-02):**
   - ตรวจสอบจำนวนคงเหลือก่อนจ่าย ปฏิเสธการทำรายการหากสินค้าไม่พอ
   - บันทึกประวัติการทำธุรกรรม (Transaction History) อัตโนมัติ
2. **แจ้งเตือนสต็อกต่ำ (US-02, US-05 / FR-03, FR-06):**
   - ตรวจสอบเกณฑ์สต็อกต่ำอย่างแม่นยำ (`quantity < threshold`)
   - รองรับการกระจายการแจ้งเตือนไปยังหลายช่องทางพร้อมกัน (Email, SMS) ด้วย **Observer Pattern**
3. **รายงานมูลค่าสต็อกสินค้า (US-03 / FR-04):**
   - คำนวณมูลค่าสินค้าคงคลังรวมแยกตามแต่ละหมวดหมู่ (Category Valuation Report)
4. **ตั้งค่าเกณฑ์สต็อกต่ำเฉพาะรายการ (US-04 / FR-05):**
   - ปรับเปลี่ยนค่า Threshold รายสินค้าได้อย่างยืดหยุ่น

---

## 🧪 การทดสอบระบบ (Automated Testing)

รันชุดทดสอบด้วย `unittest`:

```bash
cd inventory-sdd
python -m unittest discover -s tests -v
```

ผลการทดสอบผ่าน 100% (9 รายการทดสอบ):
- `test_us01_receive_stock_success` (บันทึกรับสินค้าเข้าคลัง)
- `test_us01_issue_stock_insufficient` (จ่ายสินค้าเมื่อสต็อกไม่เพียงพอ)
- `test_us02_issue_stock_below_threshold_triggers_alert` (แจ้งเตือนเมื่อสต็อกต่ำกว่าเกณฑ์)
- `test_us02_issue_stock_above_threshold_no_alert` (ไม่แจ้งเตือนเมื่อสต็อกยังสูง)
- `test_us02_issue_stock_exactly_at_threshold_no_alert` (Edge Case: สต็อกเท่ากับ threshold พอดีต้องไม่เตือน)
- `test_us03_stock_value_report` (คำนวณมูลค่าสต็อกแยกหมวดหมู่)
- `test_us04_custom_threshold_update` (ตั้งค่า threshold รายสินค้า)
- `test_us05_multi_channel_notification_and_factory` (สร้างและส่งแจ้งเตือนผ่าน Factory + Observer)
- `test_nfr01_performance_large_catalog` (วัด Performance คำนวณ 1,000 รายการใน < 1 วินาที)

---

## 🔗 ลิงก์สำหรับส่งงาน Lab 3 (eLearning Submission Links)
- **Repository URL:** [https://github.com/Phongsakhon870/inventory-management-system](https://github.com/Phongsakhon870/inventory-management-system)
- **Spec File:** [inventory-sdd/specs/spec.md](https://github.com/Phongsakhon870/inventory-management-system/blob/main/inventory-sdd/specs/spec.md)
- **AI Rules File:** [inventory-sdd/.ai-rules.md](https://github.com/Phongsakhon870/inventory-management-system/blob/main/inventory-sdd/blob/main/inventory-sdd/.ai-rules.md)
- **Design Review:** [inventory-sdd/design_review.md](https://github.com/Phongsakhon870/inventory-management-system/blob/main/inventory-sdd/design_review.md)
- **AI Iteration Log:** [inventory-sdd/AI_ITERATION_LOG.md](https://github.com/Phongsakhon870/inventory-management-system/blob/main/inventory-sdd/AI_ITERATION_LOG.md)
