# Review độc lập Bước 1 — 10/10/2026

**Kết luận tại thời điểm review: cần sửa trước khi nghiệm thu Bước 1.** Code chạy được trên bản dữ liệu hiện tại, nhưng báo cáo có số liệu sai và một số điều kiện lỗi chưa được kiểm soát. Đây là review của Codex, không thay thế việc hai thành viên nhóm kiểm tra chéo.

## Các kiểm tra đã chạy

Từ `workspaces/final-project/`, dùng chính `.venv` do Claude tạo:

- `.venv/bin/python -m pytest tests -q`: **17 passed**.
- `.venv/bin/python -m pytest tests -q --cov=src --cov-report=term-missing`: **17 passed, 91%** tổng coverage; file coverage của lượt review lưu trong `/tmp`, không ghi đè file cũ.
- `.venv/bin/ruff check src tests`: đạt.
- `.venv/bin/ruff format --check src tests`: đạt, 4 tệp đúng định dạng.
- Chạy `run_full_audit` trên dữ liệu thật, xuất sang thư mục tạm: JSON giống hoàn toàn bản đã bàn giao; CSV giống từng byte.
- SHA-256 và thời gian sửa đổi file raw trước/sau review không đổi. SHA-256 khớp manifest: `b17b99f9c421c566cc26a1c89a0b3d16b4c7f3dc74e659141900ccbac316b20e`.
- Xác nhận cấu trúc 31.069 × 90; 28.987 giá parse được, 2.082 giá thiếu; ID duy nhất. Các thống kê giá chính trong JSON tái lập được.
- Hai bản đặc tả hiện đồng bộ. Môi trường review: Python 3.12.3, Pandas 3.0.6, SciPy 1.18.1.

## F1 — P1: Phiếu kiểm toán không khớp dữ liệu và JSON/CSV

Vị trí: `docs/DATA_AUDIT.md` mục 3, 4, 8 và 11.

| Chỉ số | Phiếu ghi | Chạy lại từ file raw |
|---|---|---|
| Kiểu dữ liệu | object 41, float64 35, int64 14 | str 28, float64 38, int64 24 |
| Tổng số ô thiếu | 232.885 | **581.427** |
| Chủ nhà có nhiều hơn 1 listing | 1.975; 24,89% | **3.430; 43,23%** |
| Giá trị duy nhất property_type | 76 | **79** |
| Giá trị duy nhất accommodates | 17 | **16** |
| Giá trị duy nhất bedrooms | 16 | **25** |
| Giá trị duy nhất bathrooms | 17 | **32** |
| Giá trị duy nhất beds | 27 | **34** |
| Giá trị duy nhất minimum_nights | 51 | **95** |
| Giá trị duy nhất number_of_reviews | 363 | **436** |
| Giá trị duy nhất review_scores_rating | 157 | **150** |

Cần sinh các bảng/chỉ số trong Markdown từ kết quả máy đọc hoặc đối chiếu tự động; không chỉ sửa tay những số được liệt kê. Kiểm tra lại cả danh mục nhóm cột và tổng số cột trong từng nhóm. Dtype phải gắn với phiên bản Pandas thực dùng.

## F2 — P1: Có kết luận chưa có bằng chứng và ngữ nghĩa chưa rõ

Vị trí: `docs/DATA_AUDIT.md` mục 6–10 và README/đặc tả.

- Gọi listing giá cao là biệt thự ven sông/penthouse/siêu sang, toàn bộ outlier là hợp lệ về kinh doanh, hoặc mọi rating thiếu là chỗ ở mới: chưa có kiểm tra hỗ trợ.
- Khẳng định biến quy mô đều tương quan dương, dự kiến r ≥ 0,40/p < 0,001, hay một nhóm đắt hơn đáng kể: chưa có kết quả r–p/F–p. Đổi về câu hỏi trung tính cần kiểm nghiệm.
- Số nhóm có n > 200 chưa đủ chứng minh mọi điều kiện ANOVA. Số mẫu dùng kiểm định còn phải xét giá và biến hợp lệ. Không ghi “khả thi 100%” như bảo đảm kiểm định/mô hình.
- Một listing mỗi dòng không đồng nghĩa các quan sát độc lập; đã có bằng chứng nhiều listing cùng host.
- Bỏ tỷ giá/giá quy USD không cần cho phạm vi đồ án. Null ở thuế/phí chỉ cho thấy chưa xác nhận, không chứng minh giá cơ bản chưa bao gồm phí hoặc kỳ lưu trú đồng nhất.
- `bangkok_columns.csv` hiện có phân loại vai trò theo tên, chưa có từ điển ý nghĩa đầy đủ như mô tả trong tài liệu. Bổ sung mô tả từ nguồn; trường không có mô tả phải ghi chưa xác minh.

Nguồn chính thức đã đối chiếu trong lượt review:

- [Inside Airbnb — Get the Data](https://insideairbnb.com/get-the-data/) nêu giấy phép CC BY 4.0 và dẫn đến từ điển dữ liệu.
- [Inside Airbnb Data Dictionary](https://docs.google.com/spreadsheets/d/1iWCNJcSutYqpULSQHlNyGInUvHg2BoUGoNRIGa6Szc4/edit?usp=sharing): mục `price` mô tả giá theo ngày bằng tiền địa phương; ký hiệu `$` là dấu vết kỹ thuật khi xuất file. Phiên bản từ điển hiển thị 4.3, tháng 8/2022; không tự gán mô tả cho cột mới ngoài tài liệu.
- [Inside Airbnb — Data Assumptions](https://insideairbnb.com/data-assumptions/) mô tả snapshot và việc làm nhiễu tọa độ; gắn đúng nguồn nếu giữ nhận định này.

Bổ sung bằng chứng nguồn có thể truy lại, thời điểm truy cập và các giới hạn vào manifest/audit, không coi việc so 100 quote đầu là xác minh mọi trường giá toàn bộ dữ liệu.

## F3 — P1: Checksum sai vẫn thành công; không có kỳ vọng vẫn ghi verified

Vị trí: `src/data_audit.py`, `run_full_audit` dòng 400–408 và CLI.

Đã tái hiện trên fixture hai dòng trong thư mục tạm:

- Chạy CLI với `--expected-sha256` là 64 ký tự `0`: **exit code 0**, vẫn xuất báo cáo, dù `checksum_verified=false`.
- Gọi `run_full_audit(..., expected_sha256=None)`: **checksum_verified=true** dù không có giá trị đối chiếu.

Cần fail với exit khác 0 khi checksum không khớp, trước khi ghi/ghi đè báo cáo. Phân biệt rõ MATCH/MISMATCH/NOT_CHECKED; lấy hash từ manifest hoặc tham số phù hợp, tránh mặc định hash của Bangkok khi kiểm toán file khác. Thêm regression tests cho cả API và CLI; kiểm tra báo cáo cũ còn nguyên khi thất bại.

## F4 — P1: Runbook vi phạm tính bất biến dữ liệu thô

Vị trí: `docs/RUNBOOK.md` mục 3 và mục xử lý hash mismatch.

- `curl -L -o data/raw/...` sẽ ghi đè file đã tồn tại.
- Hướng dẫn `rm data/raw/...` xóa dữ liệu gốc khi hash khác.

Thay bằng quy trình không ghi đè: nếu file đã có, kiểm tra rồi dừng hoặc dùng lại khi đúng; tải file mới vào đường dẫn tạm, kiểm tra HTTP/checksum trước khi lưu lần đầu. Khi mismatch giữ nguyên file hiện có và báo lỗi, không xóa/đổi tên/ghi đè. Test tình huống lặp lại và tải lỗi không cần mạng. Không dùng file raw thật để thử thao tác phá hủy.

## F5 — P2: Parse giá và trạng thái bằng chứng còn sai ở trường hợp biên

Đã tái hiện:

- `parse_price_value('1,2,3') == 123.0`, `'1,50' == 150.0`: tự xóa dấu phẩy gây biến đổi chuỗi lỗi/khác locale thành giá khác.
- `'inf'`, `'-inf'` được chấp nhận; `True` thành 1.0. Cần chỉ chấp nhận số hữu hạn, loại bool, xác thực định dạng phân cách đã chọn và ghi lỗi parse.
- So giá 100.00 với quote 100.04 vẫn báo `exact_matches=1`: ngưỡng `< 0.05` là khớp trong dung sai, không phải tuyệt đối. Tách exact/tolerance, công bố tolerance và max difference.
- Mẫu quote dưới 100 dòng vẫn ghi mẫu số 100; cần số mẫu thực, cách chọn, JSON lỗi/quote thiếu, kiểm tra chứng cứ có cấu trúc khi phù hợp.
- `audit_host_clustering` với cột host_id rỗng ném `ZeroDivisionError`. Bổ sung xử lý dataframe rỗng/toàn null, tránh Infinity/NaN không chuẩn trong JSON; dùng null và trạng thái không đủ dữ liệu.

## F6 — P2: Môi trường và tài liệu còn thiếu bằng chứng tái lập

`requirements*.txt` chỉ đặt cận dưới; chưa lưu tập phiên bản chính xác đã dùng. Lưu snapshot/lock có hướng dẫn tái tạo môi trường đã kiểm chứng. Không gọi Markdown là “tự động sinh” khi script chỉ sinh JSON/CSV; hoặc bổ sung bước sinh thực sự. Không cần chạy lại test để chạy theo coverage; cần thêm đúng regression tests cho F1–F5.

## Điều kiện giao chặng tiếp theo

Giao Claude sửa F1–F6 trong nhiệm vụ riêng. Chưa chuyển sang làm sạch, EDA hay mô hình trong lượt sửa này. Sau khi sửa: chạy test/lint, tái lập audit với raw không đổi, chứng minh số liệu tài liệu khớp đầu ra, ghi phản hồi từng finding. Giữ bản review này làm bằng chứng lịch sử; ghi trạng thái xử lý riêng, không xóa các phát hiện cũ.
