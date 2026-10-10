# ระบบจัดการสินค้าคงคลัง (Inventory Management System)

โครงการพัฒนาระบบสินค้าคงคลังสำหรับรายวิชา **Software Engineering in AI Era** — มหาวิทยาลัยเทคโนโลยีราชมงคลอีสาน
ครอบคลุมงานพัฒนาและการประเมินคุณภาพใน **Lab 3 (Spec-Driven Development)** และ **Lab 4 (UX, Code Review & Evidence-based Debugging)**

---

## 📂 โครงสร้างไดเรกทอรี (Directory Structure)

```text
Inventory Management System/
│
├── .gitignore                      # กำหนดไฟล์ที่ไม่ต้องการให้ Git ติดตาม
├── README.md                       # เอกสารสรุปภาพรวมและผลการดำเนินงาน
│
├── inventory-sdd/                  # โฟลเดอร์งาน Lab 3 (Spec-Driven Development & Context Engineering)
│   ├── .ai-rules.md                # ไฟล์กฎและ Context สำหรับกำกับ AI Agent
│   ├── AI_ITERATION_LOG.md         # บันทึก Prompts, ผลลัพธ์ก่อน/หลัง context และรอบการปรับปรุง
│   ├── design_review.md            # ตารางวิเคราะห์การออกแบบตามหลัก SOLID ทั้ง 5 ข้อ
│   ├── specs/
│   │   └── spec.md                 # เอกสาร Specification (User Stories, AC, FR, NFR)
│   ├── diagrams/
│   │   ├── class.md                # Class Diagram แสดงโครงสร้างและ Design Patterns (Mermaid)
│   │   └── sequence.md             # Sequence Diagram แสดง Flow การตัดสต็อกและแจ้งเตือน (Mermaid)
│   ├── src/
│   │   ├── inventory.py            # โค้ดตั้งต้นจาก Lab 2 (Baseline)
│   │   ├── inventory_no_context.py # โค้ดผลลัพธ์จาก AI ขั้นที่ 4 ก่อนมีไฟล์กฎ (Monolithic/Violations)
│   │   ├── models.py               # Domain Models: Product, Category, StockTransaction
│   │   ├── notifiers.py            # Observer & Factory: Notifier Protocol, Email, SMS, NotifierFactory
│   │   └── service.py              # Business Logic: InventoryService (SOLID Compliant)
│   └── tests/
│       └── test_inventory.py       # ชุด Automated Unit Tests ครอบคลุมทุก Acceptance Criteria
│
└── lab04-ai-coding-ux/             # โฟลเดอร์งาน Lab 4 (UX, Code Review โค้ดที่ AI สร้าง และ Debugging)
    ├── findings-lab04.md           # สรุปผลการสัมภาษณ์ผู้ใช้, Needs, Pain Points และ Point of View
    ├── persona.md                  # Persona (สมชาย รักษาคลัง) และ Journey Map 5 ขั้นตอน
    ├── accessibility-review.md     # ตรวจสอบ Accessibility WCAG 2.1 AA และจุดที่ AI พลาด
    ├── prompt-vs-context.md        # เปรียบเทียบ Prompt สั้น ๆ vs Prompt ที่มี Context ครบถ้วน
    ├── code-review.md              # ตรวจ PR โมดูล inventory_service.py พร้อม Review Comments และตารางจัดหมวด
    ├── debug-log.md                # บันทึกการ Debug โมดูล discount.py ตามหลักฐาน 5 ขั้นตอน
    ├── discount.py                 # โค้ดคำนวณส่วนลดที่แก้ไข Root Cause เรียบร้อยแล้ว
    ├── tests/
    │   └── test_discount.py        # ชุดทดสอบ pytest สำหรับโมดูล discount.py
    └── assets/
        ├── wireframe-ai.md         # Text Wireframe (ASCII Layout) 3 หน้าจอ (Login, Dashboard, Add Product)
        ├── inventory_mockups.drawio# ไฟล์ UI Mockup ฉบับเต็ม (draw.io / diagrams.net)
        └── mockup-link.txt         # คำอธิบายและแนวทางการเปิดดู UI Mockup
```

---

## 🧪 การทดสอบระบบ (Automated Testing)

### 1. ทดสอบ Lab 3 (Spec-Driven Inventory System)
```bash
cd inventory-sdd
python -m unittest discover -s tests -v
```
ผลการทดสอบ: **9/9 ผ่านทั้งหมด (OK)**

### 2. ทดสอบ Lab 4 (Discount & Math Module)
```bash
cd lab04-ai-coding-ux
python -m pytest tests/test_discount.py -v
```
ผลการทดสอบ: **6/6 ผ่านทั้งหมด (PASSED 100%)**

---

## 🔗 ลิงก์สำหรับส่งงานใน eLearning (Submission Links)

### ลิงก์หลักของ Repository
- **GitHub Repository:** [https://github.com/Phongsakhon870/Inventory-Management-System](https://github.com/Phongsakhon870/Inventory-Management-System)

### ลิงก์ส่งงาน Lab 3
- [inventory-sdd/specs/spec.md](https://github.com/Phongsakhon870/Inventory-Management-System/blob/main/inventory-sdd/specs/spec.md)
- [inventory-sdd/.ai-rules.md](https://github.com/Phongsakhon870/Inventory-Management-System/blob/main/inventory-sdd/.ai-rules.md)
- [inventory-sdd/design_review.md](https://github.com/Phongsakhon870/Inventory-Management-System/blob/main/inventory-sdd/design_review.md)
- [inventory-sdd/AI_ITERATION_LOG.md](https://github.com/Phongsakhon870/Inventory-Management-System/blob/main/inventory-sdd/AI_ITERATION_LOG.md)

### ลิงก์ส่งงาน Lab 4
- **Code Review Document:** [lab04-ai-coding-ux/code-review.md](https://github.com/Phongsakhon870/Inventory-Management-System/blob/main/lab04-ai-coding-ux/code-review.md)
- **Evidence-Based Debug Log:** [lab04-ai-coding-ux/debug-log.md](https://github.com/Phongsakhon870/Inventory-Management-System/blob/main/lab04-ai-coding-ux/debug-log.md)
- **Persona & Journey Map:** [lab04-ai-coding-ux/persona.md](https://github.com/Phongsakhon870/Inventory-Management-System/blob/main/lab04-ai-coding-ux/persona.md)
- **Accessibility Review:** [lab04-ai-coding-ux/accessibility-review.md](https://github.com/Phongsakhon870/Inventory-Management-System/blob/main/lab04-ai-coding-ux/accessibility-review.md)
- **Prompt vs Context Engineering:** [lab04-ai-coding-ux/prompt-vs-context.md](https://github.com/Phongsakhon870/Inventory-Management-System/blob/main/lab04-ai-coding-ux/prompt-vs-context.md)
