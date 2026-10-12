# Giao tiếp Claude Code — sửa và nghiệm thu Bước 1

Ngày giao: 10/10/2026. Đọc `reports/qa_review_step_01.md` và nhiệm vụ gốc `docs/CLAUDE_TASK_STEP_01.md` từ gốc đồ án `workspaces/final-project/`.

Codex đã chạy độc lập: 17 test pass, coverage 91%, Ruff pass, JSON/CSV tái lập và raw không đổi. Tuy nhiên, F1–F6 trong báo cáo review phải được sửa trước khi nghiệm thu. Ưu tiên F1–F4 (P1), sau đó F5–F6 (P2). Thực hiện thay đổi và test, không chỉ trả lời kế hoạch.

## Đầu ra cần bàn giao

1. Sửa code/checksum/parser/kiểm tra biên và runbook theo bằng chứng cụ thể F1–F6. Regression tests phải tái hiện lỗi rồi chứng minh hành vi đúng; bao gồm CLI checksum mismatch không ghi đè báo cáo và quy trình lấy dữ liệu không ghi đè raw.
2. Bổ sung các chỉ số còn thiếu vào JSON và cơ chế sinh/đối chiếu bảng Markdown để tránh bịa hoặc lệch số liệu. Viết trung tính, phân biệt số liệu đã tính với giả thuyết chưa kiểm nghiệm. Bổ sung ý nghĩa cột kèm nguồn hoặc nhãn chưa xác minh.
3. Lưu bằng chứng nguồn/từ điển và phiên bản môi trường đã dùng. Không tải lại hoặc thay phiên bản dữ liệu đang có chỉ vì trang nguồn có phiên bản mới.
4. Chạy lại audit, test, Ruff; đồng bộ `DATA_AUDIT.md`, `RUNBOOK.md`, manifest, README và hai đặc tả; mọi số liệu phải xuất phát từ code thực chạy. Không đánh dấu kiểm tra chéo của thành viên nhóm đã xong.
5. Ghi `reports/qa_response_step_01.md`: từng F1–F6, vị trí sửa, test/kết quả và các hạn chế còn lại. Giữ nguyên báo cáo review của Codex.

## Phạm vi và ràng buộc

- Chỉ sửa/hoàn thiện Bước 1 và ma trận RQ trung tính của Bước 2. Chưa tạo `wrangling.py`, dữ liệu processed, EDA, mô hình hay notebook phân tích ở lượt này. Khi sửa xong, báo kết quả để được review trước khi sang Bước 3–4.
- Giữ nguyên raw (nội dung và mtime), template, báo cáo Word/PDF khung cùng thay đổi người dùng hiện có. Không commit, push, xuất bản hoặc gửi tin nhắn bên ngoài.
- Mọi thử nghiệm đầu vào lỗi thực hiện bằng fixture ở thư mục tạm. Không xóa/đổi tên/ghi đè file raw thật để thử.
- Không đoán các phát hiện thống kê, loại listing cao giá, tỷ giá, điều kiện ANOVA hay độ lớn tương quan. Không gọi một dòng mỗi listing là độc lập thống kê.
- Ngày/hạn nộp theo README: 18/10/2026. Nếu có trở ngại thật, nêu chính xác và tiếp tục các phần độc lập làm được.
