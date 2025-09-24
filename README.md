Sàn trao đổi đồ cũ nội bộ (Python)

Mục tiêu: xây dựng website cho phép nhân sự trong tổ chức đăng tin rao vặt đồ cũ, tìm kiếm/lọc, nhắn tin đơn giản giữa người mua-bán, và gửi thông báo email.

1) Tính năng cốt lõi (MVP)
- Đăng ký/đăng nhập, hồ sơ người dùng, xác thực phiên.
- Đăng tin: tiêu đề, mô tả, danh mục, giá, tình trạng, ảnh.
- Tìm kiếm và lọc: theo từ khóa, danh mục, tình trạng, khoảng giá, sắp xếp.
- Chat 1-1 cơ bản giữa người mua và người bán trong mỗi tin.
- Thông báo email: khi có tin nhắn mới, khi tin được duyệt, khi có quan tâm.

2) Phạm vi và giới hạn
- Nội bộ: chỉ người dùng thuộc domain tổ chức hoặc được mời.
- Media lưu local (dev) và có thể mở rộng S3/MinIO (prod) sau.
- Không xử lý thanh toán; chỉ kết nối trao đổi thông tin.

3) Công nghệ
- Backend: Django hoặc FastAPI + Jinja2 templates.
- CSDL: MySQL.
- Kiểm thử: pytest.
- Frontend: server-rendered templates (Django Templates), CSS tối giản.

Django: auth, admin, ORM, forms, templates có sẵn. Phần API ra FastAPI: realtime/async nâng cao. Tài liệu vẫn trung lập để chuyển đổi dễ dàng.

4) Cấu trúc tài liệu dự án
- docs/
  - architecture/ARCHITECTURE.md — sơ đồ cao cấp, quyết định thiết kế, ràng buộc phi chức năng.
  - features/
    - auth/AUTH.md — đăng ký, đăng nhập, vai trò, CSRF, session.
    - listings/LISTINGS.md — mô hình tin, upload media, duyệt tin, trạng thái.
    - search/SEARCH.md — chỉ mục, filter, sort, UX tìm kiếm.
    - chat/CHAT.md — mô hình hội thoại, bảo mật.
    - notifications/NOTIFICATIONS.md — mail templates, trigger, cấu hình SMTP.
  - testing/TESTING.md — chiến lược pytest, coverage, dữ liệu giả.
  - operations/OPERATIONS.md — môi trường, chạy dev/test, deploy thô.
  - data/DATA_MODEL.md — lược đồ dữ liệu, khóa, ràng buộc.

5) Yêu cầu hệ thống (dev)
- Python 3.11+
- pip, venv
- SQLite3 (thường có sẵn)

6) Khởi tạo môi trường (tạm thời vì chưa có mã)
```bash
python -m venv .venv
. .venv/bin/activate  # Windows PowerShell: .\.venv\Scripts\Activate.ps1
pip install -U pip
# Sẽ thêm requirements.txt sau khi tạo skeleton mã nguồn
```

7) Quy ước mã nguồn và nhánh Git
- đặt tên module, app ngắn gọn, có nghĩa; snake_case cho file Python.
- type hints đầy đủ cho public API.
- quy trình Git: main (ổn định), develop (tích hợp), feature/* (nhánh tính năng), test CI với pytest.

8) Phân công vai trò (gợi ý)
- Kiến trúc + Auth: thiết kế tổng thể, chọn Django/FastAPI, dựng auth, bảo mật.
- Đăng tin + Media: mô hình tin, form, upload ảnh, duyệt và quản lý.
- Tìm kiếm + Filter: query, filter, sort, UX tìm kiếm, pagination.
- Chat + Test: mô hình chat đơn giản, hộp thoại theo tin, viết test pytest.

9) Lộ trình đề xuất
- Milestone 0: Tài liệu và skeleton
- Milestone 1: Auth + khởi tạo app
- Milestone 2: Listings + Upload
- Milestone 3: Search/Filter + Pagination
- Milestone 4: Chat + Email notifications
- Milestone 5: Ổn định, test, dọn dẹp & demo

10) Kiểm thử & Chất lượng
- pytest: test đơn vị, test tích hợp (ORM, views), factory dữ liệu.
- coverage mục tiêu ≥ 70% giai đoạn đầu.
- pre-commit (flake8/ruff, black/isort) — bổ sung khi có mã.

11) Bảo mật & riêng tư
- bắt buộc xác thực nội bộ, CSRF, session timeout hợp lý.
- lọc nội dung và kích thước file upload; hạn chế loại file.
- ẩn email thật trong giao dịch giữa người dùng nếu cần.

13) Chạy test
```powershell
pytest -q
```

14) Cấu trúc dự án (tree rút gọn)
```text
.
├─ marketplace/              # Project module (config)
│  ├─ __init__.py
│  ├─ settings.py            # Cấu hình Django (SQLite dev, templates, static)
│  ├─ urls.py                # Router gốc, include các app
│  ├─ asgi.py                # Entry ASGI
│  └─ wsgi.py                # Entry WSGI
├─ accounts/                 # Auth + hồ sơ cơ bản
│  ├─ urls.py                # /accounts/login|register|profile
│  └─ views.py               # view placeholder
├─ listings/                 # Tin rao vặt (list/create/detail)
│  ├─ urls.py                # /listings/
│  └─ views.py               # view placeholder
├─ chat/                     # Chat 1-1 theo tin
│  ├─ urls.py                # /chat/
│  └─ views.py               # view placeholder
├─ templates/
│  ├─ home.html              # Trang chủ + điều hướng nhanh
│  ├─ accounts/
│  │  ├─ login.html
│  │  ├─ register.html
│  │  └─ profile.html
│  ├─ listings/
│  │  ├─ list.html
│  │  ├─ create.html
│  │  └─ detail.html
│  └─ chat/
│     ├─ threads.html
│     └─ thread_detail.html
├─ tests/
│  └─ test_smoke.py          # Test smoke trang chủ
├─ manage.py                 # CLI Django
├─ requirements.txt          # Phụ thuộc (được tạo sau khi cài)
├─ pytest.ini                # Cấu hình pytest/pytest-django
└─ .gitignore
```

15) Các route chính (dev hiện tại)
- Trang chủ: `/`
- Admin: `/admin/`
- Accounts: `/accounts/login/`, `/accounts/register/`, `/accounts/profile/`
- Listings: `/listings/`, `/listings/create/`, `/listings/<id>/`
- Chat: `/chat/`, `/chat/<id>/`

16) Điều kiện tiên quyết
- Python 3.11+ (khuyến nghị)
- PowerShell (Windows) hoặc shell tương đương

17) Thiết lập nhanh (Windows PowerShell)
```powershell
# 1) Tạo & kích hoạt venv
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2) Đảm bảo pip có sẵn và cập nhật
python -m ensurepip --upgrade
python -m pip install -U pip setuptools wheel

# 3) Cài phụ thuộc tối thiểu và tạo requirements.txt
python -m pip install django

# 4) Khởi tạo database & chạy server
python manage.py migrate
python manage.py runserver
```
- Truy cập: http://127.0.0.1:8000/

18) Lệnh hữu ích (tùy chọn, không cần làm theo)
```powershell
# Tạo tài khoản admin
python manage.py createsuperuser

# Chạy test
pytest -q

# (Tuỳ chọn) Tạo migration sau khi thêm model
python manage.py makemigrations
python manage.py migrate
```

19) Sự cố thường gặp (Troubleshooting)
- "ModuleNotFoundError: No module named 'django'": bạn đang dùng sai Python.
  - Cách khắc phục nhanh (không cần activate):
    ```powershell
    .\.venv\Scripts\python.exe -m ensurepip --upgrade
    .\.venv\Scripts\python.exe -m pip install -U pip setuptools wheel
    .\.venv\Scripts\python.exe -m pip install django pytest pytest-django python-dotenv
    .\.venv\Scripts\python.exe manage.py migrate
    .\.venv\Scripts\python.exe manage.py runserver
    ```
  - Kiểm tra interpreter đang dùng:
    ```powershell
    python -c "import sys; print(sys.executable)"
    ```
    Phải trỏ tới `...\.venv\Scripts\python.exe`.
- "requirements.txt not found": tạo sau khi cài gói bằng `python -m pip freeze > requirements.txt`.
- "execution policy" khi kích hoạt venv:
  - Mở PowerShell với quyền admin và chạy: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- Port 8000 đang dùng: đổi port `python manage.py runserver 8001`.

20) Định hướng phát triển tiếp
- Thêm model `Listing`, `Conversation`, `Message`, và liên kết `User`.
- Form & validation; upload ảnh; phân trang listings; bảo vệ route bằng login.
- Email notifications và unit/integration tests theo `docs/`.


