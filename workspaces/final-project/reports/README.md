# Sản phẩm báo cáo Nhóm 10

Cập nhật 12/10/2026: đã điền kết quả thật vào [Word](Nhom10_Bao_cao.docx) và xuất [PDF](Nhom10_Bao_cao.pdf). Đã có [12 slide PowerPoint](Nhom10_Slides.pptx), [PDF slide](Nhom10_Slides.pdf), [kịch bản 10 + 5 phút](Nhom10_Kich_ban_thuyet_trinh.md) và [hướng dẫn nộp](Nhom10_Huong_dan_nop.md). **Còn nhóm kiểm tra chéo, tổng duyệt và nộp; chưa coi là đã nghiệm thu bởi hai thành viên.**

## Nội dung hiện có

Word giữ bìa/logo, khổ giấy, lề và styles từ template; có thông tin hai thành viên, không ghi GVHD. Giới thiệu đúng hai đoạn BT dưới Heading 1 GIỚI THIỆU: mục tiêu/phương pháp/kết quả và minh bạch nguồn. Đã ghi xác nhận của nhóm: không tham khảo dự án/code mẫu, không dùng đề tài/dữ liệu làm đồ án môn khác; có AI hỗ trợ và nhóm chịu trách nhiệm kiểm tra.

Báo cáo có bảng 12 biến đúng 5 cột, quyết định làm sạch, bốn RQ, bảng r/p/n và F/p, hình thật, phần train/CV và benchmark, bốn phát hiện, kết luận, tài liệu tham khảo và phụ lục phân công. Không có code dài, ô chờ hay số liệu mô phỏng trong phần thân. PDF có **11 trang tổng: bìa + 8 trang thân + tham khảo + phụ lục**.

Chưa xây hồi quy cho Bangkok theo chính sách chọn biến hiện tại. Không biến số qua ngưỡng; điều kiện ANOVA làm bộ lọc phân loại chưa xác nhận. Báo cáo không kết luận dữ liệu không thể mô hình hóa và không có hệ số/alpha/hình phần dư giả. Xem [review Bước 7](qa_review_step_07.md).

## Cập nhật tài liệu và kiểm tra

Dựng tài liệu bằng `scripts/build_report.py`, `scripts/build_slides.py`, sơ đồ bằng `scripts/create_report_flow.py`; hướng dẫn môi trường và xuất PDF ở [RUNBOOK](../docs/RUNBOOK.md#8-dựng-word-slide-và-pdf). Khi sửa trực tiếp Word/PPTX, lưu bản riêng trước khi chạy lại builder vì script sẽ tái tạo bản thảo.

Đã mở lại DOCX/PPTX, xuất PDF bằng LibreOffice và xem bố cục; số liệu chính đối chiếu artifact. [Kiểm tra tổng hợp](qa_audit_report.md) ghi minh chứng. Nhóm vẫn phải kiểm tra font/phân trang trên máy dùng để trình bày, đọc nội dung và chạy lại notebook theo phân công. Không ghi nhận kiểm tra chéo của con người khi chưa được xác nhận.

## Bản lịch sử

`archive/Nhom10_Bao_cao_Khung_20261010.docx` và `Nhom10_Bao_cao_Khung.pdf` là khung ngày 10/10, không phải bộ nộp. `qa_response_step_07.md` là bàn giao Claude trước review, có nhãn lịch sử; kết quả hiện hành theo `qa_review_step_07.md` và artifact `modeling/`. Hai template giảng viên ở `docs/` được giữ nguyên.
