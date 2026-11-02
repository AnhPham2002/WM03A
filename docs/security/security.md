# Bảo mật WM03A

## 1. Tổng quan

Tài liệu này mô tả các cơ chế bảo mật của WM03A, gồm ba phần:

- **Bảo mật thiết bị:** xác thực người dùng khi truy cập thiết bị và phân quyền theo cấp.
- **Bảo mật mật khẩu:** cách lưu trữ mật khẩu trong FLASH và EEPROM bằng PBKDF2-HMAC-SHA-256.
- **Bảo mật truyền thông:** cách bảo vệ dữ liệu trao đổi với PC Tool (RS485) và Server (4G).

## 2. Bảo mật thiết bị

### 2.1. Đăng nhập bằng mật khẩu

`[TBD: mô tả luồng bắt tay (ACCESS_LV_0) và đăng nhập (ACCESS_LV_1 đến ACCESS_LV_3)]`

### 2.2. Phân quyền truy cập

Thiết bị hỗ trợ ba cấp mật khẩu tương ứng với ba mức quyền truy cập.

- Mức 1: Người vận hành (Supervisor).
- Mức 2: Kỹ sư (Engineer).
- Mức 3: Nhà máy (Factory / Admin).

## 3. Bảo mật mật khẩu

### 3.1. Nguyên tắc lưu trữ

Mật khẩu người dùng không được lưu dưới dạng văn bản rõ. Firmware dẫn xuất khóa từ mật khẩu bằng thuật toán **PBKDF2-HMAC-SHA-256**, sau đó chỉ lưu salt, khóa dẫn xuất và số vòng lặp vào FLASH và EEPROM.

Mỗi cấp mật khẩu được lưu thành một bản ghi `Password_Record_t` gồm ba trường:

- `au8Salt`: salt, 16 byte.
- `au8DerivedKey`: khóa dẫn xuất PBKDF2-HMAC-SHA-256, 32 byte.
- `u32IterationCount`: số vòng lặp PBKDF2, 4 byte.

Khi người dùng nhập mật khẩu mới, firmware gọi `pbkdf2_hmac_sha256()` để tạo khóa dẫn xuất từ mật khẩu và salt, rồi lưu khóa dẫn xuất cùng salt vào bản ghi. Số vòng lặp cố định là 50. `[TBD: xác nhận salt có được sinh ngẫu nhiên mỗi lần đổi mật khẩu hay không]`

Mật khẩu mặc định trong firmware chỉ được lưu dưới dạng salt và khóa dẫn xuất đã tính sẵn. Mật khẩu thô vẫn xuất hiện trong chú thích cạnh macro khóa dẫn xuất tương ứng, cần xóa trước khi chia sẻ mã nguồn rộng hơn.

### 3.2. Tham số PBKDF2

| Tham số | Giá trị | Nguồn |
|---|---|---|
| Thuật toán | PBKDF2-HMAC-SHA-256 | `app_storage.h` |
| Số cấp mật khẩu | 3 | `PASSWORD_COUNT` |
| Độ dài mật khẩu | 4 – 32 ký tự | `PASSWORD_MIN_LENGTH`, `PASSWORD_MAX_LENGTH` |
| Kích thước salt | 16 B | `PBKDF2_HMAC_SHA256_SALT_SIZE` |
| Kích thước khóa dẫn xuất | 32 B | `PBKDF2_HMAC_SHA256_DERIVED_KEY_SIZE` |
| Số vòng lặp | 50 | `PBKDF2_HMAC_SHA256_ITERATION` |

## 4. Bảo mật truyền thông

### 4.1. Phạm vi áp dụng

`[TBD: xác nhận CBC áp dụng cho kênh nào: RS485 với PC Tool, 4G với Server, hay cả hai]`

### 4.2. Thuật toán mã hóa

| Tham số | Giá trị |
|---|---|
| Thuật toán khối | `[TBD: AES-128 / AES-192 / AES-256]` |
| Chế độ | CBC |
| Độ dài khóa | `[TBD]` |
| Đệm (padding) | `[TBD: PKCS#7 hoặc phương pháp khác]` |
| Vector khởi tạo (IV) | `[TBD: cách sinh, có ngẫu nhiên và duy nhất cho mỗi gói không]` |

### 4.3. Quản lý khóa

- Nơi lưu khóa: `[TBD]`
- Cách cập nhật khóa: `[TBD]`
- Khóa có được ghi ra ngoài qua PC Tool hoặc Server không: `[TBD]`

### 4.4. Toàn vẹn gói tin

CBC chỉ bảo đảm tính bí mật, không tự phát hiện gói bị sửa đổi. `[TBD: xác nhận đang dùng CRC-16 hay có HMAC/MAC đi kèm]`. Nếu chỉ có CRC-16, nó chỉ phát hiện lỗi ngẫu nhiên, không chống được việc cố ý sửa gói tin.

### 4.5. Xử lý lỗi

- Giải mã lỗi do sai padding hoặc sai IV: `[TBD]`
- Gói tin không qua kiểm tra toàn vẹn: `[TBD]`

## 5. Tài liệu liên quan
