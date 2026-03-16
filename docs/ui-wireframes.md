# Phác thảo giao diện (Wireframe) cho Food Review Map App

> Ghi chú: Tài liệu này dùng để chuyển nhanh sang Figma/Canvas. Tập trung MVP: map-centric, leaderboard, place detail, review + media, routing.

## 1) Web App — Trang chính (Desktop)

## 1.1 Bố cục tổng thể

| Khu vực | Thành phần | Mục tiêu |
|---|---|---|
| Header | Logo, ô search, user menu | Điều hướng và tìm nhanh quán/user |
| Left Sidebar | Community Leaderboard | Khám phá reviewer/user top |
| Main Map | Bản đồ + marker hot place | Trải nghiệm trung tâm |
| Right Panel | Place Detail / Route Panel (tab) | Xem thông tin quán, review, ảnh, chỉ đường |

### ASCII Wireframe

```text
+------------------------------------------------------------------------------------------------+
| LOGO | [Search: quán, khu vực, user...]                         [Notifications] [Avatar/Menu] |
+-----------------------------+-----------------------------------------------+------------------+
| LEADERBOARD (Top Users)     |                                               | PLACE DETAIL     |
| 1. @linhfood  ⭐120 ☄️10     |                MAP VIEW                        | [Tab Info]       |
| 2. @anreview  ⭐110 ☄️12     |      (hot markers + normal markers)            | [Tab Reviews]    |
| 3. @minheat   ⭐100 ☄️8      |                                               | [Tab Photos]     |
| ...                         |                                               | [Tab Route]      |
| [Filter: khu vực, tuần]     |                                               |                  |
+-----------------------------+-----------------------------------------------+------------------+
```

---

## 2) Web App — Place Detail Panel

### 2.1 Tab Info (Thông tin quán)

| Field | Ví dụ |
|---|---|
| Tên quán | Bún Chả Hà Nội 37 |
| Địa chỉ | 123 Nguyễn Trãi, Q1 |
| Giờ mở cửa | 07:00 - 22:00 |
| Tags | Bún chả, bình dân, gia đình |
| Điểm tổng hợp | 4.3/5 |
| Nút thao tác | Mark Hot, Share, Route to here |

```text
+---------------------------------------+
| Bún Chả Hà Nội 37                     |
| ⭐ 4.3 (1,245 reviews)   [Mark Hot]   |
| 123 Nguyễn Trãi, Q1      [Share]      |
| 07:00 - 22:00            [Route]      |
| Tags: #buncha #local #cheap           |
+---------------------------------------+
```

### 2.2 Tab Reviews

| Thành phần | Nội dung |
|---|---|
| Bộ lọc | Mới nhất, nhiều sao, có ảnh |
| Item review | Avatar, tên user, sao, nội dung, ảnh, thời gian |
| CTA | Viết review |

```text
+--------------------------------------------------+
| Reviews [Newest v] [Has Photos] [⭐4+ ]          |
|--------------------------------------------------|
| @linhfood   ⭐⭐⭐⭐⭐   2 giờ trước                   |
| Nước dùng đậm vị, quán sạch, phục vụ nhanh.      |
| [img1] [img2]                                    |
|--------------------------------------------------|
| @anreview   ⭐⭐⭐⭐    1 ngày trước                 |
| Giá ổn, hơi đông giờ trưa.                       |
+--------------------------------------------------+
```

### 2.3 Tab Photos

| Thành phần | Nội dung |
|---|---|
| Grid ảnh | 3-4 cột desktop |
| Bộ lọc ảnh | Ảnh món ăn / không gian / menu |
| Tương tác | Mở lightbox, next/prev |

### 2.4 Tab Route

| Field | Mô tả |
|---|---|
| Origin | Vị trí hiện tại / điểm nhập tay |
| Destination | Tự động là quán đang xem |
| Mode | Driving / Walking / Bike |
| Route options | Nhanh nhất, ngắn nhất |
| Output | ETA, distance, polyline |

```text
+-----------------------------------------------+
| Route to: Bún Chả Hà Nội 37                   |
| From: [Current Location v]                    |
| Mode: (•) Drive ( ) Walk ( ) Bike             |
|-----------------------------------------------|
| Option A: 18 min | 5.2 km | Fastest           |
| Option B: 22 min | 4.8 km | Shortest          |
| [Start Navigation]                            |
+-----------------------------------------------+
```

---

## 3) Mobile App (Flutter) — Màn hình chính

## 3.1 Bottom Navigation

| Tab | Mục đích |
|---|---|
| Map | Bản đồ + marker + mở place detail bottom sheet |
| Ranking | Bảng xếp hạng user |
| Create | Tạo place/review |
| Saved Hot | Danh sách hot đã lưu/share |
| Profile | Hồ sơ cá nhân + thống kê sao |

### ASCII Wireframe (Mobile)

```text
+-------------------------------+
| [Search...]                   |
|-------------------------------|
|           MAP                 |
|      (markers here)           |
|                               |
|-------------------------------|
|  Map | Rank | + | Hot | Me    |
+-------------------------------+
```

## 3.2 Place Detail Bottom Sheet

```text
+-------------------------------+
| Bún Chả Hà Nội 37      ⭐4.3   |
| 123 Nguyễn Trãi, Q1           |
| [Mark Hot] [Share] [Route]    |
|-------------------------------|
| Tabs: Info | Reviews | Photos |
| ... content ...               |
+-------------------------------+
```

---

## 4) Luồng UX chính (MVP)

| Flow | Bước |
|---|---|
| Khám phá quán hot | Mở map -> click marker hot -> xem info/reviews/photos -> mark hot/share |
| Xem người review tốt | Mở leaderboard -> click user -> xem profile + reviews |
| Dẫn đường đến quán | Click marker/place detail -> Route tab -> chọn route -> Start Navigation |
| Tạo nội dung | Nút Create -> tạo place hoặc review + upload ảnh |

---

## 5) Design tokens gợi ý (để chuyển Figma nhanh)

| Token | Giá trị gợi ý |
|---|---|
| Primary | `#FF5A1F` |
| Accent Hot | `#FFB703` |
| Background | `#F8F9FB` |
| Text Primary | `#1F2937` |
| Radius | 12px |
| Spacing scale | 4 / 8 / 12 / 16 / 24 / 32 |

---

## 6) Checklist chuyển sang Figma/Canvas

- Tạo 1 page `MVP-Wireframes`
- Tạo 5 frame chính:
  - `Web-Home-Map-Leaderboard`
  - `Web-Place-Detail`
  - `Web-Route-Panel`
  - `Mobile-Map`
  - `Mobile-Place-BottomSheet`
- Dùng Auto-layout cho panel/list
- Component hoá:
  - `UserRankItem`
  - `PlaceMarker`
  - `ReviewCard`
  - `RouteOptionCard`

---

## 7) Bước tiếp theo

1. Chốt user journey ưu tiên (desktop trước hay mobile trước).
2. Mình có thể tách tiếp thành **UI spec theo từng màn** (states/loading/empty/error).
3. Sau đó sinh luôn backlog ticket (Jira/Trello) theo component + API mapping.
