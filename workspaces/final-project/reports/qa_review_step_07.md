# Review độc lập Bước 7 — Nhóm 10

Chốt tài liệu ngày 12/10/2026; kiểm thử và tái lập Bước 7 chạy ngày 11/10. Codex đã đọc mã, kiểm tra bàn giao của Claude Code, sửa các lỗi dưới đây và thực thi lại notebook 04. **Đạt kiểm tra kỹ thuật trong phạm vi hiện tại; chưa xác nhận kiểm tra chéo của Thắng/Thiện trên máy cá nhân.**

## Các điểm đã sửa

| Vấn đề trước review | Sửa và kiểm chứng |
|---|---|
| Diễn giải ANOVA gán sẵn mọi giả định đều vi phạm, tự loại nhóm một quan sát | Lưu group sizes, chẩn đoán và F/p thật ở từng fold; giữ tất cả nhóm. Full train property_type có 71 nhóm, không phải 60; kết quả ANOVA không tính được theo điều kiện tối thiểu được ghi rõ. Không dùng ANOVA làm bộ lọc khi giả định chưa xác nhận. |
| Lý do không chọn biến và tỷ lệ host overlap gắn cố định với Bangkok | Tính theo dữ liệu chạy; tách giới hạn chính sách khỏi kết luận về khả năng mô hình hóa dữ liệu. |
| Nhánh có đặc trưng chưa thật sự huấn luyện dù bàn giao nói đã hỗ trợ | Bổ sung estimator chọn biến trong mỗi training fold, Pipeline imputer/scaler, CV chọn Linear/Ridge và chỉ đánh giá winner trên holdout; kiểm thử bằng dữ liệu tổng hợp. Không đưa kết quả tổng hợp vào đồ án. |
| R² âm rất nhỏ bị ghi thành −0,0000; mean dự đoán có thể bị cắt phần lẻ khi y là số nguyên | Giữ độ chính xác số trong artifact; dùng mảng float cho benchmark. R² với y hằng được ghi null và giải thích, không dùng giá trị thay thế mặc định. |
| Kiểm tra giá hữu hạn/ID thiếu chưa đầy đủ; JSON có thể chứa giá trị không chuẩn | Từ chối giá vô hạn/ID thiếu; JSON strict, có phiên bản môi trường; test các trường hợp biên. |
| Notebook/generator chứa số liệu nhập tay và ghi đè mặc định | Notebook 04 đọc artifact từ workflow; template đồng bộ; generator chỉ ghi đè khi có cờ rõ ràng. |

Các regression test mới kiểm tra mean với y nguyên, R² không xác định, nhóm một quan sát, host diagnostics, chống rò rỉ fold, nhánh khả thi thật và vòng đời artifact. Kết quả: **91 tests passed, coverage src 89,18%**. Ruff được kiểm tra lại sau khi bổ sung script dựng báo cáo/slide; xem `qa_audit_report.md`.

## Kết quả dữ liệu thật

- Split: train 20.290 / test 8.697; 4-fold shuffle seed42. Chọn biến chỉ trên training fold tương ứng.
- Không biến số nào đạt đồng thời |r|≥0,30 và p<0,05 ở cả bốn fold và full train. Biến phân loại chưa được chọn do cơ sở dùng ANOVA làm bộ lọc chưa được xác nhận; xem chẩn đoán cụ thể trong `feature_selection.json`.
- Chưa xây hồi quy theo chính sách hiện tại; đây **không phải** bằng chứng dữ liệu không thể mô hình hóa. Không có mô hình hồi quy lưu, alpha tốt nhất hoặc biểu đồ phần dư hồi quy cho Bangkok.
- Benchmark mean train: 2.976,12 THB/đêm. Test MSE = 315.021.203,8296908 THB²; R² = −0,000014334218385370079. Số âm nhỏ được giữ, không trình bày như mô hình hoàn hảo hay hiệu quả dự báo tốt.
- 2.229 host xuất hiện ở cả hai tập; 7.202 listing test (82,81%) thuộc host đã thấy ở train. Chưa đánh giá khả năng dự báo host mới.

## Minh chứng

[JSON kiểm chứng](qa_step_07_verification.json) ghi kết quả độc lập: split/fold IDs trùng, r/p/n của mọi biến số trên mọi fold trùng, group sizes phân loại trùng; MSE/R² tính trực tiếp từ SSE/SST trùng. Chạy workflow ra thư mục tạm cho bốn artifact byte-identical và metadata bằng nhau sau bỏ timestamp. Notebook 04 có 5 code cells chạy đủ, không có error output.

[Log pytest/coverage](verification_step_07/pytest_coverage.log) và [log notebook](verification_step_07/notebook04.log). Raw giữ hash/mtime; baseline, template, năm hình EDA và các bảng EDA giữ hash. Word khung được lưu riêng trước khi tiếp tục Bước 8–9.

Phương pháp hiện hành: [MODELING_METHODS.md](../docs/MODELING_METHODS.md). Bản Claude bàn giao được giữ để truy vết ở [qa_response_step_07.md](qa_response_step_07.md), có nhãn lịch sử; không dùng những số liệu/diễn giải cũ trong báo cáo cuối.
