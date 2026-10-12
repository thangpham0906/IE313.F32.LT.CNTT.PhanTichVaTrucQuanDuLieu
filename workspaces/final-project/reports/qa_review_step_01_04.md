# Review lần 2 và nghiệm thu kỹ thuật Bước 1–4

Ngày: 10/10/2026. Reviewer/triển khai bổ sung: Codex. Yêu cầu: kiểm tra phần Claude Code đã sửa, rồi tiếp tục các bước. Kết luận: **đủ điều kiện kỹ thuật chuyển sang EDA Bước 5–6**. Kiểm tra trên máy cá nhân của Thắng/Thiện chưa được xác nhận.

## Review phần Claude đã bàn giao

31 test ban đầu và Ruff đạt. Chạy độc lập audit vào thư mục tạm: JSON giống nhau khi bỏ timestamp, CSV giống từng byte; SHA-256/mtime raw không đổi. Số liệu cơ bản đã sửa đúng: 31.069 × 90, 581.427 ô khuyết, 3.430/7.935 host nhiều listing.

Các điểm còn sót đã được Codex sửa trực tiếp:

| Phát hiện | Cách sửa và bằng chứng |
|---|---|
| P1: `--manifest` thiếu/lỗi JSON/thiếu hash vẫn hạ xuống NOT_CHECKED | Manifest được yêu cầu phải đọc được và có hash 64 ký tự hex; mâu thuẫn hash CLI bị từ chối. Test bốn loại manifest lỗi chứng minh exit khác 0 và chưa tạo output |
| P1: Markdown gán sẵn 90 cột, khớp quote 100%, THB và thống kê 0 khi không có giá | Tách `src/audit_markdown.py`, sinh số liệu từ summary/catalog; không có bằng chứng thì ghi chưa xác minh/N/A; test với dữ liệu một dòng, giá toàn thiếu và hằng số |
| P2: Raw tải đồng thời có thể bị ghi đè qua `Path.replace`, temp tên trùng theo giây | Staging tên duy nhất ngoài raw; chỉ công bố file đã kiểm hash bằng hard link không ghi đè. Test tạo file cạnh tranh trong lúc tải chứng minh giữ nguyên file đó; runbook dùng cùng hàm đã kiểm thử |
| P2: JSON xuất NaN ở mẫu nhỏ/không có phương sai | Đại lượng không xác định chuyển null; JSON xuất với `allow_nan=False`; không tính skew/kurtosis khi thiếu điều kiện |
| Tài liệu trạng thái còn mâu thuẫn, gợi ý lọc <100 THB/điền bathroom chưa được kiểm chứng | Đồng bộ README/hai spec/runbook; giữ phản hồi cũ như lịch sử có chú thích. Phương án hiện hành giữ mọi giá dương, không tự điền bathrooms_text |

`safe_acquire_raw_data` dùng thư mục staging cùng filesystem mặc định. Nếu người gọi tự chọn staging ở filesystem khác, thao tác công bố báo lỗi, không ghi đè đích. Nhánh tải mạng được kiểm bằng fixture; review này tái sử dụng raw hiện có, không tải lại snapshot.

## Công việc tiếp tục đã hoàn thành

- Giữ bốn RQ theo đặc tả, không đặt trước kết luận Pearson/ANOVA.
- `docs/CLEANING_PLAN.md`: bảng vấn đề–xử lý–lý do–ảnh hưởng; xác định giới hạn EDA và training.
- `src/wrangling.py`: kiểm manifest, chuẩn hóa xác định, nhật ký dòng loại và predictor; cấm ghi output vào raw.
- `data/processed/bangkok_cleaned.csv`: **28.987 dòng × 16 cột**, giảm 2.082 dòng thiếu giá; không cắt giá dương, không điền predictor/scale/chọn biến.
- `reports/cleaning/`: summary, ID dòng loại, 2.730 ngoại lệ IQR được giữ lại để rà soát.
- `notebooks/01_data_audit_and_cleaning.ipynb`: thực thi bằng kernel mới, 5/5 code cells có kết quả, không có output lỗi; trình bày nguồn, chính sách, kế toán dòng, missing và hợp đồng bàn giao.

## Kiểm chứng cuối

| Kiểm tra | Kết quả |
|---|---|
| `pytest --cov=src --cov-report=term-missing` | **46 passed**, coverage **90%**, không warning |
| `ruff check src tests` | Pass |
| `ruff format --check src tests` | 8 file đạt |
| `python -m jupyter nbconvert --to notebook --execute ... --inplace` | Exit 0; notebook 01 có output đầy đủ |
| Chạy cleaning sang thư mục tạm | CSV processed, summary và hai CSV nhật ký giống từng byte |
| Raw SHA-256 | `b17b99f9c421c566cc26a1c89a0b3d16b4c7f3dc74e659141900ccbac316b20e` |
| Raw mtime ns | `1791612578936933598`, không đổi so với trước review |
| Processed SHA-256 | `961a01ad225e35f989ec81f124925488e392baca2ef3800ff4028b4423d5f9a7` |
| Hai bản đặc tả | Giống từng byte |

Bằng chứng máy đọc: [qa_step_01_04_verification.json](qa_step_01_04_verification.json). Requirements/lock đã bổ sung bộ chạy notebook. Hướng dẫn chạy lại tại `docs/RUNBOOK.md`.

Giới hạn: giá cực đoan còn nguyên; predictor còn khuyết; mô tả/kiểm định sau này phải ghi n riêng và hạn chế host clustering. Chưa có mô hình, kết quả kiểm định, báo cáo cuối hay slide hoàn thiện. Không xem kiểm tra kỹ thuật này là xác nhận nhóm đã kiểm tra chéo hoặc nộp bài.
