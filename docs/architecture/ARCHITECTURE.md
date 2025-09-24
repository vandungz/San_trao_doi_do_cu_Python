# Kiến trúc tổng quan

## Mục tiêu phi chức năng
- Đơn giản, dễ triển khai nội bộ, ưu tiên tốc độ phát triển.
- Bảo mật ở mức nội bộ: xác thực, CSRF, phân quyền cơ bản.
- Dễ chuyển từ SQLite sang PostgreSQL khi cần.

## Lựa chọn công nghệ
- Django (mặc định) hoặc FastAPI + Jinja. Quyết định cuối cùng ở Milestone 1.
- Templates server-side để giảm độ phức tạp frontend.
- Storage ảnh: filesystem (dev); có thể trừu tượng hóa để chuyển S3/MinIO.

## Sơ đồ logic cao cấp
- Người dùng → Web app (views/templates) → ORM → SQLite
- Email notifications → SMTP server (cấu hình .env)
- Chat cơ bản: (realtime)

## Module dự kiến (Django terms)
- core: cấu hình dự án, settings, base templates.
- users: đăng ký/đăng nhập, profile.
- listings: đăng tin, media, trạng thái.
- search: view tìm kiếm, filter, sort.
- chat: hội thoại 1-1 theo tin đăng.
- notifications: gửi email theo trigger domain.

## Ràng buộc và quyết định
- Ưu tiên đồng bộ HTTP trước; tránh WebSocket giai đoạn đầu.
- Không có thanh toán; chỉ liên hệ giữa người dùng.
- Ảnh giới hạn dung lượng, số lượng; kiểm tra MIME.

## Khả năng mở rộng tương lai
- Thay SQLite bằng PostgreSQL.
- Bổ sung Celery/Redis cho email hàng loạt hoặc tác vụ nền.
- Realtime chat bằng WebSocket hoặc dịch vụ đẩy.
