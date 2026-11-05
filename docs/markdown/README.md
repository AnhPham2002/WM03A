# Documentation

## 1. Giới thiệu

Water Datalogger **WM03A** là thiết bị thu thập dữ liệu từ đồng hồ nước và các cảm biến giám sát. Thiết bị hỗ trợ xử lý và lưu trữ dữ liệu cục bộ, đồng thời truyền dữ liệu đến máy chủ trung tâm thông qua mạng di động.

Bên cạnh khả năng truyền thông từ xa, thiết bị hỗ trợ giao tiếp trực tiếp tại hiện trường phục vụ cấu hình, kiểm tra, chẩn đoán và bảo trì. Firmware được thiết kế theo hướng phân tầng và module hóa, nhằm nâng cao khả năng bảo trì, mở rộng chức năng và đảm bảo độ tin cậy trong quá trình vận hành.

## 2. Danh mục các tài liệu thành phần

### Architecture
- [System Architecture](architecture/architecture.md)

### Hardware
- [Hardware Design](hardware/hardware.md)

### Firmware
- [Firmware Architecture](firmware/firmware_architecture.md)
- [FLASH layout](firmware/flash.md)
- [Bootloader](firmware/bootloader.md)
- [Application](firmware/application.md)
- [SRAM layout](firmware/sram.md)
- [EEPROM layout](firmware/eeprom.md)

### Measurement
- [Pulse Meter](measurement/pulse_meter.md)
- [Modbus Meter](measurement/modbus_meter.md)
- [Pressure Sensor](measurement/pressure_sensor.md)

### Security
- [Security](security/security.md)

### Communication
- [Communication Protocol](communication/protocol.md)
- [RS485 Communication](communication/rs485.md)
- [Cellular Module Communication](communication/cellular.md)
- [Server Communication](communication/server.md)
- [OTA Firmware Update](communication/ota.md)

### Development
- [Firmware Image Packing](compilation/firmware_image_packing.md)
- [Build and Flash](compilation/build_and_flash.md)