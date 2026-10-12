# Quy ước phương pháp EDA — sau review Bước 5–6

Bốn RQ và phạm vi chính theo `SPECIFICATION.md`; mọi thống kê dựa trên mẫu hữu hạn hợp lệ, chưa điền khuyết hay cắt ngoại lệ giá. Giá gốc THB/đêm. `n_missing` ở Pearson đếm dòng bị loại khỏi cặp do thiếu/sai định dạng/vô cực ở một trong hai biến.

- Phương sai/std mẫu dùng `ddof=1`; mẫu dưới 2 trả null, không ghi 0. Skewness và Fisher excess kurtosis EDA dùng `bias=False`. Audit sơ bộ trước đó dùng `bias=True`, nên số kurtosis EDA 3.094,3914 khác audit 3.093,8575; không trộn hai ước lượng trong báo cáo.
- |skew| >2 là cảnh báo mô tả của nhóm, không phải kiểm định chuẩn. Không dùng skew nhỏ để xác nhận phân phối chuẩn. `all_parametric_assumptions_met` chỉ false hoặc chưa xác định; không tự coi host ID duy nhất là độc lập thống kê.
- ANOVA tổng thể chỉ được trình bày thăm dò kèm F/p, n và giới hạn. Bỏ so sánh cặp khi điều kiện suy luận chưa xác nhận; không diễn giải các p riêng lẻ như kết luận chắc chắn. Nguồn giả định/ca suy biến: [SciPy f_oneway](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.f_oneway.html).

## Phần bổ sung được tách nhãn

**[MỞ RỘNG NGOÀI BÀI HỌC] Levene với `center='median'`**: dùng ở RQ2 để bổ sung chẩn đoán phương sai; chưa xác nhận API này trong slide. Nguồn: [SciPy Levene](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.levene.html). p≥0,05 chỉ là chưa bác bỏ giả thuyết, không chứng minh phương sai bằng nhau. Host clustering vẫn giới hạn p-value; không dùng phép kiểm này để tự xác nhận toàn bộ điều kiện ANOVA. Vị trí: `evaluate_anova_conditions`, notebook 02 và bảng RQ2.

**[MỞ RỘNG NGOÀI BÀI HỌC] `pd.qcut`**: minh họa riêng phân khoảng theo phân vị bên cạnh `pd.cut` khoảng đều trong Bài 02. Nguồn: [Pandas qcut](https://pandas.pydata.org/docs/reference/api/pandas.qcut.html). Mục đích là so sánh số lượng quan sát trong các khoảng, không khẳng định phương pháp nào tốt hơn với mọi mục tiêu. Giá trị trùng có thể không chia được đúng ba khoảng; phải trả trạng thái/nhóm trống thay vì làm hỏng pipeline. Các khoảng giá chỉ mô tả, không predictor.

## Quy tắc biểu đồ

1. RQ1: panel toàn miền dùng thang trục log10 để đọc phạm vi rộng; không tạo log(price) cho thống kê/mô hình. Histogram dùng số đếm trong từng khoảng có độ rộng khác nhau ở đơn vị gốc; không gọi là mật độ. Panel trung tâm có giới hạn trục và số ngoài khung thực tính; không lẫn với số ngoại lệ IQR.
2. RQ2: hộp, râu, trung vị và Q1/Q3 tính trên toàn bộ mẫu nhóm; phóng to chỉ thay `ylim`. Các đoạn Q1–Q3 mô tả độ phân tán quan sát, không phải khoảng tin cậy của trung vị.
3. RQ3: OLS/Pearson dùng toàn bộ cặp hợp lệ. Lấy mẫu seed42 chỉ để vẽ điểm; công bố số chọn, số vẽ thực và số ngoài khung, giữ cờ thiếu dữ liệu/constant. Không quy kết tương quan yếu do ngoại lệ khi chưa kiểm tra độ nhạy.
4. RQ4: heatmap so sánh trong từng loại phòng, ghi n và dấu * n<5; bar so sánh quận trong cùng `Entire home/apt`. Ngưỡng n≥20 chỉ là lựa chọn hiển thị, không bảo đảm tính đại diện hoặc loại bỏ sai số mẫu.

Catalog tính trực tiếp từ DataFrame dùng vẽ, có fingerprint và checksum nguồn khi có; không nhập tay số mẫu/điểm ngoài khung.
