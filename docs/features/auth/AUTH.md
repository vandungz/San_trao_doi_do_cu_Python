# Xác thực và phân quyền

## Yêu cầu
- Đăng ký nội bộ (email domain tổ chức) hoặc import người dùng.
- Đăng nhập bằng email + mật khẩu, nhớ đăng nhập (session).
- CSRF bảo vệ form; rate limit đăng nhập.
- Hồ sơ người dùng: tên, phòng ban, avatar (tùy chọn).

## Vai trò (đơn giản)
- user: dùng hệ thống bình thường.
- moderator: duyệt/sửa/xoá tin vi phạm.
- admin: quản trị hệ thống.

## Luồng chính
- Đăng ký → xác nhận email (tùy chọn) → đăng nhập → cập nhật hồ sơ.
- Quên mật khẩu: gửi email đặt lại (token có hạn).

## Bảo mật
- Hash mật khẩu bằng PBKDF2/Argon2 (Django hỗ trợ sẵn).
- CSRF trên mọi POST form; HTTPS trong môi trường thật.
- Chặn upload avatar nguy hiểm; kiểm tra MIME và kích thước.

## Kiểm thử
- Test tạo user, login/logout, CSRF, phân quyền view.
