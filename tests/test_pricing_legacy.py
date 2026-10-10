"""
Characterization Tests สำหรับ pricing_legacy.py และ pricing.py (ขั้นที่ 7 และ 8)
บันทึกและพิสูจน์ว่าโมดูลทั้งสองเวอร์ชันให้ผลลัพธ์ตรงกันทุกกรณี 100%
"""

import datetime

import pytest

import pricing as p_refactored
import pricing_legacy as p_legacy


@pytest.fixture(params=[p_legacy, p_refactored], ids=["legacy", "refactored"])
def pl(request):
    """Fixture รันชุดทดสอบกับทั้ง pricing_legacy และ pricing เพื่อพิสูจน์ความเข้ากันได้"""
    mod = request.param
    mod.member_points.clear()
    mod.LOG.clear()
    yield mod
    mod.member_points.clear()
    mod.LOG.clear()


# =============================================================
# 1. กลุ่มราคาปกติ (Normal Price)
# =============================================================
def test_pricing_normal(pl):
    """สินค้า 1 รายการ จำนวนน้อย ไม่ใช้สิทธิ์สมาชิกหรือคูปอง (บวกภาษี 7%)"""
    items = [("สมุด", 2, 100.0)]
    result = pl.calc(items)
    # 2 * 100 = 200, 200 + 7% tax = 214.0
    assert result == 214.0


# =============================================================
# 2. กลุ่มซื้อจำนวนมาก (Bulk Discount Thresholds)
# =============================================================
def test_pricing_bulk_threshold_50(pl):
    """สินค้าจำนวน 50 ชิ้นพอดี -> ได้รับส่วนลด 5% ก่อนบวกภาษี"""
    items = [("ปากกา", 50, 10.0)]
    result = pl.calc(items)
    # 50 * 10 = 500, ลด 5% = 475.0, 475 * 1.07 = 508.25
    assert result == 508.25


def test_pricing_bulk_threshold_100(pl):
    """สินค้าจำนวน 100 ชิ้นพอดี -> ได้รับส่วนลด 10% ก่อนบวกภาษี"""
    items = [("ดินสอ", 100, 10.0)]
    result = pl.calc(items)
    # 100 * 10 = 1000, ลด 10% = 900.0, 900 * 1.07 = 963.0
    assert result == 963.0


# =============================================================
# 3. กลุ่มจำนวนเป็นศูนย์หรือติดลบ (Zero/Negative Quantity)
# =============================================================
def test_pricing_zero_and_negative_quantity(pl):
    """สินค้าที่จำนวน 0 หรือติดลบ -> ข้ามการคิดราคา ยอดเป็น 0"""
    items = [("ยางลบ", 0, 50.0), ("ไม้บรรทัด", -2, 20.0)]
    result = pl.calc(items)
    assert result == 0.0


# =============================================================
# 4. กลุ่มสมาชิกและแต้มสะสม (Member Discount & Loyalty Points)
# =============================================================
def test_pricing_member_discount_and_points_accumulation(pl):
    """สมาชิกได้รับส่วนลด 5% และสะสมแต้ม 1 แต้มต่อทุก 100 บาท (คิดก่อนภาษี)"""
    items = [("กระเป๋า", 2, 100.0)]
    result = pl.calc(items, member="somchai")
    # 200 * 0.95 = 190.0, 190 + 7% tax = 203.3
    assert result == 203.3
    # แต้มสะสม: int(190 / 100) = 1 แต้ม
    assert pl.member_points["somchai"] == 1

    # ซื้อครั้งที่สอง แต้มต้องสะสมต่อเนื่อง
    result2 = pl.calc(items, member="somchai")
    assert result2 == 203.3
    assert pl.member_points["somchai"] == 2


# =============================================================
# 5. กลุ่มคูปองส่วนลด (Coupons: SAVE50, HALF, NEWYEAR)
# =============================================================
def test_pricing_coupon_save50(pl):
    """คูปอง SAVE50 -> ลด 50 บาทจากยอดรวมก่อนภาษี"""
    items = [("แฟ้มเอกสาร", 2, 100.0)]
    result = pl.calc(items, coupon="SAVE50")
    # 200 - 50 = 150.0, 150 * 1.07 = 160.5
    assert result == 160.5


def test_pricing_coupon_half(pl):
    """คูปอง HALF -> ลด 50% จากยอดรวมก่อนภาษี"""
    items = [("กล่องดินสอ", 2, 100.0)]
    result = pl.calc(items, coupon="HALF")
    # 200 * 0.5 = 100.0, 100 * 1.07 = 107.0
    assert result == 107.0


def test_pricing_coupon_newyear_in_january(pl):
    """คูปอง NEWYEAR ใช้ในเดือนมกราคม -> ได้รับส่วนลด 20% (คูณ 0.8)"""
    items = [("ชุดเครื่องเขียน", 2, 100.0)]
    jan_date = datetime.date(2026, 1, 20)
    result = pl.calc(items, coupon="NEWYEAR", today=jan_date)
    # 200 * 0.8 = 160.0, 160 * 1.07 = 171.2
    assert result == 171.2


def test_pricing_coupon_newyear_outside_january(pl):
    """คูปอง NEWYEAR ใช้นอกเดือนมกราคม -> ไม่ได้รับส่วนลด (คิดราคาปกติ)"""
    items = [("ชุดเครื่องเขียน", 2, 100.0)]
    feb_date = datetime.date(2026, 2, 10)
    result = pl.calc(items, coupon="NEWYEAR", today=feb_date)
    # 200 (ไม่ลด), 200 * 1.07 = 214.0
    assert result == 214.0


def test_pricing_coupon_newyear_default_today(pl):
    """คูปอง NEWYEAR เมื่อไม่ระบุวันที่ -> ดึง datetime.date.today() อัตโนมัติ"""
    items = [("ชุดเครื่องเขียน", 2, 100.0)]
    result = pl.calc(items, coupon="NEWYEAR")
    current_month = datetime.date.today().month
    expected = 171.2 if current_month == 1 else 214.0
    assert result == expected



# =============================================================
# 6. กลุ่มยอดติดลบ (Negative Subtotal Cap)
# =============================================================
def test_pricing_coupon_discount_exceeding_subtotal_caps_at_zero(pl):
    """ส่วนลดคูปองมากกว่าราคาสินค้า -> ปรับยอดเป็น 0 ไม่ให้ยอดติดลบ"""
    items = [("ยางลบ", 1, 20.0)]
    result = pl.calc(items, coupon="SAVE50")
    # 20 - 50 = -30 -> t = 0 -> 0 + 0*TAX = 0.0
    assert result == 0.0


# =============================================================
# 7. กลุ่มค่าที่ฟังก์ชันเก็บไว้ (State & Side Effects)
# =============================================================
def test_pricing_log_and_member_points_side_effects(pl):
    """ฟังก์ชันต้องบันทึกประวัติลงใน LOG tuple (member, final_price) ทุกครั้ง"""
    items = [("ปากกาเจล", 1, 100.0)]
    result = pl.calc(items, member="wichai")
    assert result == 101.65
    assert len(pl.LOG) == 1
    assert pl.LOG[0] == ("wichai", 101.65)
