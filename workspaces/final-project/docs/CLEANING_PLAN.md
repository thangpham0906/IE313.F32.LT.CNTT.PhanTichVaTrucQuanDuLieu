# Phương án làm sạch — Bước 3–4

Ngày triển khai: 10/10/2026. Người phụ trách theo kế hoạch: Thiện; kiểm tra chéo: Thắng. Codex triển khai và kiểm tra kỹ thuật theo yêu cầu tiếp tục của người dùng; việc hai thành viên chạy trên máy cá nhân vẫn chưa được xác nhận.

Nguồn: snapshot Inside Airbnb Bangkok phát hành 29/06/2026; ngày cào 29/06–02/07/2026. SHA-256 nằm trong `data/source_manifest.json`; ngữ nghĩa giá đã đối chiếu trong `DATA_AUDIT.md`. Giữ bốn RQ hiện có, chưa kết luận tương quan hoặc khác biệt thống kê.

## Bảng quyết định

| Vấn đề | Xử lý | Lý do | Ảnh hưởng / giới hạn |
|---|---|---|---|
| Raw và nguồn gốc | Kiểm checksum trước đọc; giữ file gốc; ghi hash đầu ra | Tái lập và truy vết | Sai hash dừng trước khi ghi kết quả |
| Một listing/snapshot | Loại bản ghi trùng toàn bộ; nếu ID thiếu hoặc trùng nhưng khác nội dung thì dừng rà soát | Không tự chọn bản ghi khi chưa có căn cứ | Snapshot thật không có trùng; không chứng minh các listing độc lập |
| Giá có ký hiệu `$` | Parse dấu phân cách theo định dạng xuất nguồn; giữ `price_raw`; dùng THB/đêm đã xác minh | `$` không tự chứng minh USD | Không chuyển tỷ giá; chưa xác minh đủ thuế/phí |
| Giá thiếu, sai định dạng, không hữu hạn hoặc không dương | Loại dòng, ghi ID và lý do; tuyệt đối không điền `price` | Không tạo nhãn mục tiêu giả | Mẫu phân tích chỉ gồm listing có giá hợp lệ; có nguy cơ sai lệch chọn mẫu |
| Giá dương rất nhỏ/lớn | Giữ nguyên; IQR chỉ đánh dấu tại `reports/cleaning/price_outliers.csv` | Chưa có bằng chứng mức giá là lỗi | Giữ cả 1 THB và 1.320.255 THB; không lọc `<100`, winsorize hay log mặc định |
| Predictor số bị khuyết | Giữ khuyết | EDA dùng mẫu hợp lệ cho từng phép tính; tránh điền toàn bộ dữ liệu trước chia tập | Luôn ghi n riêng; imputer nếu dùng phải fit trong training fold ở notebook 04 |
| Predictor sai kiểu, vô cực, âm | Ép số; chuyển về khuyết và ghi số lượng | Ràng buộc miền số khách/phòng/đêm/review không âm | `accommodates`, `minimum_nights` phải >=1; phòng ngủ/tắm/giường, số review/rating >=0; số đếm trừ bathrooms/rating phải nguyên |
| Phòng ngủ = 0 | Giữ nguyên | Có thể là studio; không suy diễn bằng thiếu | Không tự đổi 0 thành 1 |
| `bathrooms` thiếu nhưng có `bathrooms_text` | Giữ thiếu ở baseline | Chưa kiểm chứng tương đương ngữ nghĩa bathroom chung/riêng và quy tắc parse | Không dùng văn bản để tự điền; chỉ bổ sung sau khi có kiểm toán và nhật ký riêng |
| Rating = 0 hoặc thiếu | Giữ 0 khi số hữu hạn không âm; giữ khuyết | Không mặc định khuyết = mới hoặc 0 = thiếu | Rà soát ở EDA; chưa cắt theo thang điểm chưa được xác nhận |
| Cột danh mục | Trim khoảng trắng; chuỗi rỗng thành thiếu; superhost chỉ giữ t/f | Chuẩn hóa xác định, không học phân bố | Không gộp nhóm hiếm, không fit encoder toàn bộ mẫu |
| Cột báo giá, doanh thu ước tính, URL/văn bản | Chỉ xuất 12 biến ứng viên và cột truy vết | Giảm dữ liệu không cần thiết và rò rỉ từ giá | `id`, `host_id`, `last_scraped`, `price_raw` chỉ truy vết; không predictor |

## Hợp đồng đầu ra

- `data/processed/bangkok_cleaned.csv`: dữ liệu chung 16 cột = 12 biến ứng viên + `id`, `host_id`, `last_scraped`, `price_raw`. `price` là số hữu hạn dương; ID duy nhất; predictor có thể còn khuyết. Đây là baseline chưa fit phép biến đổi nào.
- `reports/cleaning/cleaning_summary.json`: số dòng trước/sau, lý do loại, thay đổi predictor, missing, phạm vi giá giữ lại, hash nguồn/processed, danh sách predictor cho phép.
- `reports/cleaning/excluded_rows.csv`: ID và lý do từng dòng bị loại; không chứa nội dung riêng tư/URL nguồn.
- `reports/cleaning/price_outliers.csv`: ID/giá/loại phòng/khu vực các ngoại lệ để kiểm tra; **không phải dữ liệu training đã lọc**.
- `notebooks/01_data_audit_and_cleaning.ipynb`: gọi lại code nguồn, kiểm checksum, trình bày bảng trước/sau và các kiểm tra bàn giao.

Nhánh EDA đọc baseline, dùng mẫu hợp lệ từng cặp/nhóm, không tự loại mọi dòng còn khuyết. Nhánh mô hình về sau lấy X **chỉ bằng** `src.wrangling.MODEL_FEATURES`, y = `price`; chia 70/30 seed 42 trước fit imputer/scaler/encoder/chọn biến và CV 4-fold. Host ID dùng để kiểm mức trùng chủ nhà giữa hai tập; không xem chia ngẫu nhiên theo listing là kiểm tra khả năng dự báo chủ nhà mới.

IQR tính toàn bộ mẫu chỉ phục vụ mô tả, không chuyển ngưỡng/cờ IQR sang predictor hoặc lọc test. Scaling/binning/dummy theo Bài 02 sẽ được minh họa trên bản EDA riêng ở notebook 02–03; không ghi đè baseline.

## Kết quả lần chạy 10/10/2026

Từ 31.069 dòng xuống 28.987 dòng; loại đúng 2.082 dòng thiếu giá. Không có dòng giá sai định dạng/không dương, không loại trùng, không chuyển predictor quan sát được sang thiếu vì vi phạm miền. Giữ 2.730 ngoại lệ IQR (ngưỡng trên 4.786,715 THB; khi trình bày làm tròn 4.786,72). Số liệu chi tiết và khuyết theo cột lấy từ `cleaning_summary.json`, không suy từ bảng raw.

## Tiêu chí nghiệm thu

Chạy notebook bằng kernel mới; test/lint đạt; chạy cleaning hai lần có CSV/JSON giống nhau; đối chiếu số dòng kế toán; checksum và mtime raw không đổi. Phần mềm được kiểm tra độc lập bởi Codex; thành viên nhóm vẫn cần giải thích được từng quyết định và chạy lại runbook.
