# Chiến lược kiểm thử (pytest)

## Mục tiêu
- Đảm bảo luồng chính hoạt động: auth, listings, search, chat, email.
- Coverage mục tiêu ≥ 70% giai đoạn đầu.

## Công cụ
- pytest, pytest-django hoặc pytest + FastAPI TestClient (tuỳ khung chọn).
- factory-boy hoặc model_bakery để tạo dữ liệu mẫu.

## Phân lớp test
- Unit test: logic thuần, validators, services.
- Integration test: ORM + view/template + routing.
- Functional flow: đăng ký→đăng nhập→đăng tin→tìm kiếm→chat→email.

## Dữ liệu giả
- Fixtures người dùng, danh mục, tin đăng, hội thoại.
- Ảnh mẫu nhỏ để kiểm thử upload.

## CI (đề xuất)
- Chạy pytest với -q, xuất coverage XML/HTML.
- Gate PR nếu coverage giảm đáng kể.
