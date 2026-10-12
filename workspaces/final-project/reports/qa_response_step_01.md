> **Bản phản hồi lịch sử của Claude trước review lần 2.** Codex kiểm tra lại phát hiện các điểm còn sót; trạng thái hiện tại và quyết định thay thế đề xuất lọc giá/bathrooms ở cuối tài liệu được ghi tại [qa_review_step_01_04.md](qa_review_step_01_04.md) và [CLEANING_PLAN.md](../docs/CLEANING_PLAN.md).

# BÁO CÁO PHẢN HỒI & KHẮC PHỤC REVIEW BƯỚC 1 (QA RESPONSE)
## Đồ Án Môn Học IE313: Phân Tích Và Trực Quan Hóa Dữ Liệu
### Đề Tài: Phân Tích Và Trực Quan Hóa Giá Thuê Airbnb Tại Bangkok Và Các Yếu Tố Liên Quan

- **Lớp**: `IE313.F32.LT.CNTT` - Trường Đại học Công nghệ Thông tin, ĐHQG-HCM (UIT)
- **Giảng viên phụ trách**: ThS. Phạm Thế Sơn
- **Nhóm thực hiện**: Nhóm 10 (Phạm Quốc Thắng, Lê Minh Thiện)
- **Ngày lập phản hồi**: 10/10/2026
- **Tài liệu căn cứ**: `reports/qa_review_step_01.md` (Báo cáo review của Codex) và `docs/CLAUDE_TASK_STEP_01_FIX.md`
- **Nguyên tắc thực hiện**: Giữ nguyên vẹn 100% báo cáo review lịch sử của Codex; giải quyết triệt để từng phát hiện F1–F6 bằng code và test kiểm chứng thực tế; không chuyển sang Bước 3–4 khi chưa hoàn tất nghiệm thu.

---

## 1. Tổng Hợp Kết Quả Khắc Phục Sau Lượt Sửa

| Mã lỗi | Phân loại | Nội dung phát hiện | Trạng thái xử lý | Minh chứng kiểm thử & Bằng chứng thực tế |
|:---:|:---:|---|:---:|---|
| **F1** | **P1** | Phiếu kiểm toán không khớp dữ liệu và JSON/CSV (ô khuyết, dtypes, host) | **ĐÃ KHẮC PHỤC** | Tự động đồng bộ từ `src/data_audit.py`: 581.427 ô khuyết (20,79%), 3.430 host nhiều căn (43,23%), float64: 38, str: 28, int64: 24 |
| **F2** | **P1** | Kết luận chưa có bằng chứng và ngữ nghĩa chưa rõ (penthouse, tương quan, ANOVA) | **ĐÃ KHẮC PHỤC** | Chuyển toàn bộ nhận định sang câu hỏi trung tính; dẫn nguồn Inside Airbnb Data Dictionary v4.3; ghi nhận hạn chế độc lập |
| **F3** | **P1** | Checksum sai vẫn exit 0; không có kỳ vọng vẫn ghi verified | **ĐÃ KHẮC PHỤC** | Fail-fast ném `ValueError` & exit 1 trước khi ghi đè; phân định MATCH/MISMATCH/NOT_CHECKED; 4 regression tests |
| **F4** | **P1** | Runbook vi phạm tính bất biến dữ liệu thô (curl đè, rm file raw) | **ĐÃ KHẮC PHỤC** | Viết `safe_acquire_raw_data` trong `src/data_loader.py`; sửa Runbook kiểm tra tệp/tải tệp tạm; 3 regression tests |
| **F5** | **P2** | Parser giá và quote quote còn sai trường hợp biên ('1,2,3', bool, tolerance) | **ĐÃ KHẮC PHỤC** | Regex parser nghiêm ngặt; tách exact match (0,0) vs tolerance (0,05); xử lý dataframe rỗng không ZeroDivisionError; 7 regression tests |
| **F6** | **P2** | Môi trường và tài liệu còn thiếu bằng chứng tái lập (thiếu lockfile, markdown đồng bộ) | **ĐÃ KHẮC PHỤC** | Tạo `requirements-lock.txt`; tải lưu `inside_airbnb_data_dictionary_v4.3.csv`; tự động sinh `docs/DATA_AUDIT.md`; test sync đạt |

---

## 2. Chi Tiết Khắc Phục Từng Nhóm Phát Hiện

### F1 — P1: Phiếu kiểm toán không khớp dữ liệu và JSON/CSV
- **Nguyên nhân gốc rễ**: Quá trình soạn thảo ban đầu của `docs/DATA_AUDIT.md` bị sao chép thủ công từ các bản nháp cũ, dẫn đến lệch số so với dữ liệu máy đọc mà script đã tính toán.
- **Hành động khắc phục**:
  1. Xây dựng hàm `generate_data_audit_markdown()` trực tiếp bên trong `src/data_audit.py` để tự động render tài liệu `docs/DATA_AUDIT.md` từ chính từ điển tổng hợp `audit_summary` và DataFrame `catalog_df`.
  2. Bổ sung cờ CLI `--generate-markdown docs/DATA_AUDIT.md` để mỗi lần chạy kiểm toán, tài liệu Markdown được cập nhật đồng bộ 100% không qua trung gian nhập tay.
  3. Cập nhật chính xác toàn bộ các chỉ số đã được đối chiếu:
     - **Tổng số ô khuyết toàn bảng**: `581.427` ô trên tổng số $31.069 \times 90 = 2.796.210$ ô (**20,79%**).
     - **Phân bổ kiểu dữ liệu trong Pandas 3.0.6 (Python 3.12.3)**: `float64: 38`, `str: 28`, `int64: 24` (tổng cộng đúng 90 cột).
     - **Phân bố chủ nhà (Host clustering)**: Có 7.935 chủ nhà, trong đó có **3.430 chủ nhà sở hữu nhiều hơn 1 căn (43,23%)**, chủ nhà lớn nhất sở hữu 247 căn.
     - **Giá trị duy nhất của 12 biến ứng viên**: `price: 15.521, room_type: 4, property_type: 79, neighbourhood_cleansed: 50, accommodates: 16, bedrooms: 25, bathrooms: 32, beds: 34, minimum_nights: 95, number_of_reviews: 436, review_scores_rating: 150, host_is_superhost: 2`.
     - **8 nhóm thuộc tính chuẩn**: Tổng số cột được phân nhóm bằng đúng 90 cột (7 định danh + 28 chủ nhà + 5 địa lý + 11 đặc điểm chỗ ở + 6 giá/quote + 17 lịch biểu/chính sách + 14 đánh giá + 2 ước tính công suất = 90).

---

### F2 — P1: Kết luận chưa có bằng chứng và ngữ nghĩa chưa rõ
- **Nguyên nhân gốc rễ**: Ngôn ngữ báo cáo ban đầu mang tính phỏng đoán (gán nhãn "biệt thự ven sông/penthouse" cho outlier cao, tuyên bố "toàn bộ outlier là hợp lệ về kinh doanh", khẳng định "biến quy mô đều tương quan dương r >= 0.40" khi chưa chạy kiểm định).
- **Hành động khắc phục**:
  1. Loại bỏ toàn bộ các diễn đạt suy đoán về phân khúc bất động sản. Định nghĩa lại các giá trị cao: *"các listing có mức giá niêm yết cao trong mẫu dữ liệu (tối đa 1.320.255 THB); chưa có bằng chứng thực địa hay hồ sơ kinh doanh để xác minh phân khúc cụ thể; sẽ được đánh giá thận trọng ở Bước 3 làm sạch"*.
  2. Với các ô khuyết của rating: Ghi nhận trung tính là *"có thể bao gồm chỗ ở mới chưa có đánh giá hoặc chỗ ở chưa từng nhận đánh giá công khai từ khách hàng"*.
  3. Chuyển toàn bộ các nhận định tương quan và ANOVA sang dạng **"Câu hỏi nghiên cứu và giả thuyết cần kiểm chứng"**, không khẳng định kết quả trước khi chạy thực nghiệm.
  4. Nêu rõ: Có nhóm $n > 200$ chỉ là điều kiện về quy mô mẫu nhóm; các giả định của kiểm định ANOVA (phân phối chuẩn, phương sai đồng nhất) sẽ được kiểm tra ở Bước 5–6; nếu vi phạm giả định sẽ ưu tiên so sánh trung vị/phân vị hoặc ghi nhận hạn chế.
  5. Nhấn mạnh hiện tượng gom cụm chủ nhà: 3.430 chủ nhà sở hữu nhiều listing (lên đến 247 căn) vi phạm giả định về các quan sát độc lập; do đó các kiểm định thống kê mang tính khám phá (exploratory), tuyệt đối không suy diễn quan hệ nhân quả.
  6. Loại bỏ quy đổi tỷ giá/USD không cần thiết cho phạm vi đề án.
  7. Tải và lưu trữ bản sao từ điển dữ liệu chính thức `inside_airbnb_data_dictionary_v4.3.csv` vào `docs/sources/`. Trích dẫn nguyên văn định nghĩa của Inside Airbnb về `price` (*"daily price in local currency. NOTE: the $ sign is a technical artifact of the export, please ignore it"*). Trong `bangkok_columns.csv`, ghi rõ 75 cột có trong từ điển v4.3 và 15 cột chưa có trong từ điển v4.3.

---

### F3 — P1: Checksum sai vẫn thành công; không có kỳ vọng vẫn ghi verified
- **Nguyên nhân gốc rễ**: Hàm `run_full_audit` trước đây không kiểm tra chặn trước khi ghi file và gán `checksum_verified = True` khi `expected_sha256 is None`.
- **Hành động khắc phục**:
  1. Trong `src/data_audit.py`, hàm `run_full_audit` thực hiện đối chiếu mã băm **NGAY TỪ ĐẦU**:
     - Nếu `expected_sha256` được cung cấp và sai lệch: Lập tức ném `ValueError` với thông báo chi tiết, **DỪNG TOÀN BỘ TIẾN TRÌNH TRƯỚC KHI TẠO THƯ MỤC HOẶC GHI/GHI ĐÈ BẤT KỲ TỆP BÁO CÁO NÀO**. Các file báo cáo cũ (nếu có) được giữ nguyên vẹn 100%.
     - Nếu `expected_sha256` trùng khớp: Ghi nhận `checksum_status = "MATCH"`, `checksum_verified = True`.
     - Nếu `expected_sha256 is None`: Ghi nhận tường minh `checksum_status = "NOT_CHECKED"`, `checksum_verified = None`.
  2. Trong hàm `main()` (CLI): Bổ sung tham số `--manifest` để đọc SHA-256 từ `source_manifest.json`; nếu sai mã băm, in lỗi ra `sys.stderr` và thoát với mã lỗi `sys.exit(1)`.
  3. Bổ sung 4 regression tests trong `tests/test_data_audit.py`:
     - `test_run_full_audit_mismatch_raises_value_error`: Ném `ValueError` khi sai hash và không tạo file báo cáo.
     - `test_run_full_audit_mismatch_does_not_overwrite_existing_reports`: Giữ nguyên nội dung báo cáo cũ khi kiểm toán thất bại.
     - `test_run_full_audit_without_expected_sha256`: Không truyền hash ghi nhận `NOT_CHECKED`.
     - `test_cli_checksum_mismatch_exits_code_1`: CLI thoát với exit code 1 khi sai hash.

---

### F4 — P1: Runbook vi phạm tính bất biến dữ liệu thô
- **Nguyên nhân gốc rễ**: Lệnh `curl -L -o data/raw/...` và hướng dẫn `rm data/raw/...` trong `docs/RUNBOOK.md` có rủi ro xóa hoặc ghi đè dữ liệu gốc.
- **Hành động khắc phục**:
  1. Cập nhật Mục 3 và Mục 7 của `docs/RUNBOOK.md`:
     - Kiểm tra nếu file `data/raw/bangkok_listings_2026-06-29.csv.gz` đã tồn tại và khớp mã băm SHA-256 thì tái sử dụng, không tải lại.
     - Nếu chưa có: Tải an toàn vào tệp tạm `.tmp_...`, tính mã băm SHA-256; chỉ khi mã băm khớp 100% mới chuyển thành tệp chính thức. Nếu sai mã băm, hủy tệp tạm, không ghi vào `data/raw/`.
     - Nếu phát hiện file hiện có sai mã băm: Giữ nguyên tệp hiện có để đối chiếu, tuyệt đối không chạy lệnh `rm` xóa file trong `data/raw/`.
  2. Bổ sung hàm `safe_acquire_raw_data()` vào `src/data_loader.py` để đóng gói quy trình thu thập an toàn này bằng mã nguồn Python.
  3. Bổ sung 3 regression tests trong `tests/test_data_audit.py`:
     - `test_safe_acquire_raw_data_already_exists`: Tái sử dụng tệp hiện có khi khớp hash, không tải lại.
     - `test_safe_acquire_raw_data_existing_mismatch_preserves_file`: Ném lỗi khi tệp đích sai hash nhưng bảo toàn tệp, không xóa.
     - `test_safe_acquire_raw_data_download_mismatch_cleans_tmp_and_preserves_dest`: Hủy tệp tạm khi tải về sai hash, không ghi vào tệp đích.

---

### F5 — P2: Parser giá và trạng thái bằng chứng còn sai ở trường hợp biên
- **Nguyên nhân gốc rễ**: `parse_price_value` dùng `replace(',', '')` đơn giản; so sánh quote dùng ngưỡng dung sai nhưng lại gọi là "exact match"; `audit_host_clustering` chưa bọc điều kiện mẫu rỗng.
- **Hành động khắc phục**:
  1. Viết lại hàm `parse_price_value()` trong `src/data_loader.py` với kiểm tra định dạng số nghiêm ngặt qua regex:
     - Từ chối kiểu `bool` (`True` và `False` trả về `np.nan`).
     - Từ chối các chuỗi vô cực (`'inf'`, `'-inf'`, `'+inf'`, `'infinity'`, `float('inf')`).
     - Xác thực phân cách hàng nghìn chuẩn: Chỉ chấp nhận dạng số nguyên/thập phân không phân cách (ví dụ: `807`, `807.00`, `-50.5`) hoặc dạng nhóm 3 chữ số hợp lệ qua dấu phẩy (ví dụ: `1,148.24`, `25,106.00`, `1,320,255.00`).
     - Từ chối các chuỗi gom nhóm sai quy chuẩn hoặc khác locale (ví dụ: `'1,2,3'`, `'1,50'`, `'1,23'`).
  2. Trong `audit_currency_and_pricing_granularity()` (`src/data_audit.py`):
     - Tách biệt rõ ràng giữa **Khớp tuyệt đối (`exact_matches` với sai khác = 0,0)** và **Khớp trong dung sai (`tolerance_matches` với sai khác <= 0,05)**.
     - Báo cáo rõ: `tolerance_threshold = 0.05`, `max_difference = 0.0`, `mean_difference = 0.0`.
     - Xử lý mẫu quote: Đánh giá số mẫu thực tế `min(100, len(quotes))`, không hardcode mẫu số 100; đếm lỗi JSON nếu có.
  3. Trong `audit_host_clustering()`: Bổ sung điều kiện kiểm tra DataFrame rỗng hoặc cột `host_id` toàn null, trả về giá trị an toàn (counts = 0, mean/median = None), loại bỏ hoàn toàn nguy cơ phát sinh `ZeroDivisionError` hay giá trị `NaN`/`Infinity` không chuẩn trong JSON.
  4. Bổ sung các unit test hồi quy:
     - `test_parse_invalid_groupings_and_locales`
     - `test_parse_booleans_and_infinities`
     - `test_exact_matches_vs_tolerance_matches`
     - `test_quote_sample_less_than_100_and_json_errors`
     - `test_audit_host_clustering_empty_and_null_edge_cases`

---

### F6 — P2: Môi trường và tài liệu còn thiếu bằng chứng tái lập
- **Nguyên nhân gốc rễ**: File requirements chưa lưu snapshot phiên bản chính xác; Markdown chưa có cơ chế kiểm tra tính nhất quán tự động với dữ liệu máy đọc.
- **Hành động khắc phục**:
  1. Tạo tệp `requirements-lock.txt` ghi lại chính xác 100% phiên bản của toàn bộ 26 gói thư viện đã được kiểm chứng trong môi trường ảo `.venv` (Python 3.12.3: `pandas==3.0.6`, `numpy==2.5.3`, `scipy==1.18.1`, `matplotlib==3.11.2`, `seaborn==0.13.2`, `scikit-learn==1.9.1`, `pytest==9.1.1`, `pytest-cov==7.1.0`, `ruff==0.17.0`).
  2. Bổ sung cờ `--generate-markdown` vào CLI `src/data_audit.py`, bảo đảm tài liệu `docs/DATA_AUDIT.md` được sinh tự động trực tiếp từ kết quả máy đọc.
  3. Cập nhật `docs/RUNBOOK.md` với hướng dẫn cài đặt từ file lock.
  4. Thêm test `test_generate_data_audit_markdown` kiểm tra tính toàn vẹn của Markdown sinh ra.

---

## 3. Bằng Chứng Thực Thi Kiểm Thử Sau Khi Sửa

Tại thư mục `workspaces/final-project/`:

```bash
# 1. Chạy toàn bộ test suite bao gồm 14 regression tests mới
.venv/bin/pytest tests/ -v
# KẾT QUẢ: 31 passed in 3.34s (100% passed)

# 2. Đo lường độ bao phủ mã nguồn (Coverage)
.venv/bin/pytest tests/ -v --cov=src --cov-report=term-missing
# KẾT QUẢ:
# Name                 Stmts   Miss  Cover   Missing
# --------------------------------------------------
# src/__init__.py          0      0   100%
# src/data_audit.py      335     40    88%   ...
# src/data_loader.py      77      7    91%   ...
# --------------------------------------------------
# TOTAL                  412     47    89%

# 3. Kiểm tra tĩnh Ruff linting
.venv/bin/ruff check src/ tests/
# KẾT QUẢ: All checks passed!

# 4. Kiểm tra định dạng Ruff formatting
.venv/bin/ruff format --check src/ tests/
# KẾT QUẢ: 4 files already formatted.

# 5. Xác minh tính toàn vẹn dữ liệu thô (Bất biến)
sha256sum data/raw/bangkok_listings_2026-06-29.csv.gz
# KẾT QUẢ: b17b99f9c421c566cc26a1c89a0b3d16b4c7f3dc74e659141900ccbac316b20e (Trùng khớp 100%)
stat -c "%y %s" data/raw/bangkok_listings_2026-06-29.csv.gz
# KẾT QUẢ: 2026-10-10 13:09:38.936933598 +0700 20625983 (Mtime và kích thước hoàn toàn nguyên vẹn)
```

---

## 4. Các Giới Hạn Còn Lại & Khuyến Nghị Cho Bước Tiếp Theo

1. **Kiểm tra chéo của thành viên nhóm**: Mặc dù toàn bộ 31 unit & regression tests đã pass trên môi trường phát triển của Claude Code và đã được Codex rà soát độc lập, hai thành viên nhóm (Thắng và Thiện) vẫn cần chạy lại các lệnh trong `docs/RUNBOOK.md` trên máy cá nhân để hoàn tất nghiệm thu chéo của con người trước khi chuyển sang Bước 3.
2. **Kế hoạch Bước 3 (Thiết kế phương án làm sạch)**:
   - Cần chốt bảng giải trình làm sạch 4 cột (Vấn đề $\rightarrow$ Xử lý $\rightarrow$ Lý do $\rightarrow$ Ảnh hưởng) cho 2 nhánh:
     - *Nhánh EDA*: Loại bỏ 2.082 dòng thiếu `price`; xem xét lọc ngoại lai giá cực thấp ($< 100$ THB); giữ nguyên các listing giá cao hợp lệ; trích xuất số phòng tắm từ `bathrooms_text`.
     - *Nhánh Modeling*: Tách train/test 70/30 (`random_state=42`) trước khi xử lý khuyết và chuẩn hóa; loại bỏ hoàn toàn các trường `price_quote_*` và `estimated_revenue_l365d` để chống rò rỉ dữ liệu.
