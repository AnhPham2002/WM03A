## 1. Tổng quan

Tài liệu này mô tả phân vùng SRAM của STM32L431RCT6 trong firmware WM03A, bao gồm vùng dữ liệu thông thường, vùng đặt địa chỉ thủ công (`RAM_MANUAL`) và vùng giữ dữ liệu qua reset (`RAM_NOINIT`).

## 2. Phân vùng SRAM

| Vùng | Địa chỉ bắt đầu | Kích thước | Cách quản lý | Mục đích |
|---|---|---:|---|---|
| RAM | `0x20000000` | 48 KB | Compiler (`.data`, `.bss`) | Dữ liệu thông thường, khởi tạo khi khởi động |
| RAM_MANUAL | `0x10000000` | 1 KB | Người phát triển đặt địa chỉ cố định | Dữ liệu OTA metadata, giữ qua reset |
| RAM_NOINIT | `0x10000400` | 15 KB | Compiler, qua section `.ram_noinit` | Dữ liệu trạng thái, giữ qua reset |

Cả `RAM_MANUAL` và `RAM_NOINIT` đều là vùng noinit: trình khởi động C không xóa hay gán giá trị lại cho chúng. Khác biệt nằm ở cách xếp địa chỉ:

- `RAM_MANUAL` được khai báo tại địa chỉ cố định (`RAM_NOINIT_OTA_METADATA_ADDRESS`). Người phát triển chịu trách nhiệm không để vùng này chồng lấn với biến khác.
- `RAM_NOINIT` dùng thuộc tính `__attribute__((section(".ram_noinit")))`. Linker script ánh xạ section này vào vùng `RAM_NOINIT`, còn địa chỉ từng biến do compiler quyết định.

Vì địa chỉ của biến trong `RAM_NOINIT` không cố định, không nên hard-code địa chỉ của chúng trong tài liệu hoặc trong code khác.

## 3. Dữ liệu OTA (`RAM_MANUAL`)

`Ota_Metadata_t` được đặt tại `0x10000000` (`RAM_NOINIT_OTA_METADATA_ADDRESS`) và được truy cập qua con trỏ `pOtaMetadata`. Dữ liệu hợp lệ khi `u32Magic` = `0x11223344`.

| Trường | Kiểu | Ý nghĩa |
|---|---|---|
| `u32Magic` | `uint32_t` | Magic number, xác nhận dữ liệu hợp lệ |
| `au8Version[12]` | `uint8_t[12]` | Phiên bản firmware mới |
| `bFirmwareUpdated` | `bool` | Đã cập nhật firmware hay chưa |
| `u16PacketIndex` | `uint16_t` | Chỉ số gói OTA đang xử lý |
| `u32Size` | `uint32_t` | Kích thước firmware |
| `u32Crc` | `uint32_t` | CRC của firmware |

## 4. Trạng thái giữ qua reset (`RAM_NOINIT`)

Các trạng thái sau được khai báo với `RAM_NOINIT` và do compiler xếp địa chỉ. Mỗi trạng thái có magic number riêng:

| Biến | Struct | Magic | Nội dung |
|---|---|---|---|
| `sMagneticStatus` | `Magnetic_Status_t` | `0x11223344` | Trạng thái nam châm: đang phát hiện hay không, thời điểm phát hiện và kết thúc |
| `sPowerStatus` | `Power_Status_t` | `0x5A5AA5A5` | Trạng thái nguồn VBUS và pin: có VBUS hay không, đang kiểm tra, pin yếu |
| `sConfigChangeStatus` | `Config_Change_Status_t` | `0xA5A55A5A` | Đang thay đổi cấu hình hay không và thời điểm bắt đầu |
| `sPasswordChangeStatus` | `Password_Change_Status_t` | `0xFEDCBA98` | Đang thay đổi mật khẩu hay không và thời điểm bắt đầu |
| `sPushStatus` | `Push_Status_t` | `0x12344321` | Trạng thái chờ phản hồi khi gửi dữ liệu, thời điểm kích hoạt. Timeout phản hồi: 2000 ms |
| `sPulseCount[]` | `Pulse_Count_t` | `0x12345678` | Số xung tích lũy theo cổng, có CRC16 kiểm tra (`u16PulseCountCrc`) |

## 5. Kiểm tra khi khởi động

Với mỗi biến trong `RAM_NOINIT` và `RAM_MANUAL`, firmware kiểm tra `u32Magic` trước khi sử dụng. Nếu magic không khớp, dữ liệu được coi là không hợp lệ và được khởi tạo lại về giá trị mặc định.

## 6. Tài liệu liên quan