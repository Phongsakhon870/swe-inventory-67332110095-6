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
