# Kiểm tra tổng hợp bộ đồ án — Nhóm 10

**Cập nhật 12/10/2026: đạt kiểm tra kỹ thuật và bố cục của bộ tài liệu hiện hành. Chưa có xác nhận kiểm tra chéo, tổng duyệt hoặc nộp bài của hai thành viên.** Hạn nộp 18/10/2026.

## Phạm vi và minh chứng

| Hạng mục | Kết quả đã kiểm tra | Minh chứng |
|---|---|---|
| Kiểm toán/làm sạch | Raw 31.069×90; baseline 28.987×16; loại 2.082 dòng thiếu giá; raw bất biến | `qa_review_step_01_04.md`, `data/source_manifest.json`, `reports/cleaning/` |
| EDA/hình | Bốn RQ, 12 artifact thống kê + metadata, 5 hình 300 DPI; r/p/n, F/p, số mẫu trong hình và catalog đã review | `qa_review_step_05_06.md`, `qa_step_05_06_verification.json` |
| Review Bước 7 | Sửa ANOVA gán sẵn, R² làm tròn, kiểm tra đầu vào và nhánh huấn luyện; 91 tests passed, src coverage 89,18% | `qa_review_step_07.md`, `qa_step_07_verification.json`, `verification_step_07/` |
| Tái lập mô hình | Split/fold IDs, r/p/n mọi biến số/fold, group sizes, benchmark tính độc lập đều trùng; bốn artifact byte-identical, metadata trùng ngoài timestamp | `qa_step_07_verification.json` |
| Notebook | 01–03 thực thi ở review Bước 5–6; 04 chạy lại kernel mới sau sửa Bước 7. Output lưu đủ 5/7/6/5 code cells, không error | Notebook 01–04; log các review tương ứng |
| Word/PDF | Đúng hai đoạn Giới thiệu BT; Heading 1 GIỚI THIỆU; có xác nhận minh bạch; bảng biến 5 cột/12 biến; sáu mục tham khảo TLTK; không có ô chờ | `Nhom10_Bao_cao.docx`, `qa_step_08_10_verification.json` |
| Phân trang | PDF 11 trang: bìa, 8 trang thân, tham khảo, phụ lục. Đã xem bố cục toàn bộ và kiểm tra bảng/nhãn; không có text ngoài khổ trang | `Nhom10_Bao_cao.pdf`, `verification_step_08_10/Bao_cao_contact.png` |
| Slide/demo | 12 slide, có notes, số liệu đối chiếu; xuất PDF đủ 12 trang. Kịch bản slide 1–10 tổng 600 giây và demo 300 giây là dự kiến, chưa đo tổng duyệt thực tế | `Nhom10_Slides.pptx`, `.pdf`, `Nhom10_Kich_ban_thuyet_trinh.md` |
| Số liệu báo cáo | Bảng Pearson toàn mẫu/train, p-value, MSE/R² đối chiếu JSON; hình lấy nguyên artifact; con số chính trong slide khớp | `qa_step_08_10_verification.json` |
| Bảo toàn | Raw giữ SHA-256/mtime; baseline, hai template và bảng/hình EDA giữ hash; Word khung lưu riêng trước khi điền | Các JSON verification; `archive/Nhom10_Bao_cao_Khung_20261010.docx` |
| Đồng bộ tài liệu | README và hai đặc tả nhất quán; hai đặc tả byte-identical; runbook, báo cáo và hướng dẫn không gọi bản hiện hành là khung | README, SPECIFICATION, RUNBOOK, reports/README |
| Lint/format | `ruff check .`, `ruff format --check .` đạt; `git diff --check` không có lỗi | `verification_step_08_10/ruff.log` |

DOCX/PPTX dựng bằng script trong `scripts/`; PDF xuất bằng LibreOffice 24.2.7. Bản gốc template không sửa. Môi trường docs tách khỏi lock phân tích; RUNBOOK ghi cách dựng lại. Log xuất PDF giữ dòng kết quả chuyển đổi; preview trong `verification_step_08_10/` dùng kiểm tra bố cục, không phải hình phân tích mới.

## Kết luận mô hình cần giữ trong bài nộp

Chưa có predictor qua chính sách chọn biến trên train/CV. Không biến số qua đồng thời ngưỡng |r|≥0,30 và p<0,05; điều kiện dùng ANOVA làm bộ lọc phân loại chưa được xác nhận. Chưa xây hồi quy Linear/Ridge cho Bangkok, không có alpha tối ưu hay hình phần dư hồi quy; không suy ra rằng dữ liệu không thể mô hình hóa.

Mốc trung bình train cho test MSE 315.021.203,83 THB² và R²≈−0,000014334. 82,81% listing test thuộc host đã xuất hiện ở train; chưa đánh giá chủ nhà mới. Nhánh phần mềm khả thi được kiểm thử với dữ liệu tổng hợp, không coi kết quả tổng hợp là thực nghiệm của đồ án.

## Việc còn lại cần người trong nhóm thực hiện

1. Thiện và Thắng chạy runbook trên máy cá nhân; đối chiếu nội dung/số liệu và ghi nhận kiểm tra chéo.
2. Thắng đọc Word/PDF; cả hai mở PPTX trên máy trình bày, tổng duyệt 10 + 5 phút trước 17/10.
3. Thắng xác nhận giờ/kênh nộp, lịch thuyết trình và yêu cầu video. Thiện kiểm tra quy cách file/code/data theo kênh nộp.
4. Nếu học online, nhóm quay video theo hướng dẫn. Tài liệu link chỉ tạo khi có tệp/link thật.
5. Thắng nộp trước giờ chốt ngày 18/10, Thiện kiểm tra và lưu bằng chứng.

Đây là các công việc còn mở, không phải lỗi bị che giấu bằng trạng thái “hoàn thành”. Chi tiết tại `Nhom10_Huong_dan_nop.md`; chưa upload, publish, commit hay push trong lần tiếp tục này.
