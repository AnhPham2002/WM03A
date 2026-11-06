Các vấn đề còn tồn tại của firmware:
- Chưa xử lý vấn đề chặn cổng RS485 khi nhập sai mật khẩu nhiều lần hoặc truyền sai frame nhiều lần.
- Cần phải sửa lại giao thức của command GET và SET để thiết bị và PC Tool/Server giảm được khối lượng giao tiếp.
- Chưa chốt được driver cho IC sạc (BQ25895) do dự kiến phần cứng sẽ thay đổi IC sạc khác (BQ25622).
- Chưa khắc phục được hoàn toàn vấn đề dòng cao (dòng ngủ trung bình hiện tại đang ở mức khoảng 700uA tại mức pin 4.0V)