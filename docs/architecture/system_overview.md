# WM03A System Overview

## 1. Giới thiệu

WM03A là thiết bị thu thập và truyền dữ liệu đồng hồ nước (Water Meter Datalogger), được thiết kế để giám sát trạng thái vận hành, thu thập dữ liệu đo lường và truyền dữ liệu về hệ thống quản lý từ xa.

Thiết bị sử dụng vi điều khiển STM32L431RCT6 làm bộ xử lý trung tâm, kết hợp các giao tiếp ngoại vi và module truyền thông để kết nối với cảm biến, đồng hồ nước và máy chủ.

**Chức năng chính:**

- Thu thập dữ liệu từ đồng hồ nước qua giao tiếp RS485 (Modbus RTU) và ngõ vào xung.
- Đo giá trị áp suất từ cảm biến ngõ ra 4–20 mA.
- Lưu trữ dữ liệu vận hành và cấu hình trong EEPROM ngoài.
- Truyền dữ liệu lên Server qua mạng di động 4G.
- Hỗ trợ cấu hình, giám sát và cập nhật firmware từ xa (OTA) hoặc tại hiện trường qua PC Tool.

## 2. Thông số tổng quan

| Hạng mục | Mô tả |
|---|---|
| Sản phẩm | WM03A (Water Meter Datalogger) |
| Vi điều khiển chính | STM32L431RCT6 |
| Truyền thông di động | A7677S-LANV (4G) |
| Truyền thông có dây | RS485 (MAX3485) |
| Bộ nhớ ngoài | M95M02 (EEPROM) |
| Ngõ vào analog | Dòng điện 4–20 mA từ cảm biến áp suất |
| Ngõ vào xung | Xung từ đồng hồ nước |
| Ngôn ngữ firmware | C |
| Môi trường phát triển | STM32CubeIDE / CMake / Ninja |

## 3. Các thành phần chính

### 3.1. Phần cứng

- **MCU chính:** STM32L431RCT6, điều khiển toàn bộ hoạt động của thiết bị.
- **Module di động:** A7677S-LANV, cung cấp kết nối 4G để truyền dữ liệu.
- **Giao tiếp RS485:** Kết nối với đồng hồ nước hoặc thiết bị hỗ trợ Modbus RTU.
- **EEPROM ngoài:** Lưu trữ thông tin thiết bị, cấu hình và dữ liệu vận hành.
- **Ngõ vào analog:** Tiếp nhận tín hiệu từ cảm biến áp suất 4–20 mA.
- **Ngõ vào xung:** Tiếp nhận xung từ đồng hồ nước.

### 3.2. Firmware

Firmware được phát triển bằng ngôn ngữ C và chạy trên STM32L431RCT6, đảm nhiệm:

- Quản lý và điều khiển phần cứng ngoại vi.
- Thu thập và xử lý dữ liệu đo lường.
- Quản lý cấu hình và dữ liệu lưu trữ.
- Điều khiển module 4G và giao tiếp RS485.
- Quản lý trạng thái thiết bị và ghi nhận các sự kiện vận hành.
- Hỗ trợ cập nhật firmware OTA.

### 3.3. PC Tool

PC Tool là phần mềm chạy trên máy tính, dùng để cấu hình và bảo trì thiết bị tại hiện trường qua kết nối RS485, với các chức năng:

- Kết nối với thiết bị qua giao tiếp Serial/RS485.
- Đọc và thay đổi cấu hình thiết bị.
- Hiển thị thông tin và trạng thái hoạt động.
- Đọc dữ liệu từ thiết bị.
- Hỗ trợ cập nhật firmware.

### 3.4. Server

Server tiếp nhận, lưu trữ và quản lý dữ liệu từ các thiết bị WM03A, với các chức năng:

- Tiếp nhận dữ liệu từ thiết bị.
- Lưu trữ và quản lý dữ liệu đo lường.
- Giám sát trạng thái thiết bị.
- Quản lý thông tin và cấu hình thiết bị.

## 4. Nguyên lý hoạt động tổng thể

WM03A thu thập dữ liệu từ đồng hồ nước và cảm biến thông qua các giao tiếp ngoại vi. MCU xử lý dữ liệu, lưu các thông tin cần thiết vào EEPROM và điều khiển việc truyền dữ liệu lên Server qua module 4G.

PC Tool được sử dụng để cấu hình, giám sát và bảo trì thiết bị thông qua kết nối có dây RS485.

## 5. Tài liệu liên quan