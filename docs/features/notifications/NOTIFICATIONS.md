# Thông báo email

## Sự kiện gửi email
- Tin nhắn mới trong chat (gửi cho người nhận nếu offline).
- Tin đăng được duyệt/ẩn.
- Có người quan tâm (tuỳ chọn subscribe theo tin/danh mục).

## Cấu hình
- SMTP cấu hình qua biến môi trường (.env): HOST, PORT, USER, PASSWORD, FROM.
- Bật/tắt email theo môi trường; tránh gửi thật trong dev.

## Nội dung
- Mẫu email đơn giản (text hoặc HTML tối giản), có liên kết đến trang chi tiết.
- Bao gồm footer cảnh báo nội bộ.

## Kiểm thử
- Mock SMTP trong pytest, kiểm tra số lượng và nội dung email.
