# บันทึกการ Debug แบบมีหลักฐาน (Evidence-Based Debug Log - Lab 04)

เอกสารบันทึกกระบวนการแก้จุดบกพร่องในโมดูล `discount.py` โดยปฏิบัติตาม **5 ขั้นตอนการ Debug แบบมีหลักฐาน** (Reproduce -> Traceback -> Hypothesis -> Verification -> Root Cause & Fix) อย่างเคร่งครัด

---

## สรุปภาพรวมผลการทดสอบเริ่มต้น (Initial Test Run)
- **คำสั่งที่รัน:** `python -m pytest tests/test_discount.py -v`
- **ผลลัพธ์เริ่มต้น:** Failed 4 ข้อ, Passed 2 ข้อ จากทั้งหมด 6 ข้อ
  - ❌ `test_apply_discount_basic` (AssertionError: 99.9 == 90.0)
  - ✅ `test_apply_discount_zero` (Passed - ผ่านโดยบังเอิญเพราะส่วนลดเป็น 0)
  - ❌ `test_bulk_total` (AssertionError: 299.9 == 270.0)
  - ✅ `test_average_price` (Passed)
  - ❌ `test_average_price_empty` (ZeroDivisionError: division by zero)
  - ❌ `test_cheapest_n` (AssertionError: [20.0] == [10.0, 20.0])

---

## 🐞 จุดที่ 1: ฟังก์ชัน `apply_discount` และ `bulk_total`

### 1. Reproduce
- **คำสั่งที่รัน:** `python -m pytest tests/test_discount.py -k "test_apply_discount_basic or test_bulk_total" -v`
- **Assertion ที่ Fail:**
  ```text
  FAILED tests/test_discount.py::test_apply_discount_basic - assert 99.9 == 90.0
   where 99.9 = apply_discount(100.0, 10)
  FAILED tests/test_discount.py::test_bulk_total - assert 299.9 == 270.0
   where 299.9 = bulk_total([100.0, 100.0, 100.0], 10)
  ```

### 2. Traceback
- **ตำแหน่งข้อผิดพลาด:** `discount.py` บรรทัดที่ 5
  ```python
  def apply_discount(price: float, percent: float) -> float:
      return price - percent / 100
  ```

### 3. สมมติฐาน (Hypothesis)
สูตรการคำนวณส่วนลดผิดพลาดเนื่องจากลำดับการคำนวณและตัวดำเนินการทางคณิตศาสตร์ไม่ถูกต้อง โดยโค้ดเขียน `price - (percent / 100)` ซึ่งเป็นการนำเปอร์เซ็นต์มาหารด้วย 100 แล้วนำไปลบออกจากราคาตรงๆ แทนที่จะนำสัดส่วนส่วนลดไปคูณกับราคาเดิมก่อนนำไปลบออก (`price - (price * percent / 100)`) ทำให้เมื่อลด 10% จาก 100 บาท ระบบคิดเป็น `100 - (10/100) = 100 - 0.1 = 99.9` บาท

### 4. การยืนยัน (Verification)
ทดสอบพิมพ์ค่าใน Interactive Terminal:
```python
>>> price = 100.0
>>> percent = 10
>>> print(price - percent / 100)
99.9
>>> print(price * (1 - percent / 100))
90.0
```
พบว่าค่าที่ถูกต้องตามหลักเศรษฐศาสตร์และการค้าคือ `price * (1.0 - percent / 100.0)` และยังพบว่า `test_apply_discount_zero` ผ่านก่อนหน้านี้เพราะเมื่อ `percent = 0` เทอม `0 / 100 = 0` ทำให้ `price - 0 = price` ซึ่งเป็นการผ่านโดยบังเอิญ (Trap of False Positive)

### 5. Root Cause และการแก้ (Fix)
- **Root Cause:** สูตรคำนวณส่วนลดขาดการคูณด้วยฐานราคา (`price`) ส่งผลให้หักมูลค่าเพียงเศษสตางค์ (`percent/100`) แทนที่จะหักเปอร์เซ็นต์ของราคาจริง
- **การแก้ไข:** แก้ไขบรรทัดที่ 5 ใน `discount.py`:
  ```python
  def apply_discount(price: float, percent: float) -> float:
      """ลดราคาตาม percent (0-100) คืนราคาหลังลด"""
      if percent < 0 or percent > 100:
          raise ValueError("เปอร์เซ็นต์ส่วนลดต้องอยู่ระหว่าง 0 ถึง 100")
      return price * (1.0 - percent / 100.0)
  ```
- **ผลลัพธ์หลังแก้:** ทั้ง `test_apply_discount_basic` และ `test_bulk_total` ผ่าน 100%

---

## 🐞 จุดที่ 2: ฟังก์ชัน `average_price` กรณีรายการสินค้าว่างเปล่า

### 1. Reproduce
- **คำสั่งที่รัน:** `python -m pytest tests/test_discount.py -k "test_average_price_empty" -v`
- **Assertion / Exception ที่ Fail:**
  ```text
  FAILED tests/test_discount.py::test_average_price_empty - ZeroDivisionError: division by zero
  ```

### 2. Traceback
- **ตำแหน่งข้อผิดพลาด:** `discount.py` บรรทัดที่ 18 ใน `average_price()`
  ```python
  def average_price(prices: list) -> float:
      return sum(prices) / len(prices)
  ```
  โยน `ZeroDivisionError: division by zero`

### 3. สมมติฐาน (Hypothesis)
ฟังก์ชัน `average_price` ไม่มีการตรวจสอบความถูกต้องของอินพุตกรณีลิสต์ว่างเปล่า (`len(prices) == 0`) ทำให้ตัวหารในสมการหาค่าเฉลี่ยเป็นศูนย์ ซึ่งผิดหลักคณิตศาสตร์และขัดกับข้อกำหนดการทดสอบที่ระบุว่าหากคลังว่างเปล่าต้องคืนค่า `0.0` ไม่ใช่เกิดข้อผิดพลาดรุนแรง (Crash)

### 4. การยืนยัน (Verification)
ทดสอบจำลองค่าเมื่อส่งลิสต์ว่าง `[]`:
```python
>>> prices = []
>>> len(prices)
0
>>> sum(prices) / len(prices)
Traceback (most recent call last):
  ...
ZeroDivisionError: division by zero
```
ยืนยันว่าเกิดจากไม่มี Guard Clause ดักจับลิสต์ว่าง

### 5. Root Cause และการแก้ (Fix)
- **Root Cause:** ขาด Guard Clause สำหรับจัดการกรณีลิสต์ว่าง (`empty list`) ส่งผลให้เกิดการหารด้วยศูนย์เมื่อคำนวณค่าเฉลี่ย
- **การแก้ไข:** เพิ่มการตรวจสอบขนาดของลิสต์ก่อนคำนวณ:
  ```python
  def average_price(prices: list) -> float:
      """คืนราคาเฉลี่ยของรายการสินค้า (คืน 0.0 หากไม่มีสินค้า)"""
      if not prices:
          return 0.0
      return sum(prices) / len(prices)
  ```
- **ผลลัพธ์หลังแก้:** `test_average_price_empty` ผ่านการทดสอบเรียบร้อย

---

## 🐞 จุดที่ 3: ฟังก์ชัน `cheapest_n` การตัดช่วงข้อมูลผิด (Off-by-One / Slicing Bug)

### 1. Reproduce
- **คำสั่งที่รัน:** `python -m pytest tests/test_discount.py -k "test_cheapest_n" -v`
- **Assertion ที่ Fail:**
  ```text
  FAILED tests/test_discount.py::test_cheapest_n - assert [20.0] == [10.0, 20.0]
  At index 0 diff: 20.0 != 10.0
  Right contains one more item: 20.0
  ```

### 2. Traceback
- **ตำแหน่งข้อผิดพลาด:** `discount.py` บรรทัดที่ 24 ใน `cheapest_n()`
  ```python
  def cheapest_n(prices: list, n: int) -> list:
      ordered = sorted(prices)
      return ordered[1:n]
  ```

### 3. สมมติฐาน (Hypothesis)
การตัดช่วงข้อมูล (List Slicing) ของภาษา Python เริ่มต้นนับตำแหน่งดัชนี (Index) จาก 0 แต่โค้ดกลับระบุ `ordered[1:n]` ซึ่งส่งผลกระทบ 2 ประการ:
1. ตำแหน่งที่ 0 ซึ่งเป็นสินค้าที่ราคาถูกที่สุดจริง ถูกตัดทิ้งไป
2. ช่วงข้อมูลที่คืนกลับมามีขนาดเพียง `n - 1` ตัว แทนที่จะเป็น `n` ตัว

### 4. การยืนยัน (Verification)
ทดสอบใน Interactive Python:
```python
>>> prices = [50.0, 10.0, 30.0, 20.0]
>>> ordered = sorted(prices)
>>> print(ordered)
[10.0, 20.0, 30.0, 50.0]
>>> print(ordered[1:2])
[20.0]  # ขาด 10.0 ตัวแรกไป และคืนมาแค่ 1 ตัว
>>> print(ordered[:2])
[10.0, 20.0]  # ถูกต้องสมบูรณ์
```
ยืนยันว่าต้นเหตุคือการใส่ดัชนีเริ่มต้นเป็น 1 แทนที่จะเป็น 0 (หรือ `:n`)

### 5. Root Cause และการแก้ (Fix)
- **Root Cause:** Off-by-one Indexing Slicing Error โดยเริ่ม Slice ที่ Index 1 ทำให้สินค้าที่ถูกที่สุดตัวแรก (`Index 0`) หายไป และได้จำนวนสมาชิกไม่ครบ `n`
- **การแก้ไข:** ปรับปรุงการ Slice ให้อ่านตั้งแต่สมาชิกตัวแรก `ordered[:n]` พร้อมรองรับกรณี `n <= 0`:
  ```python
  def cheapest_n(prices: list, n: int) -> list:
      """คืน n รายการที่ราคาถูกที่สุด เรียงจากถูกไปแพง"""
      if n <= 0 or not prices:
          return []
      ordered = sorted(prices)
      return ordered[:n]
  ```
- **ผลลัพธ์หลังแก้:** `test_cheapest_n` ผ่านการทดสอบสมบูรณ์

---

## 3. ผลการทดสอบรอบสุดท้ายหลังการแก้ไข (Final Verification)
รันคำสั่งทดสอบทั้งชุด:
```bash
python -m pytest tests/test_discount.py -v
```
ผลลัพธ์:
```text
============================= test session starts =============================
platform win32 -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Kaopan\Desktop\Inventory Management System\lab04-ai-coding-ux
collected 6 items

tests/test_discount.py::test_apply_discount_basic PASSED                 [ 16%]
tests/test_discount.py::test_apply_discount_zero PASSED                  [ 33%]
tests/test_discount.py::test_bulk_total PASSED                           [ 50%]
tests/test_discount.py::test_average_price PASSED                        [ 66%]
tests/test_discount.py::test_average_price_empty PASSED                  [ 83%]
tests/test_discount.py::test_cheapest_n PASSED                           [100%]

============================== 6 passed in 0.02s ==============================
```
**ทุกฟังก์ชันทำงานถูกต้องและผ่านการทดสอบ 100%**
