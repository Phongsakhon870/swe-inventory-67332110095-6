# Sequence Diagram: จ่ายสินค้าจนสต็อกต่ำกว่า Threshold

ไดอะแกรมลำดับการทำงาน (Sequence Diagram) แสดงการทำงานเมื่อพนักงานบันทึกจ่ายสินค้าออกจากคลัง (`InventoryService.issue()`) จนส่งผลให้สต็อกสินค้าคงเหลือต่ำกว่าเกณฑ์ (`< threshold`) และระบบกระจายเหตุการณ์ไปยัง Observers เพื่อส่งข้อความแจ้งเตือน

```mermaid
sequenceDiagram
    autonumber
    actor Staff as พนักงานคลังสินค้า
    participant Service as InventoryService
    participant Product as Product
    participant Txn as StockTransaction
    participant Email as EmailNotifier (Observer)
    participant SMS as SMSNotifier (Observer)

    Staff->>Service: issue("PROD-01", 8)
    activate Service

    Service->>Product: quantity (ตรวจสอบจำนวนคงเหลือ)
    activate Product
    Product-->>Service: คืนค่าคงเหลือ (เช่น 20)
    deactivate Product

    Note over Service, Product: สต็อกพอจ่าย (20 >= 8) -> ดำเนินการตัดสต็อก

    Service->>Product: quantity -= 8 (คงเหลือ 12)
    activate Product
    Product-->>Service: อัปเดตสำเร็จ
    deactivate Product

    Service->>Txn: สร้างประวัติรายการจ่าย (ISSUE, 8, balance=12)
    activate Txn
    Txn-->>Service: บันทึกสำเร็จ
    deactivate Txn

    Service->>Product: is_low_stock()
    activate Product
    Note over Product: ตรวจสอบ 12 < 15 (Threshold) -> True
    Product-->>Service: True
    deactivate Product

    Note over Service: สต็อกต่ำกว่าเกณฑ์! -> เรียก Observers ทั้งหมด

    par กระจายการแจ้งเตือนไปยัง Email Observer
        Service->>Email: on_low_stock(product)
        activate Email
        Email->>Email: send(recipient, message)
        Note over Email: แสดงผล: [Email] ถึง manager@shop.com: ...
        Email-->>Service: ส่งสำเร็จ
        deactivate Email
    and กระจายการแจ้งเตือนไปยัง SMS Observer
        Service->>SMS: on_low_stock(product)
        activate SMS
        SMS->>SMS: send(recipient, message)
        Note over SMS: แสดงผล: [SMS] ถึง 0812345678: ...
        SMS-->>Service: ส่งสำเร็จ
        deactivate SMS
    end

    Service-->>Staff: คืนค่า True (จ่ายสินค้าสำเร็จและแจ้งเตือนเรียบร้อย)
    deactivate Service
```
