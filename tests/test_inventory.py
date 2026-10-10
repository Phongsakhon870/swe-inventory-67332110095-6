import tempfile
from pathlib import Path

import pytest

from inventory import Inventory


@pytest.fixture
def inv():
    with tempfile.TemporaryDirectory() as tmp_dir:
        data_file = Path(tmp_dir) / "test_inventory.json"
        inventory = Inventory(data_path=data_file)
        yield inventory


# =============================================================
# ขั้นที่ 2: TDD Phase: low_stock_items(threshold)
# =============================================================
def test_low_stock_all_above_threshold(inv):
    """กรณีที่ 1: สินค้าทุกรายการมีจำนวนมากกว่า threshold -> คืน list ว่าง"""
    inv.add_item("P01", "สมุด", 15, 20.0)
    inv.add_item("P02", "ปากกา", 20, 10.0)
    assert inv.low_stock_items(10) == []


def test_low_stock_exactly_equal_threshold(inv):
    """กรณีที่ 2: มีสินค้าที่จำนวนเท่ากับ threshold พอดี -> ต้องถูกนับรวมด้วย"""
    inv.add_item("P01", "ยางลบ", 5, 10.0)
    inv.add_item("P02", "ไม้บรรทัด", 12, 15.0)
    result = inv.low_stock_items(5)
    assert len(result) == 1
    assert result[0]["code"] == "P01"
    assert result[0]["quantity"] == 5


def test_low_stock_multiple_sorted_by_name(inv):
    """กรณีที่ 3: มีสินค้าเข้าเกณฑ์หลายรายการ -> ผลลัพธ์เรียงตามชื่อ ไม่ใช่ตามลำดับที่เพิ่ม"""
    inv.add_item("P03", "สมุดวาดภาพ", 2, 50.0)
    inv.add_item("P01", "กบเหลาดินสอ", 3, 15.0)
    inv.add_item("P02", "ดินสอดำ", 1, 5.0)
    result = inv.low_stock_items(5)
    assert len(result) == 3
    names = [item["name"] for item in result]
    assert names == sorted(names)
    assert names == ["กบเหลาดินสอ", "ดินสอดำ", "สมุดวาดภาพ"]


def test_low_stock_empty_inventory(inv):
    """กรณีที่ 4: คลังว่าง -> คืน list ว่าง ไม่ใช่ error"""
    assert inv.low_stock_items(10) == []


def test_low_stock_threshold_zero(inv):
    """กรณีที่ 5: threshold เป็น 0 -> คืนเฉพาะสินค้าที่เหลือ 0"""
    inv.add_item("P01", "สินค้าหมด", 0, 10.0)
    inv.add_item("P02", "สินค้ามีอยู่", 5, 20.0)
    result = inv.low_stock_items(0)
    assert len(result) == 1
    assert result[0]["code"] == "P01"
    assert result[0]["quantity"] == 0


def test_low_stock_negative_threshold(inv):
    """กรณีที่ 6: threshold ติดลบ -> คืน list ว่าง (เนื่องจากสต็อกในระบบไม่มีทางติดลบ)"""
    inv.add_item("P01", "ปากกา", 5, 10.0)
    assert inv.low_stock_items(-1) == []


# =============================================================
# ขั้นที่ 4: จับ test ที่ AI เขียนแล้วผ่านง่ายเกินไป (เมธอด sell)
# =============================================================
def test_sell_happy_path(inv):
    """กรณีที่ AI ให้มา: ขายสินค้าปกติ จำนวนคงเหลือลดลงถูกต้อง"""
    inv.add_item("P01", "สมุดรายงาน", 10, 25.0)
    result = inv.sell("P01", 3)
    assert result["quantity"] == 7
    assert inv.list_items()[0]["quantity"] == 7


def test_sell_exact_boundary_zero_remaining(inv):
    """กลุ่มค่าขอบ: ขายเท่ากับจำนวนที่เหลือทั้งหมดพอดี -> คงเหลือเป็น 0 ไม่ error"""
    inv.add_item("P02", "ดินสอกด", 5, 30.0)
    result = inv.sell("P02", 5)
    assert result["quantity"] == 0
    assert inv.list_items()[0]["quantity"] == 0


def test_sell_zero_and_negative_quantity_rejected(inv):
    """กลุ่มค่าที่ไม่ควรรับ: ขายจำนวน 0 หรือติดลบ -> โยน ValueError"""
    inv.add_item("P03", "ยางลบดินสอ", 10, 10.0)

    with pytest.raises(ValueError, match="มากกว่า 0"):
        inv.sell("P03", 0)

    with pytest.raises(ValueError, match="มากกว่า 0"):
        inv.sell("P03", -4)

    # ยอดคงเหลือต้องไม่เปลี่ยนแปลง
    assert inv.list_items()[0]["quantity"] == 10


def test_sell_exceeding_stock_rejected(inv):
    """กลุ่มค่าที่ไม่ควรรับ: ขายมากกว่าจำนวนคงเหลือ -> โยน ValueError ยอดคงเหลือไม่เปลี่ยน"""
    inv.add_item("P04", "ไม้โปรแทรกเตอร์", 8, 15.0)

    with pytest.raises(ValueError, match="จำนวนคงเหลือไม่พอ"):
        inv.sell("P04", 12)

    assert inv.list_items()[0]["quantity"] == 8


def test_sell_non_existent_item_raises_key_error(inv):
    """กลุ่มเส้นทาง Error: ขายสินค้าที่ไม่มีในคลัง -> โยน KeyError พร้อมระบุรหัสสินค้า"""
    with pytest.raises(KeyError, match="ไม่พบสินค้า"):
        inv.sell("NOT_FOUND", 2)


def test_sell_invalid_data_types_raises_type_error(inv):
    """กลุ่มชนิดข้อมูล: ส่งจำนวนเป็น float, str หรือ bool -> โยน TypeError"""
    inv.add_item("P05", "สีไม้ 24 สี", 10, 120.0)

    with pytest.raises(TypeError, match="integer"):
        inv.sell("P05", 2.5)

    with pytest.raises(TypeError, match="integer"):
        inv.sell("P05", "สาม")

    with pytest.raises(TypeError, match="integer"):
        inv.sell("P05", True)

    assert inv.list_items()[0]["quantity"] == 10


# =============================================================
# ขั้นที่ 5: เสริม Coverage สำหรับ Input Validation
# =============================================================
def test_add_item_empty_code_or_name_rejected(inv):
    """ทดสอบกรณีรหัสสินค้าหรือชื่อสินค้าว่างเปล่า -> โยน ValueError"""
    with pytest.raises(ValueError, match="ต้องไม่ว่างเปล่า"):
        inv.add_item("", "สมุด", 10, 20.0)

    with pytest.raises(ValueError, match="ต้องไม่ว่างเปล่า"):
        inv.add_item("P01", "   ", 10, 20.0)


def test_add_item_negative_initial_quantity_rejected(inv):
    """ทดสอบกรณีจำนวนสินค้าเริ่มต้นติดลบ -> โยน ValueError"""
    with pytest.raises(ValueError, match="ต้องไม่ติดลบ"):
        inv.add_item("P01", "สมุด", -5, 20.0)


def test_load_data_corrupted_json(tmp_path):
    """ทดสอบกรณีไฟล์ JSON เสียหาย (corrupted) -> โหลดคืน list ว่างโดยไม่ crash"""
    corrupt_file = tmp_path / "corrupt.json"
    corrupt_file.write_text("{ this is not valid json }", encoding="utf-8")
    inv = Inventory(data_path=corrupt_file)
    assert inv.list_items() == []


