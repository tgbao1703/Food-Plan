# Kế hoạch dự án Food Review Realtime (Markdown)

## 1. Bối cảnh và mục tiêu

Dự án xây dựng một nền tảng food review realtime đa nền tảng, với trải nghiệm chính xoay quanh bản đồ và khám phá cộng đồng reviewer.

Mục tiêu kinh doanh và sản phẩm:
- Giúp người dùng tìm quán nhanh theo vị trí.
- Tăng độ tin cậy quyết định đi ăn bằng xếp hạng reviewer.
- Tạo hành vi sử dụng lặp lại thông qua review, hot places, và chia sẻ danh sách.

---

## 2. Ý tưởng sản phẩm đã chốt

Sản phẩm theo mô hình **Map + Community Ranking**:
- Bản đồ là trung tâm trải nghiệm.
- Người dùng có thể click marker để xem chi tiết quán, review và ảnh.
- Sidebar (web) hiển thị leaderboard user/reviewer.
- Mọi user đều có thể tạo place, review, mark hot.
- Có điều hướng đường đi như Google Maps.

Phạm vi này đã thay thế hướng feed/follow ở giai đoạn đầu để giảm độ phức tạp và tăng tốc ra mắt.

---

## 3. Phạm vi MVP (3–4 tháng)

Các năng lực bắt buộc trong MVP:
- Đăng ký/đăng nhập.
- Hồ sơ user/reviewer: online/offline, tổng review, sao vàng, sao chổi, tỷ lệ vàng/chổi.
- Tạo địa điểm quán ăn trên map (public toàn hệ thống).
- Tạo review kèm sao, nội dung, ảnh tùy chọn.
- Xem chi tiết địa điểm: thông tin quán, review, gallery ảnh.
- Xếp hạng cộng đồng theo gold stars và gold/comet ratio.
- Search user và xem profile review chi tiết.
- Mark hot place và share danh sách hot.
- Tra cứu đường đi origin/destination và chọn tuyến phù hợp.

Yêu cầu realtime trong MVP:
- Cập nhật trạng thái online/offline user.
- Cập nhật leaderboard gần realtime.
- Cập nhật độ hot của địa điểm gần realtime.

---

## 4. Kiến trúc công nghệ

### Frontend
- Mobile: Flutter (iOS/Android).
- Web: React + TypeScript.

### Backend
- Django + Django REST Framework cho API.
- Django Channels + Redis cho realtime.
- Celery cho background jobs (tính điểm, xử lý tác vụ nền).

### Database
- PostgreSQL là DB chính.
- PostGIS cho truy vấn địa lý.
- pg_trgm cho search gần đúng.

### DevOps
- Docker cho local/staging/production parity.
- Git + CI/CD pipeline cho kiểm thử và triển khai.

---

## 5. Thiết kế module nghiệp vụ

- Auth & Profile
- Place Service
- Review Service
- Media Service
- Community Ranking Service
- Hot Place Service
- Routing Integration Service
- Realtime Gateway

Chiến lược kỹ thuật: bắt đầu bằng modular monolith để ra mắt nhanh, sau đó tách service theo tải thực tế.

---

## 6. Mô hình dữ liệu cốt lõi

Các thực thể chính:
- users
- user_reputation_stats
- places
- reviews
- review_media
- place_media
- place_hot_marks
- shared_hot_lists
- shared_hot_list_items
- user_presence
- activity_events

Các chỉ mục quan trọng:
- GIST index cho places (geo).
- Index reviews theo user/time và place/time.
- Index cho bảng reputation phục vụ leaderboard.
- Index media và hot marks phục vụ truy vấn chi tiết.

---

## 7. Luồng nghiệp vụ chính

### 7.1 Cập nhật leaderboard
1. User tạo review.
2. Hệ thống ghi review.
3. Worker tính lại user_reputation_stats.
4. Push leaderboard delta qua WebSocket.
5. Client cập nhật gần realtime.

### 7.2 Xem profile user/reviewer
1. Viewer chọn user từ leaderboard/search.
2. API trả profile + stats + reviews.
3. Viewer xem chi tiết bài review theo sao/địa điểm.

### 7.3 Hot place
1. User mark địa điểm hot.
2. Hệ thống tăng hot score.
3. Client nhận update và đổi badge trên map.

### 7.4 Route
1. User chọn điểm đi và điểm đến.
2. Backend gọi routing provider.
3. Trả tuyến đường, ETA, quãng đường.

### 7.5 Place detail
1. User click marker.
2. API trả metadata quán.
3. API trả review list + gallery ảnh.
4. Client render detail panel/bottom sheet.

---

## 8. API contract v1 (định hướng)

- `GET /api/v1/leaderboard/users`
- `GET /api/v1/users/{id}`
- `GET /api/v1/users/{id}/reviews`
- `POST /api/v1/places`
- `GET /api/v1/places?bbox=...`
- `GET /api/v1/places/{id}`
- `GET /api/v1/places/{id}/media`
- `POST /api/v1/reviews`
- `GET /api/v1/places/{id}/reviews`
- `POST /api/v1/reviews/{id}/media`
- `POST /api/v1/places/{id}/hot-marks`
- `POST /api/v1/routes`

Socket channels:
- `presence:{user_id}`
- `leaderboard:global`
- `places:hot:{region}`

---

## 9. Định hướng giao diện (UI/UX)

### Web
- Cột trái: leaderboard user.
- Khu trung tâm: map + markers.
- Cột phải: panel chi tiết quán (Info/Reviews/Photos/Route).

### Mobile
- Bottom navigation: Map / Ranking / Create / Saved Hot / Profile.
- Place detail hiển thị dưới dạng bottom sheet.

Mục tiêu UX:
- Từ khám phá quán -> xem bằng chứng review/ảnh -> định tuyến -> hành động đi ăn.

---

## 10. Lộ trình triển khai 12 tuần

- Sprint 1–2: setup skeleton + auth/profile.
- Sprint 3–4: place/review CRUD + place detail + ảnh.
- Sprint 5–6: ranking service + leaderboard UI + profile review list.
- Sprint 7–8: hot place + share + realtime.
- Sprint 9–10: search optimization + DB tuning + cache.
- Sprint 11–12: hardening bảo mật + load test + release.

---

## 11. CI/CD và vận hành

Pipeline đề xuất:
- PR: lint + unit test + build image.
- Main: integration + deploy staging + smoke test.
- Release tag: deploy production + post-deploy checks.

Vận hành/scale:
- API stateless.
- Redis cache.
- PostgreSQL read replica khi tăng tải.
- Worker tách riêng cho ranking/hot score.

---

## 12. KPI thành công MVP

- p95 API latency.
- Tỷ lệ cập nhật leaderboard thành công.
- Tỷ lệ realtime delivery thành công.
- Số hot place được tạo và share.
- CTR click marker -> mở place detail.
- Retention D7/D30.

---

## 13. Rủi ro chính và hướng giảm thiểu

Rủi ro:
- Chất lượng review không đồng đều.
- Spam/abuse khi ranking mở cho toàn user.
- Chi phí routing provider tăng nhanh theo traffic.

Giảm thiểu:
- Report/moderation sớm trong MVP.
- Ngưỡng review tối thiểu cho tài khoản trước khi vào top.
- Theo dõi chi phí route request và tối ưu cache.

---

## 14. Next steps để bắt đầu build ngay

1. Chốt công thức leaderboard chính thức.
2. Chốt routing provider và chi phí.
3. Hoàn thiện ERD + migration plan.
4. Chốt OpenAPI v1 để FE/BE làm song song.
5. Triển khai flow E2E đầu tiên:
   - create place -> create review -> recalc ranking -> realtime update -> route to place.
