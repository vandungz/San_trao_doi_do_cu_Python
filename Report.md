# Báo cáo đề tài: Sàn trao đổi đồ cũ nội bộ

## Chương 1: Giới thiệu

### 1.1 Lý do chọn đề tài
- Nhu cầu trao đổi, tái sử dụng đồ cũ trong nội bộ tổ chức giúp tiết kiệm chi phí và bảo vệ môi trường.
- Các kênh trao đổi hiện tại (mạng xã hội, chat rời rạc) thiếu kiểm soát, khó tìm kiếm, dễ thất lạc thông tin.
- Một nền tảng nội bộ, đơn giản, an toàn sẽ tối ưu hóa trải nghiệm và hiệu quả.

### 1.2 Vấn đề đặt ra
- Làm thế nào để người dùng nội bộ dễ dàng đăng tin, tìm kiếm, trao đổi thông tin mua/bán một cách an toàn?
- Quản lý phương tiện (ảnh), phân quyền, chống spam và đảm bảo riêng tư trong nội bộ.
- Thông báo kịp thời (email) và kênh trò chuyện đơn giản để tăng tương tác.

### 1.3 Mục tiêu & phạm vi
- Xây dựng website nội bộ với các chức năng: đăng ký/đăng nhập, đăng tin kèm ảnh, tìm kiếm/lọc, chat 1-1 theo tin, thông báo email.
- Phạm vi nội bộ: chỉ người dùng thuộc tổ chức hoặc được mời; không tích hợp thanh toán.
- Giai đoạn đầu dùng SQLite và render server-side; có thể mở rộng về sau.

### 1.4 Phương pháp nghiên cứu
- Khảo sát nhu cầu nội bộ và các giải pháp tương tự (market scan).
- Lựa chọn công nghệ Python (Django/FastAPI) theo tiêu chí tốc độ phát triển, bảo trì, bảo mật.
- Thiết kế hướng miền (domain-first) với mô hình dữ liệu rõ ràng; lặp nhanh theo MVP.
- Kiểm thử bằng pytest: unit/integration; đánh giá kết quả theo tiêu chí chấp nhận.

### 1.5 Bố cục báo cáo
- Chương 1: Bối cảnh, mục tiêu, phạm vi, phương pháp, bố cục.
- Chương 2: Công nghệ nền tảng và nghiên cứu liên quan.
- Chương 3: Phân tích yêu cầu, kiến trúc, mô hình ERD/UML.
- Chương 4: Triển khai, môi trường thực nghiệm, kết quả.
- Chương 5: Kết luận và hướng phát triển; Tài liệu tham khảo; Phụ lục.

## Chương 2: Cơ sở lý thuyết & nghiên cứu liên quan

### 2.1 Các khái niệm, công nghệ nền tảng
- Python, hệ sinh thái web.
- Django (MTV, ORM, Auth, Admin) hoặc FastAPI (ASGI, Pydantic, dependency injection) với Jinja2.
- SQLite cho môi trường phát triển và kiểm thử; có thể thay bằng PostgreSQL khi mở rộng.
- Mẫu kiến trúc server-side rendering, bảo vệ CSRF, session-based auth.

### 2.2 Các nghiên cứu/ứng dụng trước đây
- Nền tảng rao vặt nội bộ/đồ cũ trong doanh nghiệp và trường học (case studies), nhấn mạnh: tính đơn giản, kiểm soát truy cập, tìm kiếm nhanh.
- So sánh giải pháp tự xây (custom) vs dùng công cụ chung (forums, marketplace plugins): custom phù hợp hơn cho yêu cầu nội bộ, dữ liệu tối giản, kiểm soát tốt.

## Chương 3: Phân tích & thiết kế hệ thống/giải pháp

### 3.1 Yêu cầu hệ thống
- Chức năng: quản lý người dùng; đăng tin; upload ảnh; tìm kiếm/lọc; chat 1-1; thông báo email.
- Phi chức năng: bảo mật nội bộ, hiệu năng đủ dùng, dễ triển khai/bảo trì, kiểm thử tự động.
- Ràng buộc: không thanh toán; media giới hạn dung lượng; chỉ người dùng nội bộ truy cập.

### 3.2 Kiến trúc tổng thể
- Ứng dụng web Python + template server-side; ORM kết nối SQLite.
- Email qua SMTP cấu hình bằng biến môi trường.
- Chat đơn giản lưu DB; làm mới trang để xem tin nhắn (chưa realtime).

### 3.3 Mô hình dữ liệu (ERD phác thảo)
- Users(1) — (N) Listings; Listings(1) — (N) ListingImages.
- Listings(1) — (N) Conversations (mỗi conversation liên quan một listing và 2 user: buyer/seller).
- Conversations(1) — (N) Messages.

### 3.4 UML mức cao (mô tả)
- Use case: Đăng nhập; Đăng tin; Tìm kiếm; Mở chat; Gửi tin nhắn; Nhận email.
- Class (khái quát): User, Listing, ListingImage, Conversation, Message, NotificationService.
- Sequence (chat): Buyer mở chat → tạo Conversation → Buyer gửi Message → Seller nhận email thông báo.

## Chương 4: Triển khai & kết quả

### 4.1 Công cụ, môi trường
- Python 3.11+, venv, pip.
- Django hoặc FastAPI + Jinja2; SQLite.
- pytest, factory-boy/model_bakery (dự kiến), công cụ lint/format (ruff/flake8, black, isort).

### 4.2 Cấu hình/thực nghiệm
- Dev: cấu hình `.env` (SECRET_KEY, DEBUG, EMAIL_*, …), chạy trên máy cá nhân.
- Ảnh lưu filesystem; đặt giới hạn kích thước và số lượng.
- Test: chạy pytest, sinh fixture dữ liệu cơ bản.

### 4.3 Kết quả đạt được (dự kiến theo mốc)
- MVP: đăng ký/đăng nhập; đăng tin kèm ảnh; tìm kiếm/lọc; chat 1-1; email thông báo.
- Chất lượng: coverage ≥ 70%, luồng chính ổn định, UX đơn giản, dễ dùng.

## Chương 5: Kết luận & hướng phát triển

### 5.1 Kết luận
- Đề tài khả thi với công nghệ Python server-side, đáp ứng nhu cầu nội bộ.
- Thiết kế dữ liệu và kiến trúc đơn giản giúp triển khai nhanh, dễ bảo trì.

### 5.2 Hướng phát triển
- Nâng cấp DB lên PostgreSQL; thêm cache tìm kiếm; bộ lọc nâng cao.
- Realtime chat (WebSocket), thông báo đẩy.
- Quản trị nội dung nâng cao, báo cáo vi phạm, audit log.
- Tích hợp lưu trữ đối tượng (S3/MinIO) cho media; CDN nội bộ.

## Tài liệu tham khảo
- S. A. McCandless, “Django for APIs,” 2nd ed., 2023.
- S. Tiangolo, “FastAPI documentation,” 2024. Truy cập: https://fastapi.tiangolo.com
- D. Beazley and B. Jones, “Python Cookbook,” 3rd ed., O’Reilly, 2013.
- D. Fowler, “Patterns of Enterprise Application Architecture,” Addison-Wesley, 2002.
- Django Software Foundation, “Django Documentation,” 2024. Truy cập: https://docs.djangoproject.com

Ghi chú: Tham khảo chuẩn, không trích Wikipedia; khi hoàn thiện sẽ bổ sung trích dẫn APA/IEEE đầy đủ theo các nguồn đã dùng trong quá trình triển khai.

## Phụ lục
- A. Mô tả ERD chi tiết, sơ đồ lớp, sequence diagrams.
- B. Cấu hình `.env` mẫu (đã ẩn thông tin nhạy cảm) và lệnh chạy.
- C. Test plan và danh sách test case chính.
- D. Hướng dẫn vận hành: backup media/DB, logging/monitoring.
