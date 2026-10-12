# Phát hiện EDA — Nhóm 10

Bản cập nhật sau review ngày 11/10/2026. Sinh từ artifact máy đọc bằng `src/eda_report.py`.
Baseline: 28,987 × 16; SHA-256 `961a01ad225e35f989ec81f124925488e392baca2ef3800ff4028b4423d5f9a7`.
Phương pháp, tham số, nguồn và phần mở rộng: [EDA_METHODS.md](../docs/EDA_METHODS.md).

## 1. RQ1 — Giá phân bố lệch phải

Trên n=28,987, giá trung vị **1,592.00 THB/đêm**, trung bình 2,955.96; Q1–Q3 là 1,041.47–2,539.57; min–max 1.00–1,320,255.00. Std mẫu 19,054.72, CV 644.62%; skewness 52.3111 và excess kurtosis 3094.3914 dùng bias=False. Các moment này khác audit sơ bộ bias=True, không trộn số liệu.

Có 2,730 ngoại lệ 1,5 IQR (9.42%); giữ nguyên để rà soát. Trung vị/IQR ít nhạy với cực trị hơn mean/std; chưa xác minh các mức giá cực đoan là lỗi hay loại listing cụ thể. Giá niêm yết không đồng nghĩa giá giao dịch.

Hình RQ1 có toàn miền và panel ≤10.000 THB: **28,210** quan sát trong vùng, **777** ngoài vùng. Số này khác số ngoại lệ IQR. Nguồn: `rq1_price_distribution.json`, `fig1_price_distribution.png`.

## 2. RQ2 — Giá theo loại phòng

| Loại phòng | n | Trung vị THB/đêm | Q1–Q3 THB/đêm |
|---|---|---|---|
| Entire home/apt | 19,300 | 1,715.44 | 1,141.18–2,796.00 |
| Hotel room | 275 | 1,999.00 | 1,163.50–2,893.60 |
| Private room | 8,914 | 1,389.83 | 925.36–2,165.12 |
| Shared room | 498 | 431.22 | 332.90–592.50 |

ANOVA tổng thể thăm dò: F=5.9323, p=0.000485542. **Chưa xác nhận các điều kiện suy luận**: phân bố lệch, cỡ nhóm mất cân đối và 3,215/7,231 host trong baseline có nhiều listing. Không diễn giải p như bằng chứng nhân quả; không chạy so sánh cặp khi điều kiện chưa được xác nhận.

**[MỞ RỘNG NGOÀI BÀI HỌC]** Levene center=median: W=3.1230, p=0.0247826; chỉ chẩn đoán thăm dò phương sai với giới hạn độc lập, không tự chứng minh đủ giả định. Nguồn/tham số tại EDA_METHODS. Boxplot tính phân vị trên toàn mẫu nhóm rồi mới giới hạn trục; bar kèm Q1–Q3, không phải khoảng tin cậy.

Nguồn: `rq2_room_type_stats.json`, `rq2_anova_condition_checks.json`, `fig2_price_by_room_type.png`.

## 3. RQ3 — Liên hệ tuyến tính quy mô–giá có độ lớn nhỏ

| Biến | n cặp hợp lệ | Pearson r | p thăm dò |
|---|---|---|---|
| accommodates | 28,987 | +0.1067 | 4.268e-74 |
| bedrooms | 25,428 | +0.0881 | 6.036e-45 |
| bathrooms | 26,286 | +0.0841 | 1.977e-42 |
| beds | 27,717 | +0.0688 | 1.902e-30 |

Các r dương nhưng độ lớn nhỏ; p nhỏ không đồng nghĩa tương quan mạnh. Chưa đánh giá độ nhạy để quy kết nguyên nhân r thấp cho ngoại lệ. Thiếu dữ liệu theo cặp và host clustering giới hạn việc suy rộng. Các số này chỉ trả lời EDA, **không phải danh sách feature được chọn cho mô hình**.

Scatter và OLS dùng đúng cùng tập cặp hợp lệ như Pearson. Lấy mẫu seed42 chỉ để vẽ điểm; catalog ghi n chọn/n thực vẽ và số ngoài trục 20.000 THB. Nguồn: `rq3_size_correlation.json`, `fig3_price_vs_size_scatter.png`.

## 4. RQ4 — So sánh khu vực trong cùng loại phòng

Pivot có 50 quận × 4 loại phòng, 43 ô n=0 và 27 ô 0<n<5. Heatmap hiển thị 23,043 listing thuộc các quận được chọn, ghi rõ n từng ô và dấu * ở ô ít mẫu.

Một số trung vị thấp/cao **trong cùng Entire home/apt**, chỉ hiển thị nhóm n≥20:

| Quận theo dữ liệu nguồn | n Entire home/apt | Trung vị THB/đêm |
|---|---|---|
| Bang Phlat | 284 | 678.03 |
| Thon buri | 396 | 940.14 |
| Bang Na | 586 | 969.48 |
| Phra Nakhon | 130 | 2,918.50 |
| Lat Phrao | 31 | 3,010.00 |
| Samphanthawong | 105 | 3,115.50 |

Ngưỡng n≥20 là quy tắc hiển thị, không bảo đảm tính đại diện. Không suy ra ảnh hưởng vị trí từ thứ hạng gộp mọi loại phòng; không gán quận thành trung tâm/ngoại ô hay khu du lịch nếu chưa có nguồn xác minh. Nguồn: pivot median/count/IQR và hai hình RQ4.

## Minh họa Bài 02 và bàn giao

Scaling, pd.cut khoảng đều và dummy nằm trên bản EDA riêng. **[MỞ RỘNG NGOÀI BÀI HỌC]** qcut minh họa phân vị, không khẳng định ưu thế chung; số đếm/ranh giới thực tế ở `lesson02_wrangling_demo.json`. Không dùng biến tạo từ price hoặc phép fit toàn bộ dữ liệu làm predictor.

| Hình 300 DPI | RQ | Nội dung |
|---|---|---|
| fig1_price_distribution.png | RQ1 | Histogram toàn miền + vùng trung tâm |
| fig2_price_by_room_type.png | RQ2 | Boxplot + trung vị/Q1–Q3 toàn mẫu |
| fig3_price_vs_size_scatter.png | RQ3 | Scatter; OLS toàn bộ cặp hợp lệ |
| fig4_price_by_neighbourhood_heatmap.png | RQ4 | Heatmap trung vị, n và cảnh báo n<5 |
| fig4_price_top_neighbourhoods_bar.png | RQ4 | Bar trung vị cùng loại phòng |

Catalog JSON/CSV tính trực tiếp từ DataFrame dùng vẽ, gồm checksum nguồn, fingerprint, phạm vi trục và số quan sát. Bước tiếp theo: đánh giá khả thi mô hình trên train/CV theo đặc tả; không hạ ngưỡng chọn biến hoặc cắt giá chỉ để đạt R² tốt hơn.
