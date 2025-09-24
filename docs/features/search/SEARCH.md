# Tìm kiếm và lọc

## Trường tìm kiếm
- Từ khóa: tiêu đề + mô tả (LIKE đơn giản trên SQLite giai đoạn đầu).
- Bộ lọc: category, condition, khoảng giá (min/max), trạng thái hiển thị.
- Sắp xếp: mới nhất, giá tăng/giảm.

## Hiệu năng
- Thêm index trên (category, price, created_at).
- Giới hạn chiều dài truy vấn, chống wildcard quá rộng.

## UI/UX
- Form lọc bên trái, kết quả bên phải; giữ lại state filter khi paginate.
- Hiển thị số lượng kết quả; chips filter có thể xoá nhanh.

## Kiểm thử
- Kết hợp filter + sort; các biên: giá âm, min>max, từ khóa rỗng.
