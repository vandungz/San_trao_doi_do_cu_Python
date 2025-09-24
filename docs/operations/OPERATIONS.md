# Vận hành

## Môi trường phát triển
- Python 3.11+, venv, SQLite.
- Biến môi trường trong `.env` (không commit):
  - SECRET_KEY, DEBUG, DATABASE_URL (tuỳ chọn), EMAIL_* cấu hình SMTP.

## Chạy dự án (sau khi có mã)
```bash
python -m venv .venv
. .venv/bin/activate  # Windows: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# django: python manage.py migrate && python manage.py runserver
# fastapi: uvicorn app.main:app --reload
```

## Build/Deploy tối giản
- Single node (VM hoặc container) nội bộ.
- Reverse proxy (nginx) → app (gunicorn/uvicorn) → SQLite/Postgres.
- Media lưu trên đĩa; backup định kỳ.

## Giám sát & nhật ký
- Log chuẩn stdout/stderr, quay vòng log.
- Sentry/OpenTelemetry (tùy chọn) khi cần.
