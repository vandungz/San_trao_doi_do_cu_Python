# Mô hình dữ liệu (phác thảo)

## Bảng Users
- id, email (unique, nội bộ), password_hash, name, department, role, avatar_path, created_at.

## Bảng Listings
- id, owner_id (FK Users), title, description, category, price (decimal), condition (enum), status (enum), created_at, updated_at.

## Bảng ListingImages
- id, listing_id (FK Listings), image_path, alt_text, order.

## Bảng Conversations
- id, listing_id (FK Listings), buyer_id (FK Users), seller_id (FK Users), created_at.

## Bảng Messages
- id, conversation_id (FK Conversations), sender_id (FK Users), text, created_at, read_at nullable.

## Chỉ mục đề xuất
- Listings(category), Listings(price), Listings(created_at)
- Messages(conversation_id, created_at)

## Ràng buộc toàn vẹn
- seller_id phải là owner của listing trong conversation.
- price >= 0; điều kiện và trạng thái theo enum.
- Xoá mềm listings (status=hidden) thay vì xoá vật lý nếu cần.
