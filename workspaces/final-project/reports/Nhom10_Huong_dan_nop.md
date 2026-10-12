# Danh mục nộp và việc còn lại — Nhóm 10

Cập nhật 12/10/2026. **Hạn nộp 18/10/2026; giờ chốt, kênh nộp, lịch thuyết trình và hình thức video chưa xác nhận. Chưa nộp bài.** Thắng kiểm tra thông báo; Thiện đối chiếu đủ file. Mục tiêu nội bộ kiểm tra và tổng duyệt trước 17/10.

## Sản phẩm đã có

| Sản phẩm | Vị trí hiện hành |
|---|---|
| Báo cáo Word | `reports/Nhom10_Bao_cao.docx` |
| Báo cáo PDF | `reports/Nhom10_Bao_cao.pdf`: 11 trang, gồm bìa + 8 trang thân + tham khảo + phụ lục |
| Slide | `reports/Nhom10_Slides.pptx`; `Nhom10_Slides.pdf` để xem trước/dự phòng |
| Notebook và module | Toàn bộ `notebooks/*.ipynb`, `src/*.py`; bốn notebook đã chạy |
| Dữ liệu gốc | `data/raw/bangkok_listings_2026-06-29.csv.gz` — 20.625.983 bytes |
| Baseline sạch | `data/processed/bangkok_cleaned.csv` — 28.987×16 |
| Nguồn và tái lập | `data/source_manifest.json`, `docs/sources/`, `docs/RUNBOOK.md`, requirements, pyproject, tests |
| Bảng/hình minh chứng | `reports/audit/`, `reports/cleaning/`, `reports/stats/`, `reports/figures/`, `reports/modeling/` |
| Kịch bản | `reports/Nhom10_Kich_ban_thuyet_trinh.md` |
| Kiểm tra kỹ thuật | `reports/qa_audit_report.md`, các review và JSON verification |

Không dùng `Nhom10_Bao_cao_Khung.pdf` hay Word trong `reports/archive/` làm bài nộp. Chúng là bản khung lịch sử. Không có file mô hình hồi quy cho Bangkok vì chưa có đặc trưng qua chính sách hiện tại; giải trình nằm trong báo cáo/notebook 04.

## Chuẩn bị file tại kênh nộp

Template yêu cầu nộp từng file trực tiếp, không nén toàn bộ báo cáo/code/data thành một ZIP/RAR. Báo cáo và slide đã có tiền tố `Nhom10_`. Với code/data, giữ cấu trúc chạy trong workspace; khi hệ thống chỉ nhận file rời cần tạo bản sao tên `Nhom10_<tên_gốc>` và kèm ánh xạ về đường dẫn gốc để người chấm khôi phục imports/đường dẫn. Không đổi tên module/dữ liệu gốc tùy tiện vì có thể làm notebook không chạy. Cách nhận thư mục/file rời còn phụ thuộc kênh nộp cần xác nhận.

Tệp raw đang ở định dạng `.csv.gz` do nguồn phát hành, không phải ZIP gom sản phẩm do nhóm tạo. Raw và baseline riêng lẻ đều dưới 50 MB. Nếu kênh nộp bắt buộc CSV giải nén, tạo bản sao ngoài `data/raw/`, đo dung lượng và xử lý theo quy định dataset; giữ nguyên raw/hash. Template có chênh lệch 50/60 MB cho dataset nên Thắng cần đối chiếu thông báo trước khi dùng Drive.

Chỉ tạo `Nhom10_Dataset.docx` hoặc `Nhom10_Video.docx` chứa link khi thật sự có tệp thuộc điều kiện và đã tạo link tải được; hiện chưa có link nên chưa tạo tài liệu giả. Với hệ online, nhóm quay video có mặt các thành viên theo hướng dẫn; video >60 MB dùng link theo template. Không dùng một link Drive thay toàn bộ bộ nộp.

## Kiểm tra của nhóm trước khi nộp

- [ ] Thiện và Thắng chạy runbook trên máy cá nhân, ghi xác nhận kiểm tra chéo.
- [ ] Thắng đọc toàn bộ Word/PDF; Thiện đối chiếu số liệu với notebook/artifact.
- [ ] Cả hai mở PPTX trên máy thuyết trình; tổng duyệt 10 phút + demo 5 phút.
- [ ] Thắng xác nhận giờ/kênh nộp, lịch thuyết trình và yêu cầu video; cập nhật README.
- [ ] Thiện kiểm tra tên file, đủ code/data, đường dẫn khôi phục và link tải nếu dùng.
- [ ] Thắng nộp trước giờ chốt; Thiện kiểm tra và lưu bằng chứng nộp thành công.

Các mục này chưa được đánh dấu hoàn tất vì chưa có xác nhận của hai thành viên.
