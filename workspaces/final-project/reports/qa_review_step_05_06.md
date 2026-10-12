# Review độc lập và bản sửa Bước 5–6

Ngày **11/10/2026**. Reviewer: **Codex**. Phạm vi: phần EDA/trực quan do Claude Code bàn giao; sửa lỗi, kiểm chứng lại và chuẩn bị Bước 7 theo yêu cầu người dùng.

**Kết luận: Bước 5–6 hoàn tất kỹ thuật sau các bản sửa dưới đây, có thể chuyển sang đánh giá khả thi mô hình.** Chưa xác nhận kiểm tra chéo của hai thành viên. Word/PDF hiện vẫn là bản khung, chưa có các kết quả EDA mới; không coi đây là bộ báo cáo cuối kỳ.

## Phát hiện và cách xử lý

| Mức | Phát hiện khi review | Bản sửa và bằng chứng |
|---|---|---|
| P1 | Boxplot lọc price≤8.000 trước khi tính phân vị, nhưng nhãn/bảng lại dùng toàn mẫu. Ví dụ trung vị Entire home/apt toàn mẫu 1.715,44, sau lọc còn 1.658,90 THB. | `room_box_statistics` tính trên toàn bộ nhóm rồi `ax.bxp`/giới hạn trục; trung vị và Q1–Q3 khớp bảng. Test đối chiếu cả thống kê và artist của hình trên dữ liệu có cực trị. |
| P1 | Đường OLS dùng cặp price≤20.000 trong khi Pearson/nhãn nói toàn mẫu; nhãn 3.000 điểm không phản ánh số điểm thực sự trong trục. | `scatter_data` fit toàn bộ cặp hợp lệ, lấy mẫu seed42 chỉ để vẽ. Đã đối chiếu hệ số với `scipy.stats.linregress` trực tiếp trên baseline; catalog ghi n chọn/n vẽ/n ngoài trục từng panel. |
| P1 | Điều kiện ANOVA có thể được gắn đủ giả định từ skew nhỏ và Levene p≥0,05; không xử lý đầy đủ host clustering và mẫu suy biến; còn chạy cặp nhóm khi chưa đủ cơ sở suy luận. | Không tự xác nhận phân phối chuẩn/độc lập/phương sai bằng nhau. ANOVA chỉ thăm dò, ghi F/p và giới hạn; bỏ pairwise khi điều kiện chưa xác nhận. Mẫu quá ít/hằng/vô cực trả trạng thái/null rõ ràng. Tests kiểm tra host lặp, mẫu hằng/singleton và JSON chuẩn. |
| P2 | Số mẫu catalog/nhận xét nhập tay sai: vùng ≤10.000 bị lẫn với ngoại lệ IQR; heatmap, số host và một số trung vị khu vực không khớp. | Catalog tính từ DataFrame thật, có fingerprint/hash. Đúng là 28.210 trong vùng ≤10.000 và 777 ngoài vùng, khác 2.730 ngoại lệ IQR; heatmap 23.043 listing; baseline 3.215/7.231 host có nhiều listing. `eda_report.py` sinh nhận xét từ artifact. |
| P2 | Nhận xét quy kết r yếu cho ngoại lệ, gọi trung vị “chính xác”, gán quận là vùng du lịch/ngoại ô, coi ngưỡng n≥20 loại bỏ nhiễu khi chưa có chứng cứ. | Viết lại nhận xét theo số liệu mô tả; không suy diễn nguyên nhân hoặc địa lý; bar khu vực giữ cùng Entire home/apt; n≥20 chỉ là lựa chọn hiển thị. |
| P2 | Trộn kurtosis audit bias=True với EDA bias=False; phương sai mẫu một dòng thành 0; giá trị vô cực lọt vào n hợp lệ và JSON. | Ghi rõ ddof=1, Fisher excess kurtosis bias=False trong metadata/phương pháp; kurtosis EDA 3.094,3914. Đại lượng không xác định trả null, JSON `allow_nan=False`, cặp thống kê chỉ nhận số hữu hạn. |
| P2 | Levene/qcut chưa tách nhãn phần ngoài bài; generator có thể phục hồi notebook cũ; RNG fixture chưa có seed. | Thêm `docs/EDA_METHODS.md` có nguồn chính thức/lý do/giới hạn, nhãn tại notebook và nhận xét. Generator dùng bản mẫu đã review, giữ file hiện có nếu không yêu cầu overwrite; fixture seed42. Source/Markdown notebook 02–03 đã đối chiếu với mẫu. |
| P2 | README lặp Bước 7–10; hai đặc tả vẫn ghi chưa có EDA. Runbook lùi về tải tệp tạm cố định trong raw rồi `mv`, sai cờ `--reports-dir`, gọi module visualization bằng cách không còn hỗ trợ. | Đồng bộ trạng thái 11/10 và hai đặc tả byte-identical. Runbook dùng `safe_acquire_raw_data`, cờ `--report-dir`, lệnh `python -m src...`; bỏ khẳng định baseline giữ mtime sau khi xuất lại. |

Tài liệu Claude bàn giao ban đầu được giữ tại `qa_response_step_05_06.md` với chú thích lịch sử; không dùng số cũ ở đó để viết báo cáo.

## Kiểm chứng sau sửa

| Kiểm tra | Kết quả thực chạy |
|---|---|
| `pytest tests --cov=src --cov-report=term-missing` | **72 passed**, không warning trong pytest; coverage unit-test **87,55%**, làm tròn 88% |
| `ruff check .` / `ruff format --check .` | Đạt toàn thư mục, gồm notebook và bản mẫu; 35 file đạt format |
| Notebook 01/02/03 chạy headless bằng kernel mới | Exit 0; lần lượt **5/7/6 code cell** đã thực thi, không output lỗi |
| Tái lập EDA vào thư mục tạm riêng | **12 artifact giống từng byte**; metadata khớp ngoài thời điểm UTC |
| Đối chiếu độc lập baseline | n=28.987, mean/median/quartile/std, IQR outlier, Pearson n/r/p, OLS toàn mẫu và các số ngoài trục đều khớp |
| Ảnh | **5 PNG**, DPI đọc từ file xấp xỉ 300 do độ phân giải metadata; đã xem trực quan cả 5 hình, kiểm tra nhãn và giới hạn |
| Raw | SHA-256 `b17b99f9c421c566cc26a1c89a0b3d16b4c7f3dc74e659141900ccbac316b20e`; mtime_ns `1791612578936933598`, không đổi |
| Baseline | SHA-256 `961a01ad225e35f989ec81f124925488e392baca2ef3800ff4028b4423d5f9a7`, không đổi; mtime đổi khi notebook 01 xuất lại là bình thường |
| Template GV, slide mẫu, Word/PDF bản khung | Giữ nguyên hash và mtime so với trước review |
| Hai đặc tả | Nội dung giống từng byte |

Coverage chỉ tính lượt pytest; module sinh nhận xét `src/eda_report.py` được chạy qua CLI/notebook 03 trên dữ liệu thực, chưa nằm trong coverage unit-test. Không thêm test chỉ để tăng tỷ lệ. Log notebook có cảnh báo cấu hình transport từ ipykernel; cả ba tiến trình vẫn exit 0 và không có cell lỗi.

Minh chứng máy đọc: [qa_step_05_06_verification.json](qa_step_05_06_verification.json). Log: [pytest/coverage](verification_step_05_06/pytest_coverage.log), [notebook](verification_step_05_06/notebooks.log). Hướng dẫn tái lập: [RUNBOOK.md](../docs/RUNBOOK.md).

## Bước tiếp theo

Giao Claude Code **[Bước 7 — hồi quy bổ trợ](../docs/CLAUDE_TASK_STEP_07.md)**: kiểm tra tính khả thi trên train/fold, chống rò rỉ chọn biến và đánh giá Linear/Ridge khi có cơ sở. Nếu không đủ biến theo quy tắc, phải xuất giải trình và kết quả kiểm tra thật; không hạ ngưỡng hoặc loại giá cực trị để ép mô hình thành công. Chưa có kết quả Bước 7 tại thời điểm review này.

Thắng/Thiện tiếp tục kiểm tra chéo trên máy cá nhân. Giờ/kênh nộp và lịch thuyết trình còn chưa xác nhận; hạn nộp người dùng đã cung cấp là **18/10/2026**. Tổng hợp mô hình và EDA vào Word ở Bước 8–9, sau khi phần mô hình được review.
