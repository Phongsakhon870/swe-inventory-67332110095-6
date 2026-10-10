# ระบบจัดการสินค้าคงคลัง (Inventory Management System)

โครงการพัฒนาระบบสินค้าคงคลังสำหรับรายวิชา **Software Engineering in AI Era** — มหาวิทยาลัยเทคโนโลยีราชมงคลอีสาน
ครอบคลุมงานพัฒนาตามหลักวิศวกรรมซอฟต์แวร์ยุคใหม่ตั้งแต่เริ่มต้นจนถึงการส่งมอบและจริยธรรม:
- **Lab 2:** จำลอง Sprint แบบ Agile, GitHub Flow, และระบบควบคุมเวอร์ชัน (Scrum, PR Reviews, Retrospective)
- **Lab 3:** การพัฒนาซอฟต์แวร์แบบขับเคลื่อนด้วยข้อกำหนด (Spec-Driven Development & Context Engineering)
- **Lab 4:** การออกแบบ UX, Code Review โค้ดที่ AI สร้าง และ Evidence-Based Debugging
- **Lab 5:** TDD เป็นตาข่ายกันพลาด, Refactoring โค้ด Legacy ด้วย Characterization Tests, CI/CD Pipeline และจริยธรรม AI

---

## 📂 โครงสร้างไดเรกทอรี (Directory Structure)

```text
Inventory Management System/
│
├── .github/
│   └── workflows/
│       └── ci.yml                  # GitHub Actions CI Workflow (Ruff Lint + Pytest Coverage >= 85%) (Lab 5)
├── pyproject.toml                  # การตั้งค่า Ruff Linter และ Coverage Tool (Lab 5)
├── requirements.txt                # รายการ Dependencies สำหรับการทดสอบ (pytest, pytest-cov, ruff) (Lab 5)
├── .gitignore                      # กำหนดไฟล์ที่ไม่ต้องการให้ Git ติดตาม
├── README.md                       # เอกสารสรุปภาพรวมและผลการดำเนินงานทุก Lab
│
├── inventory.py                    # โค้ด CLI สต็อกร้านเขียนดี (US-01, US-02, US-03, TDD low_stock_items, sell)
├── data/
│   └── inventory.json              # ไฟล์จัดเก็บข้อมูลสินค้า JSON
├── pricing.py                      # โมดูลคิดราคาและส่วนลดฉบับ Refactored สะอาด ปลอดภัย ปราศจาก Magic Literals (Lab 5)
├── pricing_legacy.py               # โค้ดคำนวณราคาเดิม (Legacy) ที่นำมาทำ Characterization Tests (Lab 5)
│
├── test-gap.md                     # ตารางเปรียบเทียบ Test Gap วิเคราะห์จุดที่ AI เขียน Test ง่ายเกินไป (Lab 5)
├── coverage-note.md                # บันทึกการวิเคราะห์ Test Coverage พร้อมคำตอบ 3 ข้อ (Lab 5)
├── smells.md                       # บันทึก Code Smells 6 ข้อในโค้ดเดิม pricing_legacy.py (Lab 5)
├── ethics.md                       # รายงานจริยธรรมวิศวกรรมซอฟต์แวร์ 4 มิติ และแนวปฏิบัติส่วนบุคคล (Lab 5)
│
├── TEAM_CHARTER.md                 # กฎบัตรทีม, บทบาท, GitHub Flow, WIP limit และ AI Policy (Lab 2)
├── RETRO-SPRINT-1.md               # รายงาน Retrospective: Velocity, WIP Limit, Start-Stop-Continue (Lab 2)
├── screenshots/
│   ├── board-sprint-1.png          # ภาพหน้าจอ Project Board ณ สิ้น Sprint 1 (Lab 2)
│   ├── ci-green.png                # ภาพหน้าจอ GitHub Actions CI รันผ่าน (สีเขียว) 100% (Lab 5)
│   └── ci-red.png                  # ภาพหน้าจอ GitHub Actions CI รันไม่ผ่าน (สีแดง) เมื่อจงใจให้มี Bug (Lab 5)
│
├── tests/
│   ├── test_lab02.py               # ชุดทดสอบ Automated Unit Tests สำหรับ Lab 2 (7 tests)
│   ├── test_inventory.py           # ชุดทดสอบ TDD และ Hardened Tests ของ low_stock_items และ sell (Lab 5) (15 tests)
│   └── test_pricing_legacy.py      # Characterization Tests พิสูจน์ pricing_legacy vs pricing.py (Lab 5) (24 tests)
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
│       └── test_inventory.py       # ชุด Automated Unit Tests ครอบคลุมทุก Acceptance Criteria (9 tests)
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
    │   └── test_discount.py        # ชุดทดสอบ pytest สำหรับโมดูล discount.py (6 tests)
    └── assets/
        ├── wireframe-ai.md         # Text Wireframe (ASCII Layout) 3 หน้าจอ (Login, Dashboard, Add Product)
        ├── inventory_mockups.drawio# ไฟล์ UI Mockup ฉบับเต็ม (draw.io / diagrams.net)
        └── mockup-link.txt         # คำอธิบายและแนวทางการเปิดดู UI Mockup
```

---

## 🧪 การทดสอบระบบ (Automated Testing)

### 1. ทดสอบ Lab 5 (TDD, Characterization Tests, และ Coverage)
```bash
# ตรวจสอบ Lint ด้วย Ruff
ruff check .

# รันชุดทดสอบทั้งหมดพร้อมวัด Coverage
pytest tests/ --cov=. --cov-report=term-missing --cov-fail-under=85
```
ผลการทดสอบ: **46/46 ผ่านทั้งหมด (100% PASSED) | Total Coverage: 92% (ผ่านเกณฑ์ >= 85%)**

### 2. ทดสอบ Lab 2 (Agile Sprint 1 - CLI Inventory System)
```bash
python -m unittest tests/test_lab02.py -v
```
ผลการทดสอบ: **7/7 ผ่านทั้งหมด (OK 100%)**

### 3. ทดสอบ Lab 3 (Spec-Driven Inventory System)
```bash
cd inventory-sdd
python -m unittest discover -s tests -v
cd ..
```
ผลการทดสอบ: **9/9 ผ่านทั้งหมด (OK 100%)**

### 4. ทดสอบ Lab 4 (Discount & Math Module)
```bash
cd lab04-ai-coding-ux
python -m pytest tests/test_discount.py -v
cd ..
```
ผลการทดสอบ: **6/6 ผ่านทั้งหมด (PASSED 100%)**

---

## 🔗 ลิงก์สำหรับส่งงานใน eLearning (Submission Links)

### ลิงก์หลักของ Repository
- **GitHub Repository (Public):** [https://github.com/Phongsakhon870/swe-inventory-67332110095-6](https://github.com/Phongsakhon870/swe-inventory-67332110095-6)
- **GitHub Actions Runs (CI Pipeline):** [https://github.com/Phongsakhon870/swe-inventory-67332110095-6/actions](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/actions)

### ลิงก์ส่งงาน Lab 5 (TDD, Refactoring Legacy & CI/CD)
- **ไฟล์ทดสอบ TDD & Edge Cases:** [tests/test_inventory.py](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/tests/test_inventory.py)
- **ตาราง Test Gap Analysis:** [test-gap.md](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/test-gap.md)
- **บันทึก Coverage Note:** [coverage-note.md](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/coverage-note.md)
- **วิเคราะห์ Code Smells:** [smells.md](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/smells.md)
- **Characterization Tests:** [tests/test_pricing_legacy.py](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/tests/test_pricing_legacy.py)
- **โค้ด Refactored ฉบับใหม่:** [pricing.py](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/pricing.py)
- **CI Workflow & Ruff Config:** [.github/workflows/ci.yml](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/.github/workflows/ci.yml) | [pyproject.toml](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/pyproject.toml)
- **หลักฐานภาพหน้าจอ CI:** [screenshots/ci-green.png](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/screenshots/ci-green.png) | [screenshots/ci-red.png](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/screenshots/ci-red.png)
- **เอกสารจริยธรรมและแนวปฏิบัติ:** [ethics.md](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/ethics.md)
- **Merged Pull Request Lab 5:** [feat/low-stock-alert](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/tree/feat/low-stock-alert)

### ลิงก์ส่งงาน Lab 2 (Agile Sprint Simulation & GitHub Flow)
- **TEAM_CHARTER.md:** [TEAM_CHARTER.md](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/TEAM_CHARTER.md)
- **RETRO-SPRINT-1.md:** [RETRO-SPRINT-1.md](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/RETRO-SPRINT-1.md)
- **Project Board Screenshot:** [screenshots/board-sprint-1.png](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/screenshots/board-sprint-1.png)
- **Merged PRs:** [PR #1](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/tree/feat/1-list-items) | [PR #2](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/tree/feat/2-add-item) | [PR #3](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/tree/feat/3-update-stock) | [PR #4](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/tree/docs/4-retro-sprint-1)

### ลิงก์ส่งงาน Lab 3 (Spec-Driven Development)
- [inventory-sdd/specs/spec.md](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/inventory-sdd/specs/spec.md)
- [inventory-sdd/.ai-rules.md](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/inventory-sdd/.ai-rules.md)
- [inventory-sdd/design_review.md](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/inventory-sdd/design_review.md)
- [inventory-sdd/AI_ITERATION_LOG.md](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/inventory-sdd/AI_ITERATION_LOG.md)

### ลิงก์ส่งงาน Lab 4 (UX & Code Review)
- [lab04-ai-coding-ux/code-review.md](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/lab04-ai-coding-ux/code-review.md)
- [lab04-ai-coding-ux/debug-log.md](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/lab04-ai-coding-ux/debug-log.md)
- [lab04-ai-coding-ux/persona.md](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/lab04-ai-coding-ux/persona.md)
- [lab04-ai-coding-ux/accessibility-review.md](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/lab04-ai-coding-ux/accessibility-review.md)
- [lab04-ai-coding-ux/prompt-vs-context.md](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/lab04-ai-coding-ux/prompt-vs-context.md)

