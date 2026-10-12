# PHIẾU KIỂM TOÁN DỮ LIỆU THỰC TẾ

Nhóm 10 — IE313.F32.LT.CNTT — Phạm Quốc Thắng, Lê Minh Thiện.
Sinh tự động bởi `src/data_audit.py`; thời điểm UTC: 2026-10-11T14:49:30.453876+00:00.
Nguồn số liệu: `reports/audit/bangkok_audit_summary.json` và `bangkok_columns.csv`.

## 1. Kích thước và toàn vẹn

- **Tổng số dòng (quan trắc)**: `31,069` dòng.
- Số cột: 90; tổng số ô: 2,796,210.
- Tệp: `bangkok_listings_2026-06-29.csv.gz`; dung lượng: 20,625,983 bytes.
- SHA-256: `b17b99f9c421c566cc26a1c89a0b3d16b4c7f3dc74e659141900ccbac316b20e`; đối chiếu: **MATCH**.

## 2. Danh mục và ý nghĩa cột

Danh mục có 90 cột; 75 cột được đối chiếu với bản từ điển v4.3 lưu ở `docs/sources/`. Cột chưa có trong từ điển được ghi rõ trạng thái chưa xác minh.

| Nhóm nghiệp vụ | Số cột |
| --- | --- |
| id_source | 7 |
| host | 28 |
| location | 5 |
| property_room | 11 |
| price_quotes | 6 |
| availability_policy | 17 |
| reviews | 14 |
| estimates | 2 |

## 3. Kiểu dữ liệu thực tế

| Kiểu khi nạp | Số cột |
| --- | --- |
| float64 | 38 |
| str | 28 |
| int64 | 24 |

Không suy diễn đơn vị tiền tệ chỉ từ ký hiệu `$`. Chuyển giá sang số bằng parser có kiểm tra định dạng.

## 4. Giá trị khuyết

Tổng 581,427/2,796,210 ô khuyết (20.79%). Không mặc định lý do thiếu rating là listing mới.

| Cột | Số ô khuyết | % |
| --- | --- | --- |
| description | 579 | 1.86 |
| neighborhood_overview | 31,069 | 100 |
| host_profile_url | 2 | 0.01 |
| host_since | 31,069 | 100 |
| host_location | 8,025 | 25.83 |
| host_about | 11,988 | 38.59 |
| host_response_time | 31,069 | 100 |
| host_response_rate | 31,069 | 100 |
| host_acceptance_rate | 31,069 | 100 |
| host_thumbnail_url | 31,069 | 100 |
| host_neighbourhood | 31,069 | 100 |
| host_total_listings_count | 31,069 | 100 |
| host_verifications | 31,069 | 100 |
| neighbourhood | 31,069 | 100 |
| neighbourhood_group_cleansed | 31,069 | 100 |
| bathrooms | 4,122 | 13.27 |
| bathrooms_text | 143 | 0.46 |
| bedrooms | 3,897 | 12.54 |
| beds | 2,651 | 8.53 |
| price | 2,082 | 6.7 |
| price_quote_checkin_date | 1,319 | 4.25 |
| price_quote_checkout_date | 1,319 | 4.25 |
| price_quote_total_price | 2,082 | 6.7 |
| price_quote_price_per_night | 2,082 | 6.7 |
| price_quote_raw | 1,319 | 4.25 |
| minimum_nights | 2 | 0.01 |
| maximum_nights | 2 | 0.01 |
| minimum_minimum_nights | 2 | 0.01 |
| maximum_minimum_nights | 2 | 0.01 |
| minimum_maximum_nights | 2 | 0.01 |
| maximum_maximum_nights | 2 | 0.01 |
| calendar_updated | 31,069 | 100 |
| has_availability | 219 | 0.7 |
| estimated_revenue_l365d | 2,082 | 6.7 |
| first_review | 10,253 | 33 |
| last_review | 10,253 | 33 |
| review_scores_rating | 10,253 | 33 |
| review_scores_accuracy | 10,253 | 33 |
| review_scores_cleanliness | 10,253 | 33 |
| review_scores_checkin | 10,255 | 33.01 |
| review_scores_communication | 10,254 | 33 |
| review_scores_location | 10,255 | 33.01 |
| review_scores_value | 10,256 | 33.01 |
| license | 31,069 | 100 |
| instant_bookable | 31,069 | 100 |
| reviews_per_month | 10,253 | 33 |

## 5. Trùng lặp và đơn vị quan sát

ID đầy đủ và duy nhất, phù hợp cấu trúc Listing Snapshot. Tính duy nhất không chứng minh độc lập thống kê.
ID duy nhất: 31,069; dòng trùng ID: 0; dòng trùng toàn bộ: 0.
Ngày cào: 2026-06-29 đến 2026-07-02.

| Ngày | Số dòng |
| --- | --- |
| 2026-07-02 | 13,286 |
| 2026-06-29 | 9,656 |
| 2026-07-01 | 5,372 |
| 2026-06-30 | 2,755 |

## 6. Chất lượng và ngữ nghĩa giá

Có bằng chứng ký hiệu ฿ phù hợp Thái Baht (THB) trong snapshot Bangkok; đối chiếu định nghĩa giá bằng tiền địa phương của từ điển.
Mẫu quote: 100 chuỗi đầu tiên không khuyết; có 97 chuỗi mang ký hiệu ฿. Đây là mẫu thuận tiện, không phải mẫu ngẫu nhiên đại diện toàn bộ.

Toàn bộ cặp giá hữu hạn so sánh được khớp chính xác với báo giá theo đêm.
Cặp so sánh: 28987; khớp chính xác: 28987 (100%); khớp trong dung sai 0.05: 28,987; sai khác cực đại: 0.
Chưa xác minh đầy đủ thuế/phí cuối cùng. Giá niêm yết không phải giá giao dịch thực tế hay doanh thu.

Giá parse được: 28987; khuyết hoặc không parse được: 2082; giá bằng 0: 0; giá âm: 0.

## 7. Phân bố giá sơ bộ

Thống kê trên 28987 giá trị parse được, chưa cắt tỉa. Các chỉ số giá dùng đơn vị được kiểm chứng ở mục 6; skewness/kurtosis không có đơn vị. N/A là không đủ dữ liệu để tính.

| Chỉ số | Giá trị |
| --- | --- |
| Min | 1 |
| Q1 | 1,041.465 |
| Trung vị | 1,592 |
| Trung bình | 2,955.96 |
| Độ lệch chuẩn mẫu | 19,054.72 |
| Q3 | 2,539.565 |
| Max | 1,320,255 |
| IQR | 1,498.1 |
| Skewness | 52.3084 |
| Kurtosis (excess) | 3,093.8575 |

Ranh giới 1,5 IQR: -1,205.68 đến 4,786.72; số ngoại lệ: 2,730 (9.42%). Đây là dấu hiệu để kiểm tra, không phải tiêu chí tự động xóa.

## 8. Biến ứng viên

| Biến | Có mặt | Kiểu | Khuyết | Khuyết (%) | Giá trị duy nhất |
| --- | --- | --- | --- | --- | --- |
| price | 1 | str | 2,082 | 6.7 | 15,521 |
| room_type | 1 | str | 0 | 0 | 4 |
| property_type | 1 | str | 0 | 0 | 79 |
| neighbourhood_cleansed | 1 | str | 0 | 0 | 50 |
| accommodates | 1 | int64 | 0 | 0 | 16 |
| bedrooms | 1 | float64 | 3,897 | 12.54 | 25 |
| bathrooms | 1 | float64 | 4,122 | 13.27 | 32 |
| beds | 1 | float64 | 2,651 | 8.53 | 34 |
| minimum_nights | 1 | float64 | 2 | 0.01 | 95 |
| number_of_reviews | 1 | int64 | 0 | 0 | 436 |
| review_scores_rating | 1 | float64 | 10,253 | 33 | 150 |
| host_is_superhost | 1 | str | 0 | 0 | 2 |

## 9. Khả thi và điều kiện kiểm nghiệm

Các RQ chỉ khả thi khi có mẫu hợp lệ ở những biến tương ứng. Pearson phải báo cáo n, r, p và xem tính tuyến tính; ANOVA cần xem số mẫu, phân bố, phương sai và giới hạn độc lập. Chưa có kết quả kiểm định tại bước kiểm toán này.

## 10. Ma trận RQ — phương pháp — biểu đồ

| RQ | Biến | Phương pháp | Biểu đồ | Giới hạn |
|---|---|---|---|---|
| RQ1: Phân bố giá | price | Thống kê mô tả, IQR (Bài 05) | Histogram, boxplot | Giữ cực trị; ghi rõ phạm vi trục |
| RQ2: Giá theo loại phòng | price, room_type | Groupby; ANOVA khi đủ điều kiện | Boxplot, bar trung vị | Nhóm mất cân đối; host clustering |
| RQ3: Quy mô và giá | price, accommodates, bedrooms, bathrooms, beds | Pearson r–p, mẫu cặp hợp lệ | Scatter, heatmap | Khuyết, phi tuyến, cực trị |
| RQ4: Giá theo khu vực | price, neighbourhood_cleansed, room_type | Groupby, pivot | Bar, heatmap | So sánh trong loại phòng; ghi n |

Nguồn phương pháp/trang PDF theo `SPECIFICATION.md` mục 1.3–1.4. Chưa chọn feature mô hình từ EDA toàn bộ dữ liệu.

## 11. Giới hạn và bàn giao

Số host: 7,935; host có nhiều listing: 3,430 (43.23%); nhiều nhất 247 listing/host. Không coi ID duy nhất là bằng chứng độc lập; các kiểm định thường chỉ dùng thăm dò, không kết luận nhân quả.

Giữ snapshot, không suy rộng thành xu hướng thời gian. Không dùng `price_quote_*`, doanh thu ước tính, ID/URL hoặc biến tạo từ giá làm predictor. Phần imputer/scaler/chọn biến phải fit trong training fold, sau chia tập. Phương án làm sạch tại `CLEANING_PLAN.md`; notebook 01 là bước tiếp theo sau kiểm toán kỹ thuật.

Nguồn: [Inside Airbnb](https://insideairbnb.com/get-the-data/), [Data Dictionary v4.3](https://docs.google.com/spreadsheets/d/1iWCNJcSutYqpULSQHlNyGInUvHg2BoUGoNRIGa6Szc4/edit), [Data Assumptions](https://insideairbnb.com/data-assumptions/). Tọa độ nguồn được làm nhiễu, không dùng phân tích khoảng cách trong phạm vi đồ án.
