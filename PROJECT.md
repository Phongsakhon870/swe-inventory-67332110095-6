# โครงงานบูรณาการระบบจัดการสินค้าคงคลัง (Inventory Management System)
## PROJECT.md — เอกสารสารบัญหลักสำหรับตรวจประเมินโครงงาน

เอกสารฉบับนี้จัดทำขึ้นสำหรับอาจารย์ผู้สอนและผู้ตรวจประเมินโครงงานรายวิชา **Software Engineering in AI Era** เพื่อให้สามารถคลิกลิงก์เข้าดูผลงานและหลักฐานเชิงประจักษ์ในแต่ละหัวข้อได้อย่างครบถ้วนและสะดวก รวดเร็ว

---

## 📌 สรุปสารบัญ 5 หัวข้อหลักสำหรับตรวจโครงงาน

| ลำดับ | หัวข้อการตรวจประเมิน | ไฟล์เอกสารหลัก (คลิกเปิดได้ทันที) | ลิงก์ตรงบน GitHub Repository |
|:---:|---|---|---|
| **1** | **Spec ของระบบ** | [inventory-sdd/specs/spec.md](inventory-sdd/specs/spec.md) | [ดูบน GitHub](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/inventory-sdd/specs/spec.md) |
| **2** | **Class Diagram & Sequence Diagram** | [inventory-sdd/diagrams/class.md](inventory-sdd/diagrams/class.md)<br>[inventory-sdd/diagrams/sequence.md](inventory-sdd/diagrams/sequence.md) | [Class Diagram บน GitHub](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/inventory-sdd/diagrams/class.md)<br>[Sequence Diagram บน GitHub](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/inventory-sdd/diagrams/sequence.md) |
| **3** | **งานฝั่งผู้ใช้ (Persona, Wireframe, Accessibility)** | [lab04-ai-coding-ux/persona.md](lab04-ai-coding-ux/persona.md)<br>[lab04-ai-coding-ux/assets/wireframe-ai.md](lab04-ai-coding-ux/assets/wireframe-ai.md)<br>[lab04-ai-coding-ux/accessibility-review.md](lab04-ai-coding-ux/accessibility-review.md) | [Persona บน GitHub](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/lab04-ai-coding-ux/persona.md)<br>[Wireframe บน GitHub](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/lab04-ai-coding-ux/assets/wireframe-ai.md)<br>[Accessibility บน GitHub](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/lab04-ai-coding-ux/accessibility-review.md) |
| **4** | **Test อัตโนมัติ และผลการรัน CI** | [tests/test_inventory.py](tests/test_inventory.py)<br>[tests/test_pricing_legacy.py](tests/test_pricing_legacy.py)<br>[screenshots/ci-green.png](screenshots/ci-green.png)<br>[.github/workflows/ci.yml](.github/workflows/ci.yml) | [Test Inventory บน GitHub](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/tests/test_inventory.py)<br>[CI Passed บน GitHub](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/screenshots/ci-green.png)<br>[GitHub Actions Runs](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/actions) |
| **5** | **บันทึกการใช้ AI** | [inventory-sdd/AI_ITERATION_LOG.md](inventory-sdd/AI_ITERATION_LOG.md)<br>[lab04-ai-coding-ux/prompt-vs-context.md](lab04-ai-coding-ux/prompt-vs-context.md)<br>[test-gap.md](test-gap.md)<br>[ethics.md](ethics.md) | [AI Iteration Log บน GitHub](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/inventory-sdd/AI_ITERATION_LOG.md)<br>[Prompt vs Context บน GitHub](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/lab04-ai-coding-ux/prompt-vs-context.md)<br>[Test Gap บน GitHub](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/test-gap.md)<br>[Ethics บน GitHub](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/ethics.md) |

---

## 1. Spec ของระบบ (System Specification)
- **ไฟล์เอกสารข้อกำหนด:** [inventory-sdd/specs/spec.md](inventory-sdd/specs/spec.md) ([URL บน GitHub](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/inventory-sdd/specs/spec.md))
- **เนื้อหาที่ระบุไว้ใน Spec:**
  - **User Stories (US-01 ถึง US-05):** บันทึกรับ/จ่ายสินค้า, แจ้งเตือนสต็อกต่ำกว่าเกณฑ์, คำนวณมูลค่ารวมแยกตามหมวดหมู่, กำหนดเกณฑ์ threshold เฉพาะสินค้า, และระบบแจ้งเตือนหลายช่องทาง
  - **Acceptance Criteria (Given-When-Then):** ระบุเงื่อนไขการทำงานปกติและ Edge Cases ละเอียดครบถ้วน (เช่น กรณีสต็อกเท่ากับเกณฑ์พอดีต้องไม่ส่งการแจ้งเตือน)
  - **Functional & Non-Functional Requirements (FR/NFR):** กำหนด Data Integrity, Performance, Extensibility, และ Reliability

---

## 2. Class Diagram และ Sequence Diagram
- **Class Diagram:** [inventory-sdd/diagrams/class.md](inventory-sdd/diagrams/class.md) ([URL บน GitHub](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/inventory-sdd/diagrams/class.md))
  - แสดงความสัมพันธ์ของคลาสตามหลัก **SOLID Principles**
  - แสดงการประยุกต์ใช้ **Observer Pattern** (`StockObserver`, `EmailNotifier`, `SMSNotifier`) และ **Factory Pattern** (`NotifierFactory`)
- **Sequence Diagram:** [inventory-sdd/diagrams/sequence.md](inventory-sdd/diagrams/sequence.md) ([URL บน GitHub](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/inventory-sdd/diagrams/sequence.md))
  - แสดงลำดับขั้นตอนตั้งแต่พนักงานตัดสต็อก (`InventoryService.issue`) การตรวจสอบเงื่อนไขสต็อกต่ำ จนถึงการกระจายแจ้งเตือนไปยัง Observers แบบ Concurrent/Decoupled
- **การวิเคราะห์การออกแบบ SOLID:** [inventory-sdd/design_review.md](inventory-sdd/design_review.md) ([URL บน GitHub](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/inventory-sdd/design_review.md))

---

## 3. งานฝั่งผู้ใช้ (Persona, Wireframe และผลตรวจ Accessibility)
- **Persona & User Journey Map:** [lab04-ai-coding-ux/persona.md](lab04-ai-coding-ux/persona.md) ([URL บน GitHub](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/lab04-ai-coding-ux/persona.md))
  - Persona "สมชาย รักษาคลัง" พนักงานคลังสินค้าวัย 32 ปี ทักษะไอทีระดับ 2/5
  - Journey Map 5 ขั้นตอน (เปิดระบบ, หาเมนู, กรอกข้อมูล, บันทึก, ตรวจผล) พร้อม Pain Points และวิธีแก้
- **Text Wireframe (ASCII Layout):** [lab04-ai-coding-ux/assets/wireframe-ai.md](lab04-ai-coding-ux/assets/wireframe-ai.md) ([URL บน GitHub](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/lab04-ai-coding-ux/assets/wireframe-ai.md))
  - โครงสร้าง 3 หน้าจอ: หน้า Login, Dashboard สรุปสถานะคลัง, และหน้าฟอร์ม Add Product
- **UI Mockup File:** [lab04-ai-coding-ux/assets/inventory_mockups.drawio](lab04-ai-coding-ux/assets/inventory_mockups.drawio) ([URL บน GitHub](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/lab04-ai-coding-ux/assets/inventory_mockups.drawio)) และ [mockup-link.txt](lab04-ai-coding-ux/assets/mockup-link.txt)
- **Accessibility & Usability Review (WCAG 2.1 AA):** [lab04-ai-coding-ux/accessibility-review.md](lab04-ai-coding-ux/accessibility-review.md) ([URL บน GitHub](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/lab04-ai-coding-ux/accessibility-review.md))
  - ตารางประเมิน 7 เกณฑ์ตามมาตรฐาน WCAG 2.1 ระดับ AA (Color Contrast 16.1:1, Persistent Labels, Error Indicators)
  - วิเคราะห์จุดบกพร่องที่ AI ทำพลาดและมนุษย์เป็นผู้ตรวจพบและแก้ไข 3 จุด (Vanishing Labels, Color Alone Status, Vague Errors)

---

## 4. Test อัตโนมัติ และหน้าผลการรัน CI
- **ชุด Automated Tests ในระบบ:**
  - **Unit Tests & Edge Cases (Lab 5):** [tests/test_inventory.py](tests/test_inventory.py) ([URL บน GitHub](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/tests/test_inventory.py)) — 15 Tests (TDD low_stock_items, sell)
  - **Characterization Tests (Lab 5):** [tests/test_pricing_legacy.py](tests/test_pricing_legacy.py) ([URL บน GitHub](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/tests/test_pricing_legacy.py)) — 24 Tests ครอบคลุม Legacy และ Refactored 100%
  - **Lab 3 Tests:** [inventory-sdd/tests/test_inventory.py](inventory-sdd/tests/test_inventory.py) ([URL บน GitHub](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/inventory-sdd/tests/test_inventory.py)) — 9 Tests
  - **Lab 4 Tests:** [lab04-ai-coding-ux/tests/test_discount.py](lab04-ai-coding-ux/tests/test_discount.py) ([URL บน GitHub](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/lab04-ai-coding-ux/tests/test_discount.py)) — 6 Tests
  - **Lab 2 Tests:** [tests/test_lab02.py](tests/test_lab02.py) ([URL บน GitHub](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/tests/test_lab02.py)) — 7 Tests
- **หน้าผลการรัน GitHub Actions CI:**
  - **CI Pipeline Workflow:** [.github/workflows/ci.yml](.github/workflows/ci.yml) ([URL บน GitHub](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/.github/workflows/ci.yml))
  - **ภาพหน้าจอ CI เขียว (ผ่าน 100%):** [screenshots/ci-green.png](screenshots/ci-green.png) ([URL บน GitHub](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/screenshots/ci-green.png))
  - **ภาพหน้าจอ CI แดง (เมื่อจงใจใส่ Bug):** [screenshots/ci-red.png](screenshots/ci-red.png) ([URL บน GitHub](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/screenshots/ci-red.png))
  - **หน้าประวัติการรัน CI จริงบน GitHub Actions:** [GitHub Actions Runs Dashboard](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/actions)
  - **รายงาน Coverage:** [coverage-note.md](coverage-note.md) ([URL บน GitHub](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/coverage-note.md)) — Total Coverage **92.45%** (ผ่านเกณฑ์ >= 85%)

---

## 5. บันทึกการใช้ AI (AI Logs, Rules, Prompt Comparisons & Ethics)
- **AI Iteration Log (Spec-Driven Development):** [inventory-sdd/AI_ITERATION_LOG.md](inventory-sdd/AI_ITERATION_LOG.md) ([URL บน GitHub](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/inventory-sdd/AI_ITERATION_LOG.md))
  - บันทึก Prompts, การเปรียบเทียบโค้ดก่อน/หลัง Context, และรอบการแก้ไข Spec/Rules โดยไม่แก้โค้ดด้วยมือ
- **System Rules & Context Engine:** [inventory-sdd/.ai-rules.md](inventory-sdd/.ai-rules.md) ([URL บน GitHub](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/inventory-sdd/.ai-rules.md))
  - ไฟล์กฎกำกับ AI Agent เพื่อควบคุมสถาปัตยกรรม, SOLID และการป้องกันข้อผิดพลาด
- **Prompt เปรียบเทียบสั้น vs ละเอียด:** [lab04-ai-coding-ux/prompt-vs-context.md](lab04-ai-coding-ux/prompt-vs-context.md) ([URL บน GitHub](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/lab04-ai-coding-ux/prompt-vs-context.md))
  - วิเคราะห์ความแตกต่างของคุณภาพโค้ดที่ได้จาก Prompt สั้น และ Prompt ที่มี Context และ Persona ชัดเจน
- **Test Gap Analysis (จับผิด AI Test):** [test-gap.md](test-gap.md) ([URL บน GitHub](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/test-gap.md))
  - ตาราง 3 คอลัมน์เปรียบเทียบข้อบกพร่องของ Unit Test ที่ AI สร้างแบบตื้นเขิน กับ Hardened Tests ที่มนุษย์เพิ่มเข้าไป
- **รายงานจริยธรรม AI และแนวปฏิบัติ:** [ethics.md](ethics.md) ([URL บน GitHub](https://github.com/Phongsakhon870/swe-inventory-67332110095-6/blob/main/ethics.md))
  - วิเคราะห์จริยธรรม 4 มิติ (ลิขสิทธิ์, ความลับข้อมูล, ความรับผิดชอบต่อ Bug, การถดถอยของทักษะ) พร้อม Personal AI Guidelines
