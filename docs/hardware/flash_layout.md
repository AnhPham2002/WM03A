# Flash Memory Layout

## 1. Tổng quan

Tài liệu này mô tả cách phân chia bộ nhớ Flash trong vi điều khiển STM32L431RCT6 của thiết bị WM03A.

Flash được chia thành các vùng chức năng phục vụ Bootloader, lưu trữ firmware ứng dụng và quản lý quá trình cập nhật firmware qua OTA. Hệ thống áp dụng cơ chế **Dual-Slot**, gồm hai vùng lưu trữ firmware độc lập:

- **Slot A:** vùng lưu trữ firmware ứng dụng A.
- **Slot B:** vùng lưu trữ firmware ứng dụng B.

Tại một thời điểm, thiết bị chỉ thực thi firmware từ một slot. Khi cập nhật OTA, firmware mới được ghi vào slot còn lại, không ghi đè lên firmware đang chạy.

Địa chỉ các vùng nhớ được định nghĩa bằng macro trong file `flash_layout.h`.

## 2. Bản đồ bộ nhớ

### 2.1. Bảng phân vùng

| Vùng nhớ | Địa chỉ bắt đầu | Địa chỉ kết thúc | Kích thước | Macro |
|---|---:|---:|---:|---|
| Bootloader | `0x08000000` | `0x08007FEF` | 32 KB (32.768 bytes) | `BOOTLOADER_START_ADDR` |
| Slot A Metadata | `0x08008000` | `0x080087FF` | 2 KB (2.048 bytes) | `SLOT_A_METADATA_ADDR` |
| Slot A Firmware | `0x08008800` | `0x08023FFF` | 110 KB (112.640 bytes) | `SLOT_A_START_ADDR` |
| Slot B Metadata | `0x08024000` | `0x080247FF` | 2 KB (2.048 bytes) | `SLOT_B_METADATA_ADDR` |
| Slot B Firmware | `0x08024800` | `0x0803FFFF` | 110 KB (112.640 bytes) | `SLOT_B_START_ADDR` |

### 2.2. Sơ đồ phân vùng

```text
Flash STM32L431RCT6 (256 KB)

0x08000000  +----------------------------------+
            |   Bootloader (32 KB)             |
0x08008000  +----------------------------------+
            |   Slot A Metadata (2 KB)         |
0x08008800  +----------------------------------+
            |   Slot A Firmware (110 KB)       |
0x08024000  +----------------------------------+
            |   Slot B Metadata (2 KB)         |
0x08024800  +----------------------------------+
            |   Slot B Firmware (110 KB)       |
0x08040000  +----------------------------------+
```

### 2.3. Ghi chú về bố cục

- Tổng kích thước các vùng bằng 256 KB, tức toàn bộ Flash của STM32L431RCT6; không còn vùng trống.
- Mọi địa chỉ bắt đầu của các vùng Slot đều là bội số của 2 KB, là kích thước page Flash của dòng STM32L43x. Nhờ vậy mỗi vùng được xóa độc lập theo page mà không ảnh hưởng vùng bên cạnh.
- Mỗi vùng metadata dành 2 KB (một page) để có thể xóa và ghi lại riêng.

## 3. Bootloader

Bootloader nằm tại `0x08000000`, kích thước 32.768 bytes, và chịu trách nhiệm:

- Khởi tạo các thành phần cần thiết để kiểm tra trạng thái firmware.
- Đọc và kiểm tra metadata của Slot A và Slot B.
- Xác định slot được ưu tiên thực thi.
- Kiểm tra tính hợp lệ của firmware trước khi chuyển quyền điều khiển.
- Quản lý trạng thái firmware trong quá trình cập nhật OTA.

**Chú ý:** 16 bytes cuối của vùng Bootloader, tại địa chỉ `0x08007FF0` (`BOOTLOADER_VERSION_ADDR`) lưu phiên bản Bootloader, cho phép hệ thống hoặc công cụ bên ngoài nhận diện phiên bản đang cài trên thiết bị.

## 4. Cấu trúc Dual-Slot

Mỗi slot gồm một vùng Metadata và một vùng Firmware, có cùng kích thước và cấu trúc.

| Thành phần | Slot A | Slot B | Kích thước |
|---|---:|---:|---:|
| Metadata | `0x08008000` | `0x08024000` | 2 KB |
| Firmware | `0x08008800` | `0x08024800` | 110 KB |

**Metadata** lưu thông tin quản lý firmware của slot tương ứng, gồm Sequence, Firmware Version, Firmware Status, Firmware Size, Firmware CRC32 và số lượng packet đã tải xuống. Định dạng chi tiết của từng trường được mô tả trong tài liệu [OTA](../communication/ota.md).

**Nguyên tắc hoạt động:**

- Hai slot được dùng luân phiên. Firmware ứng dụng chỉ thực thi từ một slot, slot còn lại dùng để nhận firmware mới.
- Application Firmware đang chạy ghi firmware mới và metadata vào slot không chạy trong quá trình OTA.
- Khi MCU khởi động, Bootloader đọc metadata của cả hai slot và chọn firmware hợp lệ để thực thi.

Giao thức và quy trình cập nhật firmware được mô tả trong tài liệu [OTA](../communication/ota.md).

## 5. Tài liệu liên quan

- [Firmware Architecture](firmware_architecture.md)
- [Storage](storage.md)
- [OTA](../communication/ota.md)
- [Hardware Architecture](../hardware/hardware.md)