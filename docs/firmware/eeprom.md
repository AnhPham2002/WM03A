# Tài liệu lưu trữ EEPROM

## 1. Tổng quan

WM03A sử dụng EEPROM ngoài để lưu thông tin định danh thiết bị, cấu hình, trạng thái vận hành, dữ liệu công tơ và nhật ký sự kiện.

Không gian bộ nhớ được chia thành các vùng có địa chỉ bắt đầu và dung lượng cố định. Việc phân vùng giúp mỗi chức năng chỉ truy cập đúng vùng dữ liệu của mình, tránh ghi đè dữ liệu của chức năng khác.

| Thông số | Giá trị |
|---|---|
| EEPROM | M95M02-DRMN6TP |
| Giao tiếp | SPI |
| Dung lượng | 256 KB (262.144 B) |
| Kích thước trang | 256 B |
| Phạm vi địa chỉ | `0x00000` – `0x3FFFF` |
| Magic number | `0x02468ACE` (`EEPROM_MAGIC_NUMBER`) |
| Phiên bản layout | `V1.0.0` (`EEPROM_LAYOUT_VERSION`) |

Phiên bản layout độc lập với phiên bản firmware (`FIRMWARE_VERSION`, hiện là `V1.0.1`). Layout chỉ thay đổi khi cấu trúc bố trí dữ liệu thay đổi.

## 2. Bản đồ bộ nhớ

EEPROM được chia thành các vùng liên tiếp theo thứ tự địa chỉ. Địa chỉ bắt đầu và dung lượng của mỗi vùng được xác định bằng macro trong file `eeprom_layout.h`.

```text
EEPROM M95M02-DRMN6TP (256 KB)

0x00000  +----------------------------------------------+
         |   Header (16 B)                              |
0x00010  +----------------------------------------------+
         |   Device Serial (12 B)                       |
0x0001C  +----------------------------------------------+
         |   Device Activation Status (4 B)             |
0x00020  +----------------------------------------------+
         |   Device Password (256 B)                    |
0x00120  +----------------------------------------------+
         |   Metadata (256 B)       [4 khu vực x 64 B]  |
0x00220  +----------------------------------------------+
         |   Runtime Data (320 B)   [4 khu vực x 80 B]  |
0x00360  +----------------------------------------------+
         |   IP Endpoint Configuration (24 B)           |
0x00378  +----------------------------------------------+
         |   Module Configuration (12 B)                |
0x00384  +----------------------------------------------+
         |   Charge Configuration (12 B)                |
0x00390  +----------------------------------------------+
         |   Pulse Meter Configuration (120 B)          |
0x00408  +----------------------------------------------+
         |   Modbus Meter Configuration (200 B)         |
0x004D0  +----------------------------------------------+
         |   Pressure Sensor Configuration (80 B)       |
0x00520  +----------------------------------------------+
         |   Latch (150.000 B)           [circular]     |
0x24F10  +----------------------------------------------+
         |   Event (12.000 B)            [circular]     |
0x27DF0  +----------------------------------------------+
         |   Push Status (20.000 B)      [circular]     |
0x2CC10  +----------------------------------------------+
         |   Changed Info Log (14.000 B) [circular]     |
0x302C0  +----------------------------------------------+
         |   Chưa phân bổ (64.832 B)                    |
0x40000  +----------------------------------------------+
```

| Vùng | Macro địa chỉ | Bắt đầu | Kết thúc | Kích thước (B) | Mục đích |
|---|---|---|---|---:|---|
| Header | `EEPROM_HEADER_ADDRESS` | `0x00000` | `0x0000F` | 16 | Nhận diện EEPROM và phiên bản layout |
| Device Serial | `EEPROM_DEVICE_SERIAL_ADDRESS` | `0x00010` | `0x0001B` | 12 | Số serial thiết bị (`uint64_t`) |
| Device Activation Status | `EEPROM_DEVICE_ACTIVATION_STATUS_ADDRESS` | `0x0001C` | `0x0001F` | 4 | Trạng thái kích hoạt |
| Device Password | `EEPROM_DEVICE_PASSWORD_ADDRESS` | `0x00020` | `0x0011F` | 256 | Bản ghi mật khẩu của 3 cấp (mục [3.3](#33-bản-ghi-mật-khẩu-và-chuỗi-kiểm-tra)) |
| Metadata | `EEPROM_METADATA_ADDRESS` | `0x00120` | `0x0021F` | 256 | Chỉ số bộ đệm vòng, 4 khu vực (mục [3.2](#32-cấu-trúc-dữ-liệu-và-lưu-luân-phiên-rotating-slots)) |
| Runtime Data | `EEPROM_RUNTIME_DATA_ADDRESS` | `0x00220` | `0x0035F` | 320 | Dữ liệu vận hành, 4 khu vực (mục [3.2](#32-cấu-trúc-dữ-liệu-và-lưu-luân-phiên-rotating-slots)) |
| IP Endpoint Configuration | `EEPROM_IP_ENDPOINT_ADDRESS` | `0x00360` | `0x00377` | 24 | Cấu hình IP và cổng máy chủ |
| Module Configuration | `EEPROM_MODULE_CONFIG_ADDRESS` | `0x00378` | `0x00383` | 12 | Chu kỳ chốt, chu kỳ gửi, múi giờ |
| Charge Configuration | `EEPROM_CHARGE_CONFIG_ADDRESS` | `0x00384` | `0x0038F` | 12 | Cấu hình bộ sạc |
| Pulse Meter Configuration | `EEPROM_PULSE_METER_CONFIG_ADDRESS` | `0x00390` | `0x00407` | 120 | Cấu hình đồng hồ xung |
| Modbus Meter Configuration | `EEPROM_MODBUS_METER_CONFIG_ADDRESS` | `0x00408` | `0x004CF` | 200 | Cấu hình đồng hồ Modbus RTU |
| Pressure Sensor Configuration | `EEPROM_PRESSURE_SENSOR_CONFIG_ADDRESS` | `0x004D0` | `0x0051F` | 80 | Cấu hình cảm biến áp suất |
| Latch | `EEPROM_LATCH_ADDRESS` | `0x00520` | `0x24F0F` | 150.000 | Bản ghi chốt, bộ đệm vòng (mục [3.4](#34-bộ-đệm-vòng-circular-buffer)) |
| Event | `EEPROM_EVENT_ADDRESS` | `0x24F10` | `0x27DEF` | 12.000 | Bản ghi sự kiện, bộ đệm vòng (mục [3.4](#34-bộ-đệm-vòng-circular-buffer)) |
| Push Status | `EEPROM_PUSH_STATUS_ADDRESS` | `0x27DF0` | `0x2CC0F` | 20.000 | Trạng thái gửi dữ liệu, bộ đệm vòng (mục [3.4](#34-bộ-đệm-vòng-circular-buffer)) |
| Changed Info Log | `EEPROM_CHANGED_INFO_LOG_ADDRESS` | `0x2CC10` | `0x302BF` | 14.000 | Lịch sử thay đổi cấu hình, bộ đệm vòng (mục [3.4](#34-bộ-đệm-vòng-circular-buffer)) |
| Chưa phân bổ | — | `0x302C0` | `0x3FFFF` | 64.832 | Dự phòng mở rộng |

Vùng cấu hình (từ IP Endpoint đến Pressure Sensor) có kích thước cố định. Các vùng có `_Static_assert` kiểm tra tổng dung lượng.

Tất cả địa chỉ bắt đầu và dung lượng của các vùng trên đều là bội số của 4 byte, phù hợp với quy định căn chỉnh ở mục [3.1](#31-căn-chỉnh-theo-nhóm-4-byte-ecc).

## 3. Bảo vệ dữ liệu và kéo dài tuổi thọ EEPROM

### 3.1. Căn chỉnh theo nhóm 4 byte (ECC)

EEPROM M95M02-D tích hợp cơ chế ECC ở mức phần cứng, áp dụng cho từng nhóm 4 byte liên tiếp (địa chỉ `4N` đến `4N + 3`). Chi tiết khả năng sửa lỗi và giới hạn chu kỳ ghi/xóa theo nhóm xem trong datasheet M95M02-D.

Khi thiết kế firmware:

- Dù có thể ghi riêng từng byte, mỗi thao tác ghi vẫn tính vào số chu kỳ ghi/xóa của cả nhóm 4 byte chứa byte đó.
- Mỗi vùng dữ liệu nên có địa chỉ bắt đầu và kích thước căn theo bội số của 4 byte, để dữ liệu của hai vùng khác nhau không dùng chung một nhóm.
- Firmware dùng macro `ALIGN4()` (định nghĩa trong `app_storage.h`) để căn kích thước gói dữ liệu theo bội số 4 byte.

Căn chỉnh không trực tiếp kéo dài tuổi thọ EEPROM, nhưng giúp bố trí dữ liệu phù hợp với cơ chế ECC và kiểm soát tần suất ghi.

### 3.2. CRC và toàn vẹn dữ liệu

Các struct dữ liệu không chứa trường CRC. Khi ghi, hàm lưu trữ tự động nối thêm CRC-16/MODBUS 2 B vào cuối dữ liệu, theo thứ tự little-endian (LSB trước, MSB sau). Khi đọc, hàm tách 2 B CRC, tính lại trên phần dữ liệu và so sánh. Chi tiết trong `sv_eeprom.h`.

Khi CRC không hợp lệ, dữ liệu không được sử dụng. Hành vi theo từng vùng:

- Metadata và Runtime Data: chuyển sang khu vực luân phiên khác.
- Cấu hình: sử dụng cấu hình mặc định.
- Bản ghi Latch, Event, Push Status, Changed Info Log: bỏ qua bản ghi.

CRC giúp phát hiện dữ liệu sai lệch nhưng không tự khôi phục dữ liệu và không phát hiện được mọi loại lỗi.

### 3.3. Metadata và Runtime Data (4 khu vực luân phiên)

Hai vùng này được chia thành 4 khu vực để phân tán số lần ghi. Mỗi khu vực là một packet gồm phần dữ liệu (struct đóng gói `packed`), theo sau là CRC-16/MODBUS 2 B, lưu theo thứ tự little-endian. Packet được đệm đến bội số của 4 byte bằng `ALIGN4()`.

| Vùng | Số khu vực | Kích thước mỗi khu vực | Kích thước packet | Nội dung |
|---|---|---|---|---|
| Metadata | 4 | 64 B | 28 B | Chỉ số đọc/ghi và số lượng bản ghi của các vùng bộ đệm vòng |
| Runtime Data | 4 | 80 B | 72 B | Số thứ tự cập nhật, số lần MCU reset và bộ đếm xung theo cổng |

Khi khởi tạo, firmware đọc toàn bộ các khu vực của Metadata và Runtime Data, chỉ giữ những khu vực có CRC hợp lệ, sau đó chọn khu vực có `u32Sequence` lớn nhất làm giá trị hiện hành.

### 3.4. Bộ đệm vòng (Circular Buffer)

Bốn vùng Latch, Event, Push Status và Changed Info Log dùng bộ đệm vòng. Chỉ số đọc, chỉ số ghi và số lượng bản ghi của mỗi vùng được lưu trong Metadata (mục [3.3](#33-metadata-và-runtime-data-4-khu-vực-luân-phiên)).

| Vùng | Struct bản ghi | Số bản ghi tối đa | Packet mỗi bản ghi |
|---|---|---:|---|
| Latch | `Latch_Data_t` | 720 | 208 B |
| Event | `Event_Data_t` | 1000 | 12 B |
| Push Status | `Push_Status_Data_t` | 1000 | 16 B |
| Changed Info Log | `Changed_Info_Data_t` | 500 | 20 B |

**Quy tắc khi ghi:**

- Khi `SaveIndex` đạt `MAX_COUNT`: đưa `SaveIndex` về `0` và tiếp tục ghi theo vòng.
- Khi `SaveIndex` trùng `LoadIndex` (vùng đầy), áp dụng cho Latch và Event: loại bản ghi cũ nhất bằng cách tăng `LoadIndex` lên 1 (về `0` nếu đạt `MAX_COUNT`), sau đó ghi bản ghi mới tại `SaveIndex`.

## 4. Tài liệu liên quan