# Kịch bản trình bày và demo — Nhóm 10

Bản chuẩn bị 12/10/2026; **chưa tổng duyệt thực tế**. Slide có ghi chú người trình bày. Lịch thuyết trình cụ thể chưa được giảng viên xác nhận riêng; hạn nộp đã biết là 18/10/2026.

## Trình bày 10 phút

| Slide | Người nói | Thời lượng | Nội dung cần truyền đạt |
|---|---|---:|---|
| 1. Đề tài và nhóm | Thắng | 45 giây | Tên đề tài, hai thành viên; nguồn Inside Airbnb; không tham khảo code/dự án mẫu, không tái sử dụng môn khác; AI hỗ trợ và trách nhiệm kiểm tra của nhóm. |
| 2. Bốn câu hỏi | Thắng | 40 giây | Giá, loại phòng, quy mô và khu vực; luồng trình bày. |
| 3. Dữ liệu | Thiện | 50 giây | Raw 31.069×90; baseline 28.987×16; một listing/snapshot; giá niêm yết THB/đêm. |
| 4. Làm sạch | Thiện | 50 giây | Loại 2.082 dòng thiếu giá; giữ 2.730 ngoại lệ IQR; giữ missing predictor và công bố n từng phép tính. |
| 5. RQ1 | Thắng | 65 giây | Median 1.592 và mean 2.955,96; lệch phải; phân biệt giới hạn trục và loại dữ liệu. |
| 6. RQ2 | Thắng | 70 giây | Trung vị từng loại phòng; n khác nhau; ANOVA F=5,9323, p=0,000485542 chỉ thăm dò. Q1–Q3 không phải CI. |
| 7. RQ3 | Thắng | 65 giây | r≈0,069–0,107 và p nhỏ; mức độ liên hệ khác ý nghĩa thống kê; Pearson/OLS toàn cặp hợp lệ. |
| 8. RQ4 | Thắng | 60 giây | So sánh trong Entire home/apt; Bang Phlat 678,03 và Samphanthawong 3.115,50; chưa tách tác động vị trí. |
| 9. Train/CV | Thiện | 70 giây | 0 biến số qua bộ lọc, điều kiện ANOVA chưa xác nhận; benchmark và R² âm nhỏ; giới hạn host overlap. |
| 10. Tổng hợp | Thắng | 85 giây | Kết nối bốn phát hiện với bằng chứng, giới hạn, ý nghĩa so sánh báo giá; chuyển sang demo. |
| **Tổng** | | **600 giây** | Không tính phần demo và Q&A. |

## Chuẩn bị trước buổi demo

1. Cả hai chạy `docs/RUNBOOK.md` trên máy trình bày; dùng `requirements-lock.txt`, mở notebook đúng kernel. Thắng kiểm tra nội dung; Thiện kiểm tra số liệu và môi trường.
2. Mở sẵn slide, PDF, notebook 01–04 và thư mục `reports/modeling/`; phóng to chữ khi trình chiếu.
3. Chạy thử notebook 04 từ kernel mới để đo thời gian thực. Không cài thư viện/tải dữ liệu lần đầu trong buổi demo; dữ liệu raw đã có checksum.
4. Tổng duyệt một lượt đủ 15 phút trước 17/10, ghi thời gian và vướng mắc. Kiểm tra cả màn hình chia sẻ và font. Nếu học online, thực hiện video có mặt tất cả thành viên theo thông báo của giảng viên.

## Demo 5 phút

| Khoảng thời gian | Thực hiện | Minh chứng trên màn hình |
|---|---|---|
| 0:00–0:45 | Thiện mở manifest, xác minh raw | Nguồn snapshot, đơn vị THB/đêm, hash trùng. |
| 0:45–1:30 | Thiện mở notebook 01 | Shape trước/sau; 2.082 dòng thiếu giá; không điền mục tiêu. |
| 1:30–2:30 | Thắng mở notebook 02–03 | Một hàng Pearson có r/p/n; hình tương ứng; lý do giới hạn trục không thay thống kê. |
| 2:30–3:45 | Thiện chạy notebook 04 từ kernel mới | Train/CV; feature selection; benchmark và model comparison không có hồi quy giả. |
| 3:45–4:30 | Thắng mở PDF | Đối chiếu Bảng 4 và Hình 4; Bảng 7 trùng artifact. |
| 4:30–5:00 | Cả hai chốt phạm vi | Một snapshot, không nhân quả, chưa dự báo host mới. |

Lệnh mở Jupyter từ thư mục đồ án:

```bash
source .venv/bin/activate
python -m jupyter notebook notebooks/04_regression_modeling.ipynb
```

Nếu không có giao diện Jupyter, lệnh thực thi tương đương trong RUNBOOK là `jupyter nbconvert --execute`. Đo thời gian trước; không khẳng định kết quả đã chạy trực tiếp nếu chỉ đang mở output lưu sẵn. Khi có lỗi trình chiếu, báo rõ lỗi và dùng PDF/output lần chạy được lưu để giải thích, không giả lập demo thành công.

## Gợi ý trả lời Q&A

- **Vì sao không xóa giá cao?** Chưa có cơ sở xác định mọi giá cao là lỗi. IQR chỉ đánh dấu 2.730 trường hợp; báo cáo giữ dữ liệu, mô tả ảnh hưởng qua phân phối và giới hạn.
- **p nhỏ mà r thấp?** Hai đại lượng trả lời hai khía cạnh khác nhau; mẫu lớn có thể cho p nhỏ khi độ lớn tương quan tuyến tính vẫn nhỏ. Không đồng nhất p với chất lượng dự báo.
- **Vì sao chưa có Linear/Ridge?** Bộ lọc đã chọn không cho predictor hợp lệ trong train/CV. Đây là giới hạn chính sách hiện tại, không phải định lý dữ liệu không mô hình hóa được. Không hạ ngưỡng sau khi xem test để ép kết quả.
- **Dummy có phải mô hình hồi quy cuối?** Là mốc dự đoán trung bình train để tham chiếu MSE/R². Không có predictor, hệ số hay alpha tối ưu cho Bangkok.
- **Sao R² âm rất nhỏ?** Mean train hơi khác mean test; SSE của dự đoán mean train hơi lớn hơn SST tính theo mean test. Test R²≈−0,000014334.
- **Nhóm có kiểm tra chủ nhà mới không?** Chưa. 82,81% listing test thuộc host đã thấy ở train; không báo cáo khả năng tổng quát hóa sang host mới.
