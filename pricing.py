"""
pricing.py - โมดูลคำนวณราคาและส่วนลดระบบ Inventory (เวอร์ชัน Refactored - ขั้นที่ 8)
ปรับโครงสร้างให้อ่านง่าย แยกหน้าที่ตาม Single Responsibility และกำจัด Magic Literals
โดยคงพฤติกรรมเดิมไว้ครบถ้วน 100% ตามผลการทดสอบ Characterization Tests
"""

import datetime
from collections.abc import Sequence

# -----------------------------------------------------------------------------
# กำหนดค่าคงที่ (Named Constants) แทน Magic Literals
# -----------------------------------------------------------------------------
DEFAULT_TAX_RATE: float = 0.07
POINTS_REWARD_RATE: int = 100  # 1 แต้มต่อยอดซื้อทุก 100 บาท

# ส่วนลดตามปริมาณการซื้อ (Bulk Discounts)
BULK_TIER_LARGE_QTY: int = 100
BULK_TIER_LARGE_FACTOR: float = 0.90  # ลด 10%
BULK_TIER_MEDIUM_QTY: int = 50
BULK_TIER_MEDIUM_FACTOR: float = 0.95  # ลด 5%

# ส่วนลดสมาชิกและคูปอง
MEMBER_DISCOUNT_FACTOR: float = 0.95  # สมาชิกลด 5%
COUPON_SAVE50_DEDUCTION: float = 50.0  # ลด 50 บาท
COUPON_HALF_FACTOR: float = 0.50  # ลด 50%
COUPON_NEWYEAR_FACTOR: float = 0.80  # ลด 20% ในเดือนมกราคม
NEWYEAR_ELIGIBLE_MONTH: int = 1

# โครงสร้างสำหรับความเข้ากันได้ย้อนหลัง (Backward Compatibility State)
TAX: float = DEFAULT_TAX_RATE
member_points: dict[str, int] = {}
LOG: list[tuple[str | None, float]] = []


def _calculate_bulk_item_subtotal(quantity: int, unit_price: float) -> float:
    """คำนวณราคาย่อยของสินค้า 1 รายการ พร้อมปรับลดราคาตามเกณฑ์จำนวนซื้อ"""
    if quantity <= 0:
        return 0.0

    raw_subtotal = quantity * unit_price
    if quantity >= BULK_TIER_LARGE_QTY:
        return raw_subtotal * BULK_TIER_LARGE_FACTOR
    if quantity >= BULK_TIER_MEDIUM_QTY:
        return raw_subtotal * BULK_TIER_MEDIUM_FACTOR
    return raw_subtotal


def _apply_member_benefits(subtotal: float, member: str | None) -> float:
    """คำนวณส่วนลดสมาชิก 5% และสะสมแต้ม (1 แต้มต่อทุก 100 บาทก่อนภาษี)"""
    if member is None:
        return subtotal

    if member not in member_points:
        member_points[member] = 0

    discounted_subtotal = subtotal * MEMBER_DISCOUNT_FACTOR
    earned_points = int(discounted_subtotal / POINTS_REWARD_RATE)
    member_points[member] += earned_points

    return discounted_subtotal


def _apply_coupon_discount(
    subtotal: float, coupon: str | None, today: datetime.date | None
) -> float:
    """ประมวลผลคูปองส่วนลดตามเงื่อนไข (SAVE50, HALF, NEWYEAR)"""
    if coupon is None:
        return subtotal

    coupon_code = coupon.strip().upper()
    current_date = today if today is not None else datetime.date.today()

    if coupon_code == "SAVE50":
        subtotal -= COUPON_SAVE50_DEDUCTION
    elif coupon_code == "HALF":
        subtotal *= COUPON_HALF_FACTOR
    elif coupon_code == "NEWYEAR" and current_date.month == NEWYEAR_ELIGIBLE_MONTH:
        subtotal *= COUPON_NEWYEAR_FACTOR

    return max(0.0, subtotal)


def _calculate_tax_and_round(amount: float, tax_rate: float = DEFAULT_TAX_RATE) -> float:
    """คิดภาษีมูลค่าเพิ่มและปัดเศษทศนิยม 2 ตำแหน่ง"""
    total_with_tax = amount + (amount * tax_rate)
    return round(total_with_tax, 2)


def calc(
    items: Sequence[tuple[str, int, float]],
    member: str | None = None,
    coupon: str | None = None,
    today: datetime.date | None = None,
) -> float:
    """
    คำนวณราคาสินค้ารวม ส่วนลดสมาชิก ส่วนลดคูปอง ภาษี และบันทึกประวัติ

    Args:
        items: ลิสต์ของ tuple (ชื่อสินค้า, จำนวน, ราคาต่อหน่วย)
        member: ชื่อสมาชิก (หากมี)
        coupon: รหัสคูปองส่วนลด (หากมี)
        today: วันที่ทำรายการ (หากไม่ระบุจะใช้วันที่ปัจจุบัน)

    Returns:
        ยอดเงินสุทธิที่ต้องชำระ (ปัดเศษทศนิยม 2 ตำแหน่ง)
    """
    # 1. คำนวณราคารวมสินค้าทุกรายการ (พร้อมส่วนลดซื้อเยอะ)
    subtotal = sum(_calculate_bulk_item_subtotal(qty, price) for _, qty, price in items)

    # 2. คำนวณส่วนลดสมาชิกและสะสมแต้ม
    subtotal = _apply_member_benefits(subtotal, member)

    # 3. คำนวณส่วนลดคูปอง (พร้อมป้องกันยอดติดลบ)
    subtotal = _apply_coupon_discount(subtotal, coupon, today)

    # 4. คิดภาษีและปัดเศษ
    final_total = _calculate_tax_and_round(subtotal, TAX)

    # 5. บันทึกประวัติการคำนวณลง LOG
    LOG.append((member, final_total))

    return final_total
