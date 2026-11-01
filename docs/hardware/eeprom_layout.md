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

Các hệ quả khi thiết kế firmware:

- Dù có thể ghi riêng từng byte, mỗi thao tác ghi vẫn tính vào số chu kỳ ghi/xóa của cả nhóm 4 byte chứa byte đó.
- Mỗi vùng dữ liệu nên có địa chỉ bắt đầu và kích thước căn theo bội số của 4 byte, để dữ liệu của hai vùng khác nhau không dùng chung một nhóm.
- Firmware dùng macro `ALIGN4()` (định nghĩa trong `app_storage.h`) để căn kích thước gói dữ liệu theo bội số 4 byte.

Căn chỉnh không trực tiếp kéo dài tuổi thọ EEPROM, nhưng giúp bố trí dữ liệu phù hợp với cơ chế ECC và kiểm soát tần suất ghi.

### 3.2. Cấu trúc dữ liệu và lưu luân phiên (Rotating Slots)

#### 3.2.1. Header (16 B, `0x00000`)

Cấu trúc `Eeprom_Header_t` (đóng gói `packed`) chiếm 14 B. 2 B còn lại là dự phòng, không khai báo trong struct.

| Offset | Kích thước | Trường | Ý nghĩa |
|---|---|---|---|
| `0x00` | 4 B | `u32Magic` | `0x02468ACE` (`EEPROM_MAGIC_NUMBER`), xác nhận EEPROM đã được khởi tạo |
| `0x04` | 10 B | `au8Version[10]` | Chuỗi phiên bản layout, hiện là `"V1.0.0"` |

Khi khởi động, firmware kiểm tra `u32Magic` và `au8Version`. Nếu hợp lệ sẽ thực hiện lấy dữ liệu configuration trong EEPROM và chạy chương trình, nếu không hợp lệ sẽ init dữ liệu trong EEPROM rồi chạy chương trình.

#### 3.2.2. Device Activation Status (4 B, `0x0001C`)

Lưu giá trị enum `Device_Activation_Status_t`.

| Giá trị | Tên | Ý nghĩa |
|---|---|---|
| 0 | `DEVICE_ACTIVATION_STATUS_DEACTIVED` | Chưa kích hoạt. Thiết bị không khởi tạo ngoại vi đo đếm, không thực hiện chốt và gửi, thiết bị sẽ tự động tắt nguồn trong vòng 10 phút. |
| 1 | `DEVICE_ACTIVATION_STATUS_ACTIVED` | Đã kích hoạt. Thiết bị khởi tạo đồng hồ xung, cảm biến áp suất và module 4G, sau đó sẽ thực hiện chốt và gửi bình thường. |

#### 3.2.3. Device Password (256 B, `0x00020`)

Vùng chứa `PASSWORD_COUNT` = 3 bản ghi `Password_Record_t` (đóng gói `packed`), mỗi bản ghi tương ứng một cấp người dùng.

| Trường | Kích thước | Ý nghĩa |
|---|---:|---|
| `au8Salt` | 16 B | Salt cho PBKDF2 |
| `au8DerivedKey` | 32 B | Khóa dẫn xuất PBKDF2-HMAC-SHA-256 |
| `u32IterationCount` | 4 B | Số vòng lặp PBKDF2 |

Dữ liệu mỗi bản ghi 52 B, packet = `ALIGN4(52 + 2)` = 56 B. Vị trí từng bản ghi và cách căn chỉnh: `[TBD: xác nhận trong app_storage.h]`.

Mật khẩu mặc định và giá trị băm không được ghi trong tài liệu này.

#### 3.2.4. Metadata và Runtime Data (4 khu vực luân phiên)

Hai vùng này được chia thành 4 khu vực. Mỗi khu vực là một packet gồm phần dữ liệu (struct đóng gói `packed`), theo sau là CRC-16/MODBUS 2 B, lưu theo thứ tự little-endian. Packet được đệm đến bội số của 4 byte bằng `ALIGN4()`.

| Vùng | Số khu vực | Kích thước mỗi khu vực | Kích thước packet | Nội dung |
|---|---|---|---|---|
| Metadata | 4 | 64 B | 28 B | Chỉ số đọc/ghi và số lượng bản ghi của các vùng bộ đệm vòng |
| Runtime Data | 4 | 80 B | 72 B | Số thứ tự cập nhật, số lần MCU reset và bộ đếm xung theo cổng |

**`Eeprom_Metadata_t`** (24 B dữ liệu):

| Trường | Kiểu | Ý nghĩa |
|---|---|---|
| `u32Sequence` | `uint32_t` | Số thứ tự cập nhật, tăng dần |
| `u16NextLatchSaveIndex` / `u16NextLatchLoadIndex` / `u16LatchCount` | `uint16_t` × 3 | Chỉ số ghi, đọc và số bản ghi của Latch |
| `u16NextEventSaveIndex` / `u16NextEventLoadIndex` / `u16EventCount` | `uint16_t` × 3 | Chỉ số ghi, đọc và số bản ghi của Event |
| `u16NextPushStatusSaveIndex` / `u16PushStatusCount` | `uint16_t` × 2 | Chỉ số ghi và số bản ghi của Push Status |
| `u16NextChangedInfoLogSaveIndex` / `u16ChangedInfoLogCount` | `uint16_t` × 2 | Chỉ số ghi và số bản ghi của Changed Info Log |

**`Eeprom_Runtime_Data_t`** (69 B dữ liệu):

| Trường | Kiểu | Kích thước | Ý nghĩa |
|---|---|---:|---|
| `u32Sequence` | `uint32_t` | 4 B | Số thứ tự cập nhật, tăng dần |
| `u8ResetCount` | `uint8_t` | 1 B | Số lần MCU reset |
| `sPulseCount[4]` | `Pulse_Count_t[]` | 64 B | Bộ đếm xung theo cổng (`MAX_PULSE_GATE_COUNT` = 4) |

`Pulse_Count_t` gồm `u64ForwardPulseCount` và `u64ReversePulseCount`, mỗi `Pulse_Count_t` 16 B.

Khi khởi tạo, firmware đọc toàn bộ các khu vực của Metadata và Runtime Data, chỉ giữ những khu vực có CRC hợp lệ, sau đó chọn khu vực có `u32Sequence` lớn nhất làm giá trị hiện hành.

#### 3.2.5. Cấu hình

| Vùng | Struct | Trường |
|---|---|---|
| IP Endpoint | `Ip_Endpoint_t` | `au8Ipv4[15]`, `au8Port[5]` |
| Module | `Module_Config_Parameter_t` | `u16LatchPeriod`, `u16PushPeriod`, `fTimezone` |
| Charge | `Charge_Config_Parameter_t` | `u16IinLimMa`, `u16ChargeVoltageMv`, `u16ChargeCurrentMa`, `u8ChargeLedEnable` |
| Pulse Meter | `Pulse_Meter_Config_Parameter_t` | `u8MeterEnable`, `u8Serial[20]`, `sConfig` |
| Modbus Meter | `Modbus_Meter_Config_Parameter_t` | `u8MeterEnable`, `u8Serial[20]`, `sConfig` |
| Pressure Sensor | `Pressure_Sensor_Config_Parameter_t` | `u8MeterEnable`, `u8Serial[20]`, `sConfig` |

### 3.3. Bản ghi mật khẩu và chuỗi kiểm tra

`[TBD]` (đã gộp vào mục 3.2.3, giữ mục này để đánh số nếu cần).

### 3.4. Bộ đệm vòng (Circular Buffer)

Bốn vùng Latch, Event, Push Status và Changed Info Log dùng bộ đệm vòng. Chỉ số đọc, chỉ số ghi và số lượng bản ghi của mỗi vùng được lưu trong Metadata (mục 3.2.4).

| Vùng | Struct bản ghi | Số bản ghi tối đa | Packet mỗi bản ghi |
|---|---|---:|---|
| Latch | `Latch_Data_t` | `MAX_LATCH_COUNT` = 720 | 208 B |
| Event | `Event_Data_t` | `MAX_EVENT_COUNT` = 1000 | 12 B |
| Push Status | `Push_Status_Data_t` | `MAX_PUSH_STATUS_COUNT` = 1000 | 16 B |
| Changed Info Log | `Changed_Info_Data_t` | `MAX_CHANGED_INFO_COUNT` = 500 | 20 B |

**Quy tắc khi ghi:**
- Khi `SaveIndex` đạt `MAX_COUNT`: Đưa `SaveIndex` về `0` và tiếp tục ghi theo vòng.
- Khi `SaveIndex` trùng `LoadIndex` (vùng đầy), áp dụng cho Latch và Event: Loại bản ghi cũ nhất bằng cách tăng `LoadIndex` lên 1 (về `0` nếu đạt `MAX_COUNT`), sau đó ghi bản ghi mới tại `SaveIndex`.


**Mã sự kiện (`Event_Code_t`):** `EVENT_MCU_RESET` (0), `EVENT_MAGNETIC_DETECTED`, `EVENT_MAGNETIC_ENDED`, `EVENT_POWER_CONNECTED`, `EVENT_POWER_LOST`, `EVENT_LOW_BATTERY`, `EVENT_LOW_BATTERY_ENDED`, `EVENT_CONFIG_CHANGED`, `EVENT_PASSWORD_CHANGED`, `EVENT_FIRMWARE_UPDATED`.

**Mã thay đổi cấu hình (`Changed_Config_Id_t`):** gồm Module Serial, Activation Status, Time, IP Endpoint, Latch Period, Push Period, Timezone, Charge, Pulse Meter 1–4, Modbus Meter 1–4, Pressure Sensor 1–2, Reset Setting, Password, Reset Password và `CHANGED_UNKNOW` (0xFF).

### 3.5. CRC và toàn vẹn dữ liệu

Các struct dữ liệu không chứa trường CRC. Khi ghi vào EEPROM, hàm lưu trữ tự động tính và nối thêm CRC-16/MODBUS 2 B vào cuối dữ liệu, theo thứ tự little-endian (LSB trước, MSB sau). Khi đọc, hàm đọc tách 2 B CRC, tính lại trên phần dữ liệu và so sánh. (Chi tiết trong `sv_eeprom.h`).

- **Khi ghi:** Tính CRC trên phần dữ liệu, ghi dữ liệu và CRC vào EEPROM, sau đó đọc lại và kiểm tra CRC.
- **Khi đọc:** Đọc dữ liệu cùng 2 byte CRC, tính lại CRC trên phần dữ liệu và so sánh với giá trị đã lưu.
- **Khi CRC không hợp lệ:** Không sử dụng dữ liệu đó. Hành vi theo từng vùng:
  - Metadata và Runtime Data: chuyển sang khu vực luân phiên khác (mục 3.2.4).
  - Cấu hình: `[TBD: nạp giá trị mặc định / báo lỗi]`.
  - Bản ghi Latch, Event, Push Status, Changed Info Log: `[TBD: bỏ qua bản ghi / ghi log lỗi]`.

CRC giúp phát hiện dữ liệu sai lệch, nhưng không tự khôi phục dữ liệu và không phát hiện được mọi loại lỗi.

## 4. Tài liệu liên quan