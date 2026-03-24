# Kế hoạch sản phẩm: Nền tảng Food Review Realtime đa nền tảng

## 1) Làm rõ lại ý tưởng theo yêu cầu mới

Bạn muốn sản phẩm theo hướng **Map + Community Ranking**, không cần feed theo follow. Mô hình phù hợp:

- Bản đồ là trung tâm trải nghiệm
- Sidebar trái là **bảng xếp hạng cộng đồng user/reviewer**
- Viewer có thể search/click user để xem profile và toàn bộ review chi tiết
- Viewer có thể click địa điểm hot trên bản đồ để xem review liên quan
- Tất cả địa điểm do user tạo đều public cho toàn hệ thống
- User có thể tự mark địa điểm hot và share cho người khác

---

## 2) Phạm vi MVP (3–4 tháng)

### Tính năng bắt buộc
- Đăng ký/đăng nhập
- Hồ sơ user/reviewer (online/offline, tổng bài review, sao vàng, sao chổi, tỷ lệ vàng/chổi)
- **Mọi user đều có thể review và mark địa điểm** (không tách vai trò reviewer riêng)
- Tạo địa điểm quán ăn trên map (public toàn hệ thống)
- Click vào địa điểm để xem **thông tin quán chi tiết** (tên, địa chỉ, tag, giờ mở cửa nếu có)
- Xem danh sách review của địa điểm (sao, nội dung, tác giả, thời gian)
- Xem **dữ liệu hình ảnh** của địa điểm/review (gallery ảnh)
- Tạo review cho địa điểm (mỗi review có: sao, địa điểm, nội dung, hình ảnh tuỳ chọn)
- Bảng xếp hạng cộng đồng user theo:
  - số sao vàng
  - tỷ lệ `gold/comet` cao
- Search user + vào profile để xem tất cả bài review
- Đánh dấu địa điểm hot và share danh sách hot place
- **Tra cứu đường đi trên map như Google Maps** (chọn điểm đi/đến, ưu tiên tuyến tối ưu)

### Realtime trong MVP
- Trạng thái online/offline user realtime
- Bảng xếp hạng cập nhật gần realtime khi có review/điểm mới
- Số liệu điểm hot của địa điểm cập nhật gần realtime trên map
- Kết quả route cập nhật theo vị trí/điều kiện tìm đường gần realtime (nếu provider hỗ trợ)

---

## 3) Kiến trúc đề xuất (đúng stack yêu cầu)

## FE
- **Mobile**: Flutter (iOS/Android)
- **Web**: React + TypeScript
- Giao diện web:
  - trái: leaderboard user/reviewer
  - phải: map + hot places + detail panel + chỉ đường

## BE
- **Django + DRF**: REST API
- **Django Channels + Redis**: WebSocket realtime
- **Celery**: tính điểm/bảng xếp hạng, tác vụ nền

## DB
- **PostgreSQL**
- Extension khuyến nghị:
  - `PostGIS` cho truy vấn địa lý
  - `pg_trgm` cho search gần đúng

## DevOps
- Docker cho môi trường dev/staging/prod
- Git workflow (trunk-based hoặc GitFlow)
- CI/CD pipeline (lint/test/build/deploy)

---

## 4) Thiết kế module chức năng

- **Auth & Profile**
- **Place Service**
  - tạo/sửa địa điểm
  - public toàn hệ thống
  - trả thông tin chi tiết quán khi user click marker
- **Review Service**
  - quản lý review theo reviewer và địa điểm
  - hỗ trợ media attachment (ảnh review)
- **Media Service**
  - upload/resize/store ảnh
  - phục vụ gallery ảnh cho place/review
- **Community Ranking Service**
  - tính sao vàng/sao chổi
  - tính tỷ lệ vàng/chổi
  - trả về leaderboard
- **Hot Place Service**
  - mark địa điểm hot
  - tổng hợp độ hot theo thời gian
  - chia sẻ danh sách hot
- **Routing Integration Service**
  - tích hợp provider chỉ đường (Google Maps/Mapbox/OSRM)
  - tính tuyến tối ưu theo điều kiện
- **Realtime Gateway**
  - presence
  - leaderboard updates
  - hot-place score updates

> Giai đoạn đầu nên làm Django modular monolith để ship nhanh, sau đó tách service khi tăng tải.

---

## 5) Mô hình dữ liệu cốt lõi (PostgreSQL)

- `users`
- `user_reputation_stats`
  - `total_reviews`
  - `gold_stars`
  - `comet_stars`
  - `gold_comet_ratio`
- `places`
  - `name, lat, lng, address, created_by, is_public`
- `reviews`
  - `user_id, place_id, star, content, created_at`
- `review_media`
  - `review_id, media_url, media_type, metadata`
- `place_media`
  - `place_id, media_url, source_user_id, metadata`
- `place_hot_marks`
  - user đánh dấu địa điểm hot
- `shared_hot_lists`
  - danh sách địa điểm hot user muốn share
- `shared_hot_list_items`
- `user_presence`
- `activity_events` (phục vụ realtime + audit)

Index quan trọng:
- `places` dùng `GIST` index (PostGIS)
- `reviews(user_id, created_at DESC)`
- `reviews(place_id, created_at DESC)`
- `review_media(review_id)`
- `place_media(place_id)`
- `user_reputation_stats(gold_comet_ratio DESC, gold_stars DESC)`
- `place_hot_marks(place_id, created_at DESC)`

---

## 6) Luồng nghiệp vụ chính

### A) Cập nhật bảng xếp hạng cộng đồng
1. User tạo review
2. Hệ thống cập nhật `reviews`
3. Worker tính lại `user_reputation_stats`
4. Broadcast leaderboard delta qua WebSocket
5. Web/App cập nhật sidebar trái gần realtime

### B) Xem profile user/reviewer
1. Viewer search/click user từ leaderboard
2. API trả profile + stats + danh sách review
3. Viewer xem chi tiết từng bài (sao, địa điểm, review)

### C) Hot place trên map
1. User mark địa điểm hot
2. Hệ thống tăng hot score địa điểm
3. Event realtime push về client
4. Map đổi badge/mức độ hot tức thì

### D) Tra cứu đường đi trên map
1. User chọn điểm đi/điểm đến (hoặc vị trí hiện tại -> quán)
2. Backend gọi dịch vụ routing provider
3. Trả về 1..n tuyến đường + ETA + quãng đường
4. User chọn tuyến tối ưu theo tiêu chí (nhanh nhất/ngắn nhất/ít rẽ)

### E) Click địa điểm để xem chi tiết quán + review + ảnh
1. User click marker địa điểm trên map
2. API trả `place_detail` gồm metadata quán
3. API trả danh sách review của quán (paging)
4. API trả gallery ảnh (ảnh từ chủ địa điểm + ảnh từ review)
5. Client mở detail panel/modal và render đầy đủ thông tin

---

## 7) API contract gợi ý (v1)

- `GET /api/v1/leaderboard/users`
- `GET /api/v1/users/{id}`
- `GET /api/v1/users/{id}/reviews`
- `POST /api/v1/places`
- `GET /api/v1/places?bbox=...`
- `GET /api/v1/places/{id}` (chi tiết quán)
- `GET /api/v1/places/{id}/media`
- `POST /api/v1/reviews`
- `GET /api/v1/places/{id}/reviews`
- `POST /api/v1/reviews/{id}/media`
- `POST /api/v1/places/{id}/hot-marks`
- `POST /api/v1/hot-lists`
- `POST /api/v1/hot-lists/{id}/share`
- `POST /api/v1/routes` (origin, destination, mode)

Socket channels:
- `presence:{user_id}`
- `leaderboard:global`
- `places:hot:{region}`
- `routes:{user_id}` (tuỳ chọn khi cần realtime reroute)

---

## 8) Quy tắc tính sao vàng / sao chổi (đề xuất thực dụng)

- Sao vàng tăng khi review nhận tương tác hữu ích, chất lượng ổn định
- Sao chổi tăng khi bị report hợp lệ/spam
- Tỷ lệ hiển thị:

`gold_comet_ratio = (gold_stars + 1) / (comet_stars + 1)`

Xếp hạng ưu tiên:
1. ratio cao
2. gold_stars cao
3. total_reviews đủ ngưỡng tối thiểu (tránh tài khoản mới leo top ảo)

---

## 9) Lộ trình kỹ thuật 12 tuần

### Sprint 1–2
- Setup Django + React + Flutter skeleton
- Docker compose local
- Auth + profile cơ bản

### Sprint 3–4
- Place CRUD + map render
- Place detail panel khi click marker
- Review CRUD + upload ảnh review

### Sprint 5–6
- Ranking service + leaderboard UI
- Profile user + list review theo user

### Sprint 7–8
- Hot place mark + share list
- Presence realtime + leaderboard realtime

### Sprint 9–10
- Search tối ưu + query tuning Postgres
- Cache Redis cho leaderboard/hot places

### Sprint 11–12
- Hardening bảo mật
- Load test + release staging/prod

---

## 10) CI/CD pipeline

PR:
1. Lint (Python/TS/Dart)
2. Unit test
3. Build Docker image

Main:
1. Integration test
2. Deploy staging
3. Smoke test

Tag release:
1. Deploy production
2. Post-deploy checks

---

## 11) Scale & đồng bộ dữ liệu

- Một backend API chung cho web/app
- Redis cache cho leaderboard và hot places
- PostgreSQL read-replica cho truy vấn đọc nặng
- Worker tách riêng để tính ranking/hot score
- Dùng event + websocket để giảm polling và giữ dữ liệu đồng bộ gần realtime

---

## 12) Cấu trúc repo gợi ý

```
food-review-platform/
  backend/
  web/
  mobile/
  infra/
    docker/
    pipeline/
  docs/
```

---

## 13) KPI MVP

- p95 API latency
- tần suất cập nhật leaderboard thành công
- tỉ lệ đồng bộ realtime thành công (socket delivery)
- số địa điểm hot được tạo và share
- CTR click marker -> mở place detail
- retention D7/D30

---

## 14) Next steps thực thi ngay

1. Chốt công thức leaderboard cộng đồng (mọi user đều tham gia).
2. Chốt routing provider (Google Maps/Mapbox/OSRM) và chính sách chi phí.
3. Vẽ ERD + migration plan cho Postgres/PostGIS.
4. Dựng API contract OpenAPI v1.
5. Làm end-to-end flow đầu tiên:
   - create place -> create review -> recalc ranking -> realtime update leaderboard -> route to place.

## 15) Wireframe tham chiếu

- Xem phác thảo giao diện chi tiết tại: `docs/ui-wireframes.md`.
- Bao gồm web desktop, mobile, place detail (info/reviews/photos), leaderboard và route panel.

