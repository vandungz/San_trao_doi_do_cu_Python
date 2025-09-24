# Chat đơn giản

## Phạm vi
- Chat 1-1 giữa người mua và người bán, gắn với một tin đăng.
- Realtime.

## Mô hình dữ liệu
- Conversation: listing_id, buyer_id, seller_id, created_at.
- Message: conversation_id, sender_id, text, created_at, read_at (nullable).

## Luồng
- Người mua mở chat từ trang tin → tạo conversation nếu chưa có.
- Gửi/nhận tin nhắn dạng text; giới hạn độ dài và chống XSS.

## Bảo mật
- Chỉ các bên trong conversation mới xem được nội dung.
- Ẩn email/số điện thoại cho đến khi người dùng tự chia sẻ.

## Kiểm thử
- Tạo hội thoại, gửi/nhận tin nhắn, phân quyền truy cập.
