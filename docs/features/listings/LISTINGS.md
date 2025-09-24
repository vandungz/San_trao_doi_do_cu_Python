# Tin đăng và media

## Mô hình dữ liệu cơ bản
- Listing: title, description, category, price, condition, status, owner, created_at, updated_at.
- ListingImage: listing_id, image_path, alt_text, order.
- Category: name, slug (tĩnh hoặc seed sẵn).

## Luồng tính năng
- Tạo tin: form, upload nhiều ảnh, preview.
- Duyệt tin: moderator có thể duyệt/ẩn.
- Sửa/Xoá: chủ tin có quyền trong trạng thái cho phép.

## Ràng buộc/Quy tắc
- Giới hạn ảnh: tối đa N ảnh, dung lượng tối đa M MB/ảnh.
- Kiểm tra định dạng: jpg/png/webp; từ chối executable.
- Sanitization mô tả (allowlist HTML tối thiểu hoặc plain text).

## UX đề xuất
- Thẻ trạng thái: Đang bán, Đã bán, Ẩn.
- Breadcrumb danh mục; hiển thị giá rõ ràng.
- Pagination: 12–24 tin/trang.

## Kiểm thử
- Tạo/sửa/xoá tin, upload ảnh hợp lệ/không hợp lệ, quyền truy cập.
