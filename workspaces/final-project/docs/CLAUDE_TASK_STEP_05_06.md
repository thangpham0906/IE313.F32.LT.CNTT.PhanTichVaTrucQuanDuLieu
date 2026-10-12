# Giao Claude Code: Bước 5–6 — EDA và trực quan bốn RQ

Ngày giao: 10/10/2026. CWD: `workspaces/final-project/`. Người dùng yêu cầu review rồi tiếp tục. Codex đã hoàn tất kỹ thuật Bước 1–4 và giao bạn quyền triển khai Bước 5–6 trong checkout hiện tại. Thực hiện code/notebook/chạy kiểm chứng, không chỉ trả lời kế hoạch. Không cần đợi xác nhận lại.

## Đọc trước

`reports/qa_review_step_01_04.md`, `docs/CLEANING_PLAN.md`, `docs/SPECIFICATION.md`, `README.md`, `docs/RUNBOOK.md`, root `AGENTS.md` và `CLAUDE.md`. Báo cáo `qa_response_step_01.md` là lịch sử: Codex đã sửa các lỗi còn sót; đề xuất cũ lọc giá <100 THB và điền bathrooms_text không được áp dụng.

## Trạng thái và dữ liệu đã nghiệm thu kỹ thuật

- Source `data/raw/bangkok_listings_2026-06-29.csv.gz`, raw SHA trong manifest, mtime phải giữ nguyên.
- Baseline `data/processed/bangkok_cleaned.csv`: 28.987 × 16; SHA-256 `961a01ad225e35f989ec81f124925488e392baca2ef3800ff4028b4423d5f9a7`.
- 2.082 dòng thiếu giá đã loại; mọi giá dương giữ lại, kể cả 1 THB và 1.320.255 THB; 2.730 ngoại lệ IQR để rà soát, không tự cắt tỉa.
- Predictor còn missing; 12 biến ứng viên gồm price; `id`, `host_id`, `last_scraped`, `price_raw` chỉ truy vết. Code `MODEL_FEATURES` là allowlist ứng viên, chưa phải biến đã được thống kê chọn vào mô hình.
- Notebook 01 thực thi thành công. 46 tests đạt, coverage 90%, Ruff đạt. Requirements/lock đã có nbformat, nbconvert và ipykernel.

## Đầu ra Bước 5–6

1. `src/eda_stats.py`, `src/visualization.py`; tái sử dụng từ notebook, không sao chép logic.
2. `notebooks/02_eda_and_statistical_tests.ipynb`: đọc baseline có kiểm hash; thống kê mô tả, missing từng phép tính, Pearson/đánh giá điều kiện ANOVA, groupby/pivot, diễn giải tiếng Việt có số liệu truy được.
3. `notebooks/03_visualization_figures.ipynb`: thực thi code sinh hình, mỗi hình ghi RQ, 5 bước thiết kế ngắn gọn theo Bài 04 và thông điệp thực tế.
4. `reports/stats/` CSV/JSON hữu hạn/null hợp lệ; giữ n ở từng biến/cặp/nhóm; metadata nguồn, phương pháp/tham số và hash baseline. Không tạo danh sách chọn feature mô hình từ EDA toàn bộ dữ liệu.
5. `reports/figures/` PNG 300 DPI: tối thiểu hình cần thiết trả lời bốn RQ, không vẽ thừa để đủ số lượng; lưu catalog tên hình–RQ–bảng nguồn–đơn vị–n–phạm vi trục/các điểm không hiển thị.
6. `reports/eda_findings.md`: 3–4 nhận xét thật, n/số liệu/ID hình/bảng và giới hạn; không bịa kết quả, không suy ra nguyên nhân.
7. Test quan trọng cho tính toán thống kê, missing/constant/small sample và bàn giao; không kiểm thử máy móc từng lệnh vẽ. Chạy tất cả test/Ruff và notebook 01–03 bằng kernel mới; không dùng output cũ làm bằng chứng. Xuất `reports/qa_response_step_05_06.md` với số liệu và lệnh đã chạy.
8. Cập nhật RUNBOOK, README tiến độ thực tế; đồng bộ hai spec byte-identical nếu sửa. Không đánh dấu kiểm tra con người đã hoàn tất.

## Bốn RQ và ranh giới phương pháp

- RQ1: `price`: n, mean/median/mode, min–Q1–Q2–Q3–max, variance/std/CV khi phù hợp, skewness/kurtosis, IQR và số ngoại lệ. Histogram/boxplot cần cho thấy phạm vi đầy đủ; nếu thêm góc nhìn phóng to trung tâm phải ghi rõ giới hạn trục, số lượng/tỷ lệ nằm ngoài và dẫn sang hình toàn miền. Không âm thầm lọc các giá cực đoan khỏi bảng hay kiểm định.
- RQ2: giá theo 4 `room_type`: n, mean, median, IQR/std; boxplot/bar trung vị. Mất cân đối nhóm và host clustering phải được nêu rõ.
- RQ3: quy mô (`accommodates`, `bedrooms`, `bathrooms`, `beds`) với giá: mẫu cặp hợp lệ, Pearson r và p, n và scatter. Constant hoặc n không đủ thì trả trạng thái không tính được, không bịa r/p=0. Không gọi p nhỏ là tương quan mạnh hoặc quan hệ nhân quả. Nếu downsample scatter để đọc được, cố định seed 42, công bố n toàn bộ/n hiển thị; các thống kê vẫn trên mẫu hợp lệ đầy đủ.
- RQ4: groupby và pivot theo `neighbourhood_cleansed` **và room_type**; giá trung vị, IQR, n; bar khu vực/heatmap để so sánh trong loại phòng. Cell ít mẫu phải được nhận diện bằng n và ghi giới hạn, không tự xóa hoặc khẳng định cao/thấp ổn định.
- ANOVA: đánh giá phân bố, độ phân tán, số mẫu, tính độc lập/host clustering trước. Nếu không đủ điều kiện thì trình bày mô tả và lý do không áp dụng, không ép tạo p-value. Nếu có F/p thăm dò, ghi rõ giới hạn, không khẳng định đạt mọi giả định chỉ vì n lớn. Không tự chuyển sang Spearman/Kruskal/Welch/hậu kiểm ngoài bài. So sánh cặp chỉ khi có căn cứ từ ANOVA tổng thể và công bố các cặp đã xét, giới hạn nhiều phép thử.
- Giá giữ THB/đêm; nhãn trục có đơn vị, tiêu đề, chú giải khi có ý nghĩa; Matplotlib OO (`fig, ax`), font DejaVu Sans, bảng màu trợ năng, layout hợp lý. Không có biểu đồ thời gian giả từ một snapshot; không bản đồ/NLP/dashboard.
- Minh họa Bài 02 scaling/binning/dummy khi phù hợp trên bản EDA riêng: giải thích cách/biến và giới hạn, không ghi đè baseline; không truyền feature từ price hay phép fit toàn bộ dữ liệu sang mô hình.

## Giới hạn quyền chỉnh sửa / bàn giao

Giữ raw, baseline, notebook 01 và nhật ký Bước 1–4 làm mốc. Nếu phát hiện lỗi thật trong bước trước, ghi tái hiện rõ trong QA; không tự thay chính sách làm sạch/nguồn dữ liệu để làm kết quả đẹp hơn. Không sửa template hoặc bản Word/PDF khung; chưa làm notebook 04/mô hình/báo cáo cuối/slide. Không commit/push, không gửi tin bên ngoài, không xuất bản.

Khi hoàn thành, báo rõ đường dẫn đầu ra, phát hiện chính, kiểm định đã thực hiện hoặc bỏ qua kèm lý do, kết quả test/notebook/lint và điểm còn cần reviewer kiểm tra. Giữ quyền nghiệm thu Bước 5–6 cho lần review tiếp theo, không tự ghi Codex đã review.
