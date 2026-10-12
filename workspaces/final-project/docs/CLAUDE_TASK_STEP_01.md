# Giao việc Claude Code: môi trường và kiểm toán dữ liệu

Ngày giao: 10/10/2026. Hạn nộp đồ án: **18/10/2026**. Mốc nội bộ: môi trường 10/10; thu thập/kiểm toán và rà lại câu hỏi nghiên cứu 11/10. Đây là nhiệm vụ được người dùng giao cho Claude Code tiếp tục từ phần chuẩn bị tài liệu.

## Đọc trước khi thực hiện

- `AGENTS.md`, `CLAUDE.md` ở gốc repository; giữ các quy tắc liên quan Airbnb, không áp schema hay số mẫu Automobile vào đồ án.
- `workspaces/final-project/README.md`: lịch, phân công và trạng thái hiện tại.
- `workspaces/final-project/docs/SPECIFICATION.md`, nhất là mục 1.5, 4 và 7.
- `workspaces/final-project/reports/README.md`: trạng thái bản khung báo cáo.

Các thay đổi tài liệu hiện có có thể chưa commit. Giữ nguyên công việc này; không reset/checkout đè, không commit hoặc push. Không sửa template, báo cáo DOCX hoặc PDF khung trong nhiệm vụ này.

## Phạm vi cần hoàn thành

1. Thiết lập môi trường Python cho `workspaces/final-project/`, tạo `requirements.txt`, `requirements-dev.txt` và cấu hình Ruff/pytest phù hợp. Dùng môi trường ảo, không sửa môi trường Python hệ thống. Ghi phiên bản đã kiểm chứng và lệnh cài/chạy từ đúng thư mục.
2. Xác minh nguồn chính thức Inside Airbnb Bangkok và tải một bản detailed listings có thể truy cập. Phiên bản 29/06/2026 chỉ là ứng viên chưa xác minh, không được tự coi là tồn tại hoặc đã tải. Nếu không có phiên bản này, chọn bản Bangkok truy cập được, ghi lý do và cập nhật hai đặc tả đồng bộ. Không mở rộng sang calendar, reviews hoặc thành phố khác.
3. Lưu dữ liệu gốc mới vào `data/raw/`, không thay đổi/xóa/ghi đè dữ liệu thô đã có. Tạo `data/source_manifest.json`: URL nguồn và tải trực tiếp, phiên bản/ngày thu thập nếu xác định được, thời điểm tải, tên file, kích thước, SHA-256, giấy phép kèm nguồn, đơn vị quan sát và giới hạn chưa xác nhận. Chưa xác minh được thì ghi rõ, không đoán.
4. Viết `src/data_loader.py` và `src/data_audit.py` để đọc và kiểm toán dữ liệu. Xuất JSON tổng hợp và bảng cột/kiểu dữ liệu/missing vào `reports/audit/`. Kiểm tra kích thước, ID/trùng lặp, định dạng/giá thiếu/giá không hợp lệ, phạm vi ngày và mô tả sơ bộ giá. Xác minh tiền tệ và kỳ lưu trú dựa trên tài liệu nguồn; không suy từ tên Bangkok hoặc ký hiệu `$`. Không mặc định 31.069 dòng, 90 cột hay 28.987 giá hợp lệ.
5. Tạo `docs/DATA_AUDIT.md` theo 11 đầu mục trong đặc tả. Đối chiếu 12 biến ứng viên với schema thực; cập nhật ma trận bốn RQ–biến–phương pháp–biểu đồ–giới hạn. Nếu ý nghĩa giá chưa được xác minh, ghi kiểm toán còn thiếu điều kiện nghiệm thu; chưa tổng hợp/diễn giải giá như đã rõ đơn vị.
6. Viết test có ý nghĩa trong `tests/test_data_audit.py`: đọc/parse giá (thiếu, dấu phân cách, không hợp lệ), ID/trùng lặp theo đơn vị quan sát, checksum và dữ liệu thô không bị ghi lại. Test dùng fixture nhỏ, không cần truy cập mạng để chạy. Chạy kiểm toán trên file thực và các kiểm tra Ruff/pytest cần thiết.
7. Tạo `docs/RUNBOOK.md`: thư mục chạy, điều kiện tiên quyết, lệnh tạo môi trường/cài gói, lấy dữ liệu hoặc sử dụng file đã tải, chạy kiểm toán và test; giải thích đầu ra, lỗi thường gặp và tiêu chí nghiệm thu. Chỉ ghi lệnh thực sự tồn tại và đã kiểm tra.
8. Cập nhật README và đồng bộ hai bản đặc tả về phiên bản và trạng thái đã chứng minh. Không đánh dấu nhóm đã kiểm tra chéo khi chỉ có Claude chạy test. Ghi rõ việc còn thiếu và đường dẫn kết quả.

## Ràng buộc

- Chỉ triển khai môi trường, ingestion và audit; chưa làm sạch chính thức, chưa điền khuyết, chưa EDA chuyên sâu/ANOVA/Pearson/mô hình, chưa dựng dashboard.
- Code/tên biến dùng tiếng Anh; docstring, giải thích và báo cáo kiểm toán dùng tiếng Việt. Seed 42 nếu phát sinh ngẫu nhiên. Chỉ đọc các file thô sau khi tải xong.
- Bảo vệ thay đổi hiện có. Không gửi tin nhắn bên ngoài, không xuất bản hay chia sẻ dữ liệu công khai. Không bỏ qua xác thực, paywall hoặc cơ chế hạn chế truy cập nguồn.
- Nếu nguồn hoặc tài khoản chặn, tiếp tục phần môi trường, script, fixture và hướng dẫn làm được; báo chính xác phần chưa xác minh, không sinh dữ liệu Airbnb giả để điền kết quả.

## Báo cáo khi kết thúc

Nêu các tệp đã tạo/sửa, nguồn và phiên bản thực dùng, số liệu kiểm toán có thể tái lập, lệnh kiểm tra và kết quả, các giới hạn còn lại, cùng bước tiếp theo. Kết quả thống kê chỉ lấy từ code đã chạy.
