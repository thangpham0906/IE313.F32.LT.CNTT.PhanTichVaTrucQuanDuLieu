# Kết quả Bước 7 sau review

Nguồn: bangkok_cleaned.csv; SHA-256 `961a01ad225e35f989ec81f124925488e392baca2ef3800ff4028b4423d5f9a7`.
Train 20,290, test 8,697; seed 42; CV 4 fold.

## Chọn biến trong train/fold

Ngưỡng số: |r|≥0,30 và p<0,05 theo repository. Biến phân loại chưa được chọn khi chưa có cơ sở dùng ANOVA làm bộ lọc. Đây là chính sách phân tích, không phải định lý về khả năng dự báo.

| Biến số | n train | r train | p train | Được chọn |
|---|---:|---:|---:|---|
| accommodates | 20290 | 0.10359685 | 1.5648382e-49 | False |
| bedrooms | 17780 | 0.088127676 | 5.3665267e-32 | False |
| bathrooms | 18353 | 0.087589847 | 1.3643475e-32 | False |
| beds | 19386 | 0.069044172 | 6.3236294e-22 | False |
| minimum_nights | 20289 | -0.022790891 | 0.0011681544 | False |
| number_of_reviews | 20290 | 0.001082419 | 0.87747292 | False |
| review_scores_rating | 13702 | -0.024696398 | 0.0038398455 | False |

Số biến từng fold: [0, 0, 0, 0]; full train: 0.

| Biến phân loại | Số nhóm | F thăm dò | p thăm dò | Trạng thái |
|---|---:|---:|---:|---|
| room_type | 4 | 3.7022279 | 0.01117702 | COMPUTED |
| property_type | 71 | Không xác định | Không xác định | NOT_COMPUTABLE |
| neighbourhood_cleansed | 50 | 1.2733929 | 0.095025106 | COMPUTED |
| host_is_superhost | 2 | 5.6020681 | 0.017948623 | COMPUTED |

Các nhóm n=1 không bị âm thầm loại để tính lại ANOVA. N, skew, Levene và host trong từng training fold lưu tại `feature_selection.json`. **[MỞ RỘNG NGOÀI BÀI HỌC]** Levene center=median; nguồn/giới hạn tại `docs/EDA_METHODS.md`. Skew và mất cân đối chỉ là chẩn đoán, không tự chứng minh giả định đúng/sai.

## Quyết định theo quy tắc hiện tại

Theo quy tắc |r|≥0.3 và p<0.05, số biến chọn ở các fold là [0, 0, 0, 0]; full train có 0 biến. Fold không có biến: fold_1, fold_2, fold_3, fold_4. Biến phân loại chưa được chọn do giả định dùng ANOVA chưa xác nhận; xem chẩn đoán từng biến/fold. Chưa triển khai hồi quy theo chính sách hiện tại; đây không phải chứng minh dữ liệu không thể mô hình hóa.

## Mốc dự đoán trung bình

Giá dự đoán cố định = 2976.1215 THB/đêm. DummyRegressor là API bổ sung kỹ thuật; không thay thế hồi quy có predictor.

| Thước đo | Train | CV mean ± std | Test |
|---|---:|---:|---:|
| MSE (THB²) | 3.8366581e+08 | 3.8371497e+08 ± 2.189993e+08 | 3.150212e+08 |
| R² | 0 | -0.00053479395 ± 0.00060631197 | -1.4334218e-05 |

R² = 1 − SSE/SST với trung bình của chính tập đang đánh giá trong SST; mẫu hằng/ít hơn 2 trả null. CV std dùng ddof=0; không bỏ fold chưa xác định. Số đầy đủ trong JSON/CSV, chỉ làm tròn khi trình bày.

## Giới hạn và sản phẩm

2,229 host giao hai tập; 7,202 listing test thuộc host đã thấy (82.81%). 82.81% listing trong tập test thuộc về các chủ nhà đã xuất hiện trong tập train. Phân chia ngẫu nhiên theo listing chỉ đánh giá khả năng dự báo trên các chỗ ở mới trong cùng tập dữ liệu, KHÔNG đánh giá khả năng tổng quát hóa sang chủ nhà mới.
Các p-value mang tính thăm dò. Không suy ra tác động nhân quả, tính độc lập hay khả năng tổng quát sang host mới.
Sản phẩm hồi quy hiện hành: `{'best_pipeline_joblib': None, 'model_diagnostics_npz': None, 'diagnostic_figures': None, 'status_explanation': 'Chưa có hồi quy theo quy tắc chọn biến hiện tại; chỉ có mốc trung bình.', 'archived_previous_artifacts': []}`.
Bảng so sánh và trạng thái: `model_comparison.csv`; metadata có phiên bản môi trường. Phương pháp: `docs/MODELING_METHODS.md`.
