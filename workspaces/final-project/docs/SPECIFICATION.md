# ĐẶC TẢ THIẾT KẾ ĐỒ ÁN MÔN HỌC IE313 (SPECIFICATION)

## Đề Tài: Phân Tích Và Trực Quan Hóa Giá Thuê Airbnb Tại Bangkok Và Các Yếu Tố Liên Quan

- **Môn học**: Phân tích và trực quan dữ liệu (Data Analysis and Visualization) - Mã môn: `IE313`
- **Lớp**: `IE313.F32.LT.CNTT` (Hệ Liên thông Đại học - Khoa CNTT, Trường Đại học Công nghệ Thông tin, ĐHQG-HCM)
- **Giảng viên phụ trách**: ThS. Phạm Thế Sơn
- **Nhóm thực hiện**: Nhóm 10 — 2 thành viên
  - 1. Phạm Quốc Thắng - MSSV: 25410304 - Ngành: CNTT
  - 2. Lê Minh Thiện   - MSSV: 25410313 - Ngành: CNTT
- **Phân công dự kiến**:
  - Phạm Quốc Thắng: Trưởng nhóm, phân tích và trực quan hóa, tổng hợp báo cáo và slide.
  - Lê Minh Thiện: Tiền xử lý, kiểm định thống kê, mô hình bổ trợ và đánh giá.
- **Tài liệu căn cứ bắt buộc**:
  - `workspaces/final-project/docs/Template_IE313.docx` (Template báo cáo Word chính thức)
  - `workspaces/final-project/docs/Slides.pptx` (Template slide thuyết trình chính thức)
  - `slide-study/` (Hệ thống 8 bài giảng PDF môn học IE313)
  - `CLAUDE.md` & `AGENTS.md` (Quy chuẩn kỹ thuật và hệ thống đa tác tử)

---

## 1. Định Vị Đề Tài & Mục Tiêu Cốt Lõi

### 1.1 Triết lý tiếp cận môn học

Đề tài vận dụng quy trình **Nhập dữ liệu → Tiền xử lý → EDA → Trực quan hóa → Mô hình hóa → Đánh giá** của môn học. Phân bổ công sức dự kiến dưới đây là **lựa chọn của nhóm, không phải tỷ trọng chấm điểm của giảng viên**:
- **Trọng tâm khoảng 80%**: Kiểm toán/làm sạch, EDA, trực quan hóa, diễn giải và báo cáo theo bốn câu hỏi ở mục 1.5.
- **Phần mô hình khoảng 20%**: Linear Regression và Ridge, Pipeline, CV và chẩn đoán trong Bài 06–07. Chỉ thêm đa thức bậc thấp khi có lý do từ train/CV. Diễn giải hệ số trong phạm vi mô hình; không xem độ lớn hệ số là kiểm định ý nghĩa thống kê. Đây là phân bổ dự kiến, không cam kết R² hay kết quả có ý nghĩa trước thực nghiệm.

### 1.2 Mục tiêu cụ thể

1. Thu thập và kiểm toán bộ dữ liệu Inside Airbnb Bangkok; phiên bản 29/06/2026 là ứng viên từ kế hoạch cũ, cần xác minh khả năng tải và nội dung trước khi cố định phiên bản.
2. Làm sạch dữ liệu có cơ sở khoa học (Data Cleaning có giải trình: Vấn đề $\rightarrow$ Cách xử lý $\rightarrow$ Lý do $\rightarrow$ Ảnh hưởng).
3. Phân tích đặc trưng phân bố của biến mục tiêu trung tâm: Giá thuê (`price`).
4. Kiểm định mối liên hệ giữa các đặc điểm của listing (định lượng và định tính) với giá thuê bằng thống kê mô tả, tương quan Pearson ($r$, $p$-value), và phân tích phương sai ANOVA ($F$, $p$-value) theo Bài 05.
5. Xây dựng hệ thống đồ họa trực quan trả lời các câu hỏi nghiên cứu cụ thể, tuân thủ Matplotlib Object-Oriented API và nguyên tắc trực quan hóa bài 03 & 04.
6. Tổng hợp các phát hiện then chốt thành các khuyến nghị thực tiễn có số liệu minh chứng cụ thể.

### 1.3 Phạm vi kiến thức và bảng đối chiếu bài giảng

**Nguồn xác định nội dung đã học là 8 PDF trong `slide-study/`.** `AGENTS.md` và `CLAUDE.md` quy định cách triển khai trong repository; template Word/PowerPoint quy định sản phẩm trình bày. Không mặc nhiên coi mọi kỹ thuật được nhắc trong tài liệu quản trị là nội dung đã giảng.

Số trang dưới đây là **trang PDF tính từ 1**, không phải số slide in trên trang (nhiều PDF chứa hai slide/trang). Đây là kế hoạch áp dụng, chưa phải kết quả phân tích dữ liệu Airbnb.

| Bài học / nguồn gốc | Nội dung dùng trong đồ án | Minh chứng dự kiến |
|---|---|---|
| [TH 01 — Python cho phân tích dữ liệu](../../../slide-study/Bai_Giang_TH_01_Python_for_DA.pdf), phần kiểu dữ liệu, hàm, Pandas; tr. 28–31 | Kiểu dữ liệu, hàm, thao tác Series/DataFrame | Hàm xử lý tái sử dụng trong `src/`, các notebook |
| [Bài 01 — Nhập/xuất dữ liệu](../../../slide-study/Bai01_Gioi_thieu_PTDL-Nhap_Xuat_Bo_du_lieu.pdf), tr. 14–21 | Đọc file bằng Pandas, xem dữ liệu và kiểu dữ liệu, thống kê ban đầu, xuất dữ liệu | Notebook 01: nguồn dữ liệu, `shape`, `head`, `info`, `dtypes`, bảng mô tả biến và file sạch |
| [Bài 02 — Sắp xếp dữ liệu](../../../slide-study/Bai02_Sap_xep_DL.pdf), tr. 4–23 | Xử lý khuyết, ép kiểu/đơn vị; simple feature scaling, Min-Max, Z-score; binning; `get_dummies` | Notebook 01: bảng giải trình làm sạch; minh họa chuẩn hóa, chia khoảng, dummy khi có biến phù hợp |
| [Bài 03 — Trực quan dữ liệu](../../../slide-study/Bai03_Truc_quan.pdf), tr. 19–26, 29–39 | Kiến trúc Matplotlib, Figure/Axes và phương thức vẽ | Notebook 03: biểu đồ có tiêu đề, nhãn, đơn vị, chú giải; triển khai OO theo quy chuẩn repository |
| [Bài 04 — Công cụ trực quan](../../../slide-study/Bai04_Cong_cu_TQ.pdf), tr. 4–5, 6–67 | Quy trình 5 bước; line, area, histogram, bar, pie, box, scatter; waffle, word cloud, dashboard | Notebook 03: ưu tiên histogram, boxplot, bar, scatter; các dạng còn lại chỉ dùng nếu trả lời được RQ từ dữ liệu thực |
| [Bài 05 — EDA](../../../slide-study/Bai05_PT_Tham_do.pdf), tr. 4–20, 24–37 | Mean/median/mode, 5 số, phương sai/std/CV, skewness/kurtosis, IQR; Pearson; `groupby`, pivot, heatmap; ANOVA và so sánh cặp nhóm | Notebook 02: bảng thống kê, bảng $r$–$p$, bảng $F$–$p$, bảng nhóm/pivot và diễn giải |
| [Bài 06 — Phát triển mô hình](../../../slide-study/Bai06_Mo_hinh.pdf), tr. 3–15, 16–22, 23–40 | Hồi quy tuyến tính đơn/đa biến, hồi quy đa thức; StandardScaler và Pipeline; regression/residual/distribution plot; **MSE, $R^2$** | Notebook 04: mô hình cơ sở, thử đa thức bậc thấp khi phù hợp, chẩn đoán phần dư, so sánh phân phối thực–dự đoán |
| [Bài 07 — Đánh giá mô hình](../../../slide-study/Bai07_Danh_gia_MH.pdf), tr. 3–10, 11–32 | Train/test, K-Fold CV, `cross_val_score`, `cross_val_predict`; overfitting/underfitting; Ridge và chọn alpha bằng CV | Notebook 04: MSE/$R^2$ trên train/test, kết quả CV, nhận xét độ khớp, so sánh Ridge |

Không bắt buộc dùng mọi dạng biểu đồ hoặc mọi cách chuẩn hóa. Chọn phương pháp phù hợp câu hỏi; nêu lý do không áp dụng khi dữ liệu thiếu điều kiện. Không áp dụng công thức mpg → L/100km hay schema Automobile/Canada vào Airbnb.

### 1.4 Phân biệt nội dung học, quy ước triển khai và phần mở rộng

| Nội dung | Phân loại và cách áp dụng |
|---|---|
| MAE, RMSE | **Bài giảng giao tìm hiểu thêm**: Bài 07 tr. 9–10 (slide 18–19). Có thể báo cáo bổ sung, nhưng không thay thế MSE và $R^2$ là thước đo cốt lõi. |
| KNNImputer | **Bài giảng giao tìm hiểu thêm**: Bài 02 tr. 10. Không cần dùng mặc định; ưu tiên xử lý khuyết đơn giản có giải trình. |
| Waffle, word cloud, dashboard | **Có trong Bài 04**, tr. 58–67; không phải nội dung ngoài môn. Chỉ triển khai nếu dữ liệu và RQ phù hợp. Word cloud mô tả tần suất từ, không phải phân tích cảm xúc. |
| OO API bắt buộc, font tiếng Việt, ảnh 300 DPI, dữ liệu thô bất biến | **Quy chuẩn repository** (`AGENTS.md`, `CLAUDE.md`). Bài 03 có cả pyplot, nên không ghi rằng bài giảng cấm pyplot. |
| `random_state=42`, `KFold(n_splits=4, shuffle=True, random_state=42)` | **Quy ước repository**. Bài 07 tr. 4 minh họa seed 0; tr. 8 minh họa `cv=3`. Áp dụng seed 42/CV 4-fold nhất quán và ghi đúng nguồn. |
| `SimpleImputer` trong Pipeline; `GridSearchCV` để chọn alpha | **Bổ sung triển khai theo repository, chưa xác nhận API này trong PDF**. Phương pháp điền khuyết, Pipeline và chọn alpha bằng CV có trong bài. Nếu dùng các API này, ghi nhãn “Bổ sung kỹ thuật theo repository”, nêu chức năng và vị trí code; không gán tên API cho slide. |
| Spearman; Decision Tree/Random Forest; SHAP hoặc permutation importance | **Ngoài phạm vi đã xác nhận trong 8 PDF; không dùng trong kế hoạch mặc định**. Dùng Pearson, hồi quy tuyến tính/đa thức và Ridge để hoàn thành phần chính. |
| Biến đổi log của `price`, winsorization, kiểm định thay thế/hậu kiểm chuyên biệt, tính khoảng cách địa lý, NLP/phân tích cảm xúc | **Ngoài phạm vi đã xác nhận; không tự bổ sung** chỉ vì dữ liệu có tọa độ, văn bản hay phân phối lệch. Mặc định phân tích trên giá và biến quan sát gốc. |

Nếu thật sự cần dùng kiến thức ngoài bài học, ghi ngay tại mục phương pháp, ô Markdown trước code và chú thích kết quả liên quan theo mẫu:

> **[MỞ RỘNG NGOÀI BÀI HỌC]** Tên kỹ thuật: …; dùng để trả lời RQ: …; lý do phương pháp trong bài chưa đáp ứng: …; nguồn tham khảo cụ thể: …; vị trí áp dụng: …; ảnh hưởng và giới hạn khi diễn giải: …

Phần mở rộng phải tách khỏi kết quả cốt lõi. Phân tích chính giữ phương pháp trong bài học; kiểm tra độ nhạy theo chủ nhà, nếu triển khai, ghi nhãn mở rộng và trình bày riêng theo mục 4.2. `ColumnTransformer`/`OneHotEncoder` là bổ sung triển khai cho Pipeline hỗn hợp số–phân loại, không gán tên API cho bài giảng chưa xác nhận.

### 1.5 Phạm vi Bangkok và trạng thái xác minh ngày 10/10/2026

- **Nguồn dự kiến**: Inside Airbnb Bangkok. Bước 1 phải lưu URL tải trực tiếp, phiên bản, ngày tải, điều khoản sử dụng/giấy phép và SHA-256 tại `data/source_manifest.json`; hiện chưa có manifest trong repo.
- **Bản dữ liệu**: Chưa có file Airbnb trong repo. Phiên bản 29/06/2026 và tên `data/raw/bangkok_listings_2026-06-29.csv.gz` là dự kiến, chưa xác nhận. Các con số 31.069 dòng × 90 cột, 31.069 ID duy nhất và 28.987 dòng có giá từng ghi trong bản cũ **chưa có minh chứng tái lập trong repo, không được dùng như kết quả đã kiểm toán**.
- **Đơn vị quan sát dự kiến**: Một listing trong một đợt phát hành; phải xác minh bằng dữ liệu thực. Khoảng ngày `last_scraped` chưa xác nhận; không đồng nhất nhãn phát hành với thời điểm quan sát của mọi dòng.
- **Giá mục tiêu dự kiến**: Báo giá theo đêm; tiền tệ THB, ý nghĩa ký hiệu `$`, kỳ lưu trú, thuế/phí và quan hệ giữa `price` với cột báo giá phụ trợ đều phải xác minh ở Bước 1. Chỉ gắn nhãn THB/đêm khi có bằng chứng nguồn. Không suy ra giá giao dịch, doanh thu hoặc chênh lệch trong điều kiện đặt phòng đồng nhất.
- **12 biến ứng viên cần kiểm tra sự hiện diện và ý nghĩa**: `price`, `room_type`, `property_type`, `neighbourhood_cleansed`, `accommodates`, `bedrooms`, `bathrooms`, `beds`, `minimum_nights`, `number_of_reviews`, `review_scores_rating`, `host_is_superhost`. Chưa phải schema được xác nhận hay tập biến được chọn cho mô hình.
- **Cột phụ trợ cần kiểm tra nếu có**: `id`, `host_id`, `source`, `last_scraped`, `price_quote_*`; không đưa định danh hoặc các cột báo giá vào biến dự báo. Không sử dụng `estimated_revenue_l365d` để dự đoán giá.
- **Giới hạn triển khai**: Một thành phố, một bản listings; chưa mở rộng calendar, NLP, bản đồ, dashboard hoặc so sánh nhiều thành phố. Không mặc định mẫu dữ liệu đại diện toàn bộ thị trường Bangkok.

Bốn RQ bên dưới là thiết kế dự kiến; cột biến phải đối chiếu dữ liệu thực và được nghiệm thu ở Bước 2.

| Câu hỏi | Biến dự kiến, cần xác minh | Phương pháp và hình dự kiến | Giới hạn cần nêu |
|---|---|---|---|
| RQ1: Báo giá phân bố thế nào? | `price` | Mean/median, 5 số, IQR, skew/kurt; histogram/boxplot (Bài 03–05) | Chỉ trên giá quan sát; không điền giá thiếu, không tự xóa giá cao |
| RQ2: Giá khác nhau thế nào giữa loại phòng? | `price`, `room_type`; `property_type` để mô tả bổ sung | Thống kê nhóm, boxplot, ANOVA khi đủ điều kiện (Bài 05 tr. 28–36) | Báo cáo n và chênh lệch thực tế; không suy diễn nhân quả |
| RQ3: Quy mô chỗ ở liên hệ thế nào với giá? | `accommodates`, `bedrooms`, `bathrooms`, `beds`, `price` | Scatter, Pearson r–p, heatmap (Bài 05 tr. 24–27) | Dùng mẫu hợp lệ từng cặp; rating chỉ là phân tích phụ, không ép thêm RQ |
| RQ4: Giá khác nhau thế nào giữa khu vực? | `neighbourhood_cleansed`, `price`, `room_type` | Groupby/pivot, boxplot/bar/heatmap; ANOVA khi phù hợp | So sánh thêm trong cùng loại phòng; không gọi nhóm ít mẫu là cao/thấp nhất thị trường |
| Mô hình bổ trợ: Dự đoán báo giá tốt đến đâu? | Các biến được chọn hợp lệ từ tập ứng viên, không có thông tin giá gián tiếp | Linear Regression, Ridge, CV 4-fold, MSE/R² và residual/distribution plot (Bài 06–07) | Không dự báo doanh thu hay giá tương lai; không lấy R² cao làm điều kiện đạt |

Đầu ra dự kiến Bước 1: `docs/DATA_AUDIT.md`, `src/data_audit.py` và `reports/audit/` tính từ gốc đồ án. Các tệp này chưa có; lệnh `python src/data_audit.py` chỉ sử dụng được sau khi triển khai. Chưa có kết quả Pearson/ANOVA, mô hình hay notebook phân tích.

---

## 2. Nguyên Tắc Bất Biến & Chống Bịa Đặt Dữ Liệu (Anti-Hallucination Policy)

Đây là nguyên tắc sống còn của đồ án, được thực thi nghiêm ngặt trong mọi giai đoạn:

### 2.1 Ràng buộc về Lược đồ (Zero-Assumption on Schema)

- Schema Bangkok chưa được kiểm tra trong repo hiện tại. Bước 1 phải xuất danh mục cột thực tế, kiểu dữ liệu, missing và mô tả nguồn vào `reports/audit/bangkok_columns.csv`. Không cố định trước số cột; kiểm tra tên trường điểm đánh giá, chẳng hạn `review_scores_rating`, thay vì tự đặt tên `rating`.
- Khi thay phiên bản dữ liệu, kiểm toán lại từ `df.info()`, `df.columns`, `df.dtypes`; không mang số liệu của phiên bản cũ hoặc con số chưa xác minh sang bản mới.
- Nếu một cột không có tài liệu mô tả rõ ràng, bắt buộc ghi chú: *"Chưa đủ thông tin để xác định"* thay vì đoán mò ý nghĩa.

### 2.2 Ràng buộc về Kết quả (Zero-Fabrication on Results)

- **Nghiêm cấm bịa đặt bất kỳ kết luận thống kê nào** trước khi chạy mã nguồn thực tế.
  - *Ví dụ vi phạm*: Tự viết "Entire home có giá cao nhất", "Giá phân phối lệch phải", "Rating không ảnh hưởng đến giá", "R² đạt 0.82" khi chưa chạy dữ liệu.
- Mọi nhận định trước khi có kết quả tính toán đều phải được gọi tên chính xác là: **"Câu hỏi nghiên cứu cần kiểm nghiệm (Research Questions / Hypotheses to Test)"**, không phải kết quả đạt được.
- Khi báo cáo kết quả, mọi khẳng định bắt buộc phải kèm theo số liệu định lượng làm bằng chứng (ví dụ: mean, median, IQR, hệ số tương quan $r$, giá trị $p$-value, $F$-score, phần trăm sai khác).

### 2.3 Ranh giới ngôn ngữ học thuật (No Causal Claims)

- Phân biệt tuyệt đối giữa **Tương quan thống kê (Correlation)** và **Quan hệ nhân quả (Causation)**:
  - **Khuyến nghị sử dụng**: *"có mối liên hệ với"*, *"có sự khác biệt về giá giữa"*, *"có tương quan thuận/nghịch với"*, *"có đóng góp vào khả năng giải thích mức giá"*.
  - **Nghiêm cấm sử dụng**: *"A làm giá tăng"*, *"B khiến giá giảm"*, *"yếu tố C gây ra mức giá đắt"* khi đồ án không có thiết kế thử nghiệm nhân quả (causal inference).

---

## 3. Quy Chuẩn Cấu Trúc Báo Cáo Word & Danh Mục Bàn Giao (Template_IE313.docx)

Báo cáo và hồ sơ nộp tuân thủ `Template_IE313.docx`. Các lựa chọn phân bổ nội dung của nhóm được ghi riêng, không coi là yêu cầu nguyên văn của giảng viên.

### 3.1 Danh mục sản phẩm bàn giao & Quy định nộp bài

Theo đúng hướng dẫn cuối trang của `Template_IE313.docx`, đồ án môn học gồm các sản phẩm sau:

1. **Báo cáo (Report)**: File Word (`Nhom10_Bao_cao.docx`) và File PDF (`Nhom10_Bao_cao.pdf`). Nộp file mềm trực tiếp, không in ra giấy.
2. **Mã nguồn (Code & Demo)**: Toàn bộ Jupyter Notebooks (`notebooks/*.ipynb`) và module Python (`src/*.py`) chạy thông suốt từ đầu đến cuối không phát sinh lỗi.
3. **Bộ dữ liệu (Data)**: Dữ liệu thô gốc (`data/raw/`) và dữ liệu sạch (`data/processed/`).
4. **Slide thuyết trình**: File PowerPoint (`Nhom10_Slides.pptx`).
5. **Video thuyết trình**: Đối với hệ học TRỰC TUYẾN, nộp thêm video thuyết trình thấy rõ mặt tất cả thành viên qua MS Teams.

#### Quy tắc nộp bài nghiêm ngặt

- **Nộp từng file trực tiếp, KHÔNG NÉN TOÀN BỘ CÁC SẢN PHẨM THÀNH 1 FILE .ZIP/.RAR DUY NHẤT** (Quy định template: *"Nộp từng file, KHÔNG nén cho các sản phẩm 1, 2, 3"*).
- **Quy tắc đặt tên file**: Mọi sản phẩm nộp bắt buộc bắt đầu bằng tên nhóm: `Nhom10_...` (ví dụ: `Nhom10_Bao_cao.docx`, `Nhom10_Bao_cao.pdf`, `Nhom10_Slides.pptx`).
- **Quy định file dung lượng lớn & Chênh lệch trong template (50 MB vs 60 MB)**:
  - **Dataset**: Mục “Đồ án môn học gồm các sản phẩm sau” ghi `> 60 MB`, mục “Chú ý nộp” ghi `> 50 MB`. Nhóm tạm dùng mốc `> 50 MB` cho dataset theo mục “Chú ý nộp” và ghi nhận cần xác minh với GVHD trước khi nộp.
  - **Video**: Template ghi `> 60 MB`; không áp mốc 50 MB của dataset sang video.
  - Khi thuộc trường hợp nộp qua Drive, tạo `Nhom10_Dataset.docx` hoặc `Nhom10_Video.docx` chứa liên kết cho phép giảng viên tải không cần đăng nhập. Không dùng link Drive để nộp toàn bộ sản phẩm.

### 3.2 Quy định hình thức & Dung lượng bài viết

- **Độ dài phần thân**: Từ 05 trang đến tối đa 10 trang tính từ mục *GIỚI THIỆU* đến *KẾT LUẬN* (Không tính trang bìa, trang Tài liệu tham khảo và các trang Phụ lục).
- **Tuyệt đối không đưa mã nguồn (source code) dài vào nội dung chính của báo cáo**. Toàn bộ mã nguồn nằm trong notebook/script nộp kèm; nếu cần minh họa giải thuật chỉ tóm tắt bằng lưu đồ hoặc đưa vào Phụ lục code.
- **Không tự thêm các phần template không yêu cầu**: Không viết Lời cảm ơn, Tóm tắt (Abstract), Mục lục, hay các chương lý thuyết giáo trình dài dòng.
- **Quy chuẩn Font & Đoạn**:
  - Tiêu đề cấp 1 dùng Style `Heading 1` (Chữ IN HOA).
  - Tiêu đề cấp 2 dùng Style `Heading 2`.
  - Nội dung đoạn văn dùng Style `BT` từ template. Không đặt giãn dòng cố định 1,15 điểm: văn bản mẫu ghi “1.15pt” nhưng style BT trong file có `lineRule=auto`, `line=240`; giữ style gốc và kiểm tra bản PDF khi xuất.
  - Gạch đầu dòng dùng Style `G1`, ý con dùng `G2`.
  - Bảng biểu và hình ảnh phải có số thứ tự và tên rõ ràng (Bảng 1, Hình 1...).
  - Footer ghi tên thành viên tắt (hoặc để trống nếu nhóm đông theo hướng dẫn template).

### 3.3 Nội dung chi tiết từng chương mục

Đây là **bố cục đề xuất của nhóm** theo template; các mục 4–7 có thể gộp làm tiểu mục để giữ phần thân 5–10 trang. Template không bắt buộc chín chương riêng, không quy định ngưỡng 15 cột hay cột “Mức độ hoàn thành” trong bảng phân công; đó là lựa chọn trình bày của nhóm.

```text
TRANG BÌA (Theo đúng mẫu template, KHÔNG ghi tên GVHD)
  ├── TÊN ĐỀ TÀI (IN HOA, TỐI ĐA 3 DÒNG)
  ├── Nhóm 10
  └── Bảng thông tin sinh viên thực hiện (STT, Họ tên, MSSV, Ngành)

1. GIỚI THIỆU (Heading 1 - Viết đúng khoảng 10 dòng hoặc nửa trang, chia làm 2 đoạn, KHÔNG gạch đầu dòng)
  ├── Đoạn 1: Trả lời 4 câu hỏi kiểm nghiệm:
  │     (1) Đề tài này là gì / làm gì?
  │     (2) Mục tiêu của đề tài là gì?
  │     (3) Làm như thế nào? (công cụ: Python, Pandas, Matplotlib; giải pháp: EDA, ANOVA, hồi quy đa biến)
  │     (4) Tóm tắt kết quả nổi bật đạt được (cập nhật sau khi chạy xong phân tích).
  └── Đoạn 2: Cam kết minh bạch đề tài và bộ dữ liệu:
        - Nêu rõ xuất xứ bộ dữ liệu (tự thu thập tại... hoặc tham khảo tại...).
        - Cam kết phần công việc nhóm tự thiết kế, phân tích và thực hiện; nêu rõ phần tham khảo nếu có.

2. MÔ TẢ BỘ DỮ LIỆU (Heading 1 - BẮT BUỘC)
  ├── 2.1. Tổng quan bộ dữ liệu:
  │     - Nguồn gốc, phạm vi không gian, thời điểm thu thập (nếu có).
  │     - Kích thước: Số dòng, số cột; đối tượng quan sát của mỗi dòng (listing).
  │     - Phân loại biến: Số biến định lượng (numerical), số biến định tính (categorical).
  │     - Đánh giá sơ bộ: Số lượng giá trị khuyết (missing values), số dòng trùng lặp (duplicates).
  └── 2.2. Bảng mô tả biến (Bảng 1):
        - Bắt buộc dùng đúng 5 cột: [STT | Tên cột | Kiểu dữ liệu | Phạm vi | Giải thích].
        - Theo lựa chọn trình bày của nhóm, nếu số lượng cột quá lớn (> 15 cột), chọn lọc các biến quan trọng vào bảng chính, chuyển toàn bộ danh sách chi tiết xuống Phụ lục.

3. PHƯƠNG PHÁP PHÂN TÍCH (Heading 1)
  ├── Hình 1: Sơ đồ quy trình phân tích dữ liệu thực tế do nhóm tự vẽ (KHÔNG copy hình mẫu trong template).
  ├── 3.1. Quy trình thực hiện (Mô tả các chặng từ Ingestion -> Wrangling -> EDA -> Visualization -> Modeling -> Evaluation).
  ├── 3.2. Phương pháp làm sạch dữ liệu (Nguyên tắc xử lý missing, ép kiểu, outlier).
  ├── 3.3. Phương pháp phân tích thống kê (Thống kê mô tả, Pearson, One-way ANOVA F-test).
  └── 3.4. Phương pháp trực quan hóa (Quy chuẩn Matplotlib OO API, bảng màu, biểu đồ theo câu hỏi).

4. TIỀN XỬ LÝ DỮ LIỆU (DATA CLEANING) (Heading 1 hoặc Heading 2 thuộc Phương pháp)
  └── Trình bày từng vấn đề phát hiện theo cấu trúc 4 bước:
        Vấn đề phát hiện ──> Cách xử lý ──> Lý do khoa học ──> Ảnh hưởng đến dữ liệu
        - Kiểm tra định dạng tiền tệ và ép kiểu giá về số thực (`float`).
        - Xử lý giá trị bằng 0, giá trị âm hoặc giá trị vô lý.
        - Xử lý giá trị khuyết trên biến mục tiêu: Bắt buộc loại bỏ dòng nếu thiếu target price.
        - Xử lý trùng lặp (duplicates) sau khi đã xác nhận rõ đơn vị quan sát.
        - Phân tích outlier giá: Phân biệt rõ outlier do sai sót dữ liệu với listing cao cấp hợp lệ (Penthouse/Villa) trước khi quyết định lọc hay giữ.
        - PHÂN ĐỊNH 2 NHÁNH XỬ LÝ: Nhánh EDA làm sạch cơ bản vs Nhánh Modeling chống rò rỉ dữ liệu (xem mục 4 bên dưới).

5. PHÂN TÍCH THĂM DÒ (EDA) & TRỰC QUAN HÓA (Heading 1)
  └── Nguyên tắc: "Mỗi biểu đồ phải trả lời một câu hỏi nghiên cứu cụ thể".
        Cấu trúc trình bày mỗi visual:
        Câu hỏi nghiên cứu (RQ) ──> Biểu đồ trực quan ──> Quan sát số liệu ──> Kết luận ý nghĩa
        - RQ1–RQ4 theo đúng bảng mục 1.5; tên khu vực giữ theo nguồn Bangkok.
        - Không thêm câu hỏi chỉ để đủ số lượng kỹ thuật hoặc biểu đồ.

6. PHÂN TÍCH CÁC YẾU TỐ LIÊN QUAN ĐẾN GIÁ (Heading 1 - TRỌNG TÂM ĐỒ ÁN)
  └── Với từng yếu tố được chứng minh có liên hệ đáng chú ý với giá, áp dụng khung 6 bước:
        1. Mô tả biến (Ý nghĩa thực tế của đặc trưng).
        2. Thống kê tóm tắt theo từng nhóm hoặc dải giá trị.
        3. Biểu đồ trực quan hóa chuyên sâu với biến price.
        4. Kiểm định thống kê (Pearson r + p-value hoặc ANOVA F-score + p-value, alpha = 0.05).
        5. Nhận xét phân tích khách quan từ số liệu.
        6. Kết luận về mức độ liên hệ và khả năng giải thích giá.

7. MÔ HÌNH HỒI QUY & ĐÁNH GIÁ (BÀI 06–07; GIẢI TRÌNH NẾU DỮ LIỆU KHÔNG PHÙ HỢP)
  ├── Mục tiêu: Đánh giá khả năng giải thích/dự đoán giá và diễn giải hệ số trong phạm vi mô hình.
  ├── Linear Regression đơn/đa biến; thử PolynomialFeatures bậc thấp; so sánh Ridge khi phù hợp.
  ├── Pipeline chuẩn hóa và biến đổi; chia train/test 70/30, CV trên train, chọn alpha Ridge.
  ├── Bắt buộc báo cáo MSE và R²; MAE/RMSE là phần tìm hiểu thêm của Bài 07.
  ├── So sánh sai số train/CV để nhận xét overfitting/underfitting; test dùng đánh giá cuối.
  └── Regression plot, Residual Plot và Distribution Plot thực–dự đoán; không suy diễn nhân quả.

8. KẾT QUẢ PHÂN TÍCH (Heading 1)
  └── Tổng hợp 3–4 phát hiện có bằng chứng; có thể gồm kết quả chưa đủ bằng chứng thống kê.
        Mỗi phát hiện được cấu trúc nghiêm ngặt:
        Số liệu thực nghiệm ──> Phân tích Insight ──> Ý nghĩa kinh tế / thực tiễn
        (Không liệt kê lại toàn bộ mô tả EDA).

9. KẾT LUẬN (Heading 1 - Đúng khoảng 10 dòng hoặc nửa trang)
  └── Cấu trúc 5 phần liên hoàn:
        Mục tiêu ban đầu ──> Bộ dữ liệu đã dùng ──> Phương pháp áp dụng ──> 3-4 kết quả nổi bật nhất ──> Các hạn chế còn tồn đọng của nghiên cứu

TÀI LIỆU THAM KHẢO (Đúng chuẩn quy định của GV trong template)
  ├── Tài liệu sách, bài báo: Họ tên tác giả, Tên bài, Năm.
  └── Tài liệu internet: Tên bài viết, Link, Ngày truy cập (hạn chế blog cá nhân, wikipedia, mxh).

PHỤ LỤC PHÂN CÔNG NHIỆM VỤ (Bắt buộc theo template)
  └── Bảng phân công chi tiết công việc cho từng thành viên Nhóm 10 (STT, Thành viên, Nhiệm vụ cụ thể, Mức độ hoàn thành).
```

---

## 4. Kiến Trúc Phân Tách Nhánh Xử Lý & Chống Rò Rỉ Dữ Liệu (Zero Data Leakage)

Quy trình vận dụng Pipeline (Bài 06) và chia tập/CV (Bài 07), đồng thời áp dụng **quy chuẩn chống rò rỉ của repository**. Không chuyển bảng đã điền khuyết, chuẩn hóa hoặc chọn biến từ EDA toàn bộ dữ liệu sang huấn luyện.

```text
Dữ liệu thô (chỉ đọc)
  → Xác minh đơn vị tiền tệ, đơn vị quan sát; ép kiểu; chuẩn hóa danh mục
  → Loại dòng thiếu price; xử lý lỗi dữ liệu có căn cứ và ghi nhật ký
  ├─ EDA & trực quan: thống kê → Pearson/ANOVA → bảng nhóm/pivot → biểu đồ
  └─ Mô hình: chia train/test 70/30 (random_state=42)
       → Pipeline: chọn biến trên training fold
                   → Nhánh số: imputer → StandardScaler → đa thức nếu có lý do
                   → Nhánh phân loại: imputer → OneHotEncoder
                   → LinearRegression/Ridge
       → CV 4-fold trên train; chọn bậc/alpha
       → Đánh giá cuối trên test: MSE, R², residual/distribution plot
```

### 4.1 Xử lý và diễn giải trong nhánh EDA

- Giữ giá ở đơn vị gốc đã xác minh; không điền giá trị `price` bị thiếu. Trình bày số dòng trước/sau từng bước xử lý.
- Ưu tiên thống kê/kiểm định trên các quan sát có dữ liệu thực ở những biến đang xét; ghi số mẫu hợp lệ `n` của từng phép tính. Nếu điền khuyết để mô tả, ghi rõ cột, cách điền và số giá trị được điền.
- Theo Bài 02, minh họa scaling/binning/dummy trên biến phù hợp. Các cột tạo từ `price` (ví dụ phân khúc giá) chỉ phục vụ mô tả, không dùng làm đầu vào dự đoán `price`.
- Tập biến dự báo được giới hạn rõ: cấm `price_quote_*`, `estimated_revenue_l365d`, biến tính trực tiếp/gián tiếp từ giá, định danh và URL. Nếu có `price_quote_price_per_night`, phải kiểm tra quan hệ với mục tiêu trong kiểm toán; vẫn loại cột báo giá khỏi tập dự báo, không chọn tự động từ toàn bộ cột số.
- Theo Bài 05, báo cáo mean/median/mode, min–Q1–median–Q3–max, phương sai/std, IQR, skewness/kurtosis; CV khi trung bình khác 0 và có ý nghĩa. Dùng ngưỡng 1.5 × IQR để đánh dấu ngoại lệ, không tự động xóa listing có giá cao hợp lệ.
- Pearson: trình bày cả $r$, $p$-value và scatter plot. ANOVA: nêu nhóm, số mẫu, $F$, $p$-value; ngưỡng ý nghĩa $0.05$. Khi $p \ge 0.05$, viết “chưa đủ bằng chứng”, không kết luận “không có liên hệ”. Không diễn giải p-value là xác suất giả thuyết đúng.
- Dùng `groupby`, pivot và heatmap theo Bài 05 tr. 28–30. ANOVA tổng thể có ý nghĩa chưa xác định cặp nào khác biệt; nếu khảo sát cặp nhóm theo tr. 36 thì nêu các cặp đã xét và coi kết quả là thăm dò. Hậu kiểm/hiệu chỉnh nhiều phép thử, nếu bổ sung, phải gắn nhãn ngoài bài học.
- **Ghi chú điều kiện áp dụng bổ sung**: Với nhóm quá ít quan sát hoặc nhiều dòng lặp theo cùng listing/thời gian, chưa khẳng định tính độc lập hay độ tin cậy của kiểm định; ưu tiên mô tả và ghi hạn chế. Không tự chuyển sang kiểm định ngoài bài.
- Kiểm tra số listing cùng `host_id` nếu có cột này; nếu nhiều listing cùng chủ nhà, p-value Pearson/ANOVA thông thường cần được diễn giải như kết quả thăm dò có hạn chế về tính độc lập. Không lấy p nhỏ để thay thế độ lớn chênh lệch hoặc kết luận nhân quả. Kiểm tra phân bố, độ phân tán và số mẫu từng nhóm trước ANOVA; nếu không đủ điều kiện, giữ thống kê mô tả và ghi lý do.

### 4.2 Quy tắc nhánh mô hình và đánh giá

1. **Đơn vị quan sát trước khi chia tập**: Chỉ chia ngẫu nhiên theo dòng khi dữ liệu phù hợp với một quan sát cho mỗi listing. Nếu là listing-date, ưu tiên xác định một snapshot có căn cứ; chưa áp dụng chia ngẫu nhiên khi cùng listing có thể xuất hiện ở cả train/test. Chia theo nhóm/thời gian là thiết kế bổ sung ngoài nội dung đã xác nhận, phải ghi nhãn nếu dùng.
   - Phải kiểm tra tính duy nhất của ID và khả năng nhiều listing cùng chủ nhà trước khi chia tập. Chia theo dòng chỉ đánh giá listing chưa thấy trong cùng đợt dữ liệu, có thể có chủ nhà đã xuất hiện trong train; không khẳng định tổng quát hóa sang chủ nhà mới. Nếu báo cáo mục tiêu chủ nhà mới, phải thêm đánh giá giữ riêng `host_id` ở cả holdout/CV, ghi [MỞ RỘNG NGOÀI BÀI HỌC] và không dùng ID làm feature. Nguồn: [Scikit-learn — CV cho dữ liệu nhóm](https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data).
2. **Chia tập trước khi học từ dữ liệu**: Dùng `train_test_split(X, y, test_size=0.3, random_state=42)` sau làm sạch chung. Imputer/scaler chỉ fit trên train; trong CV chỉ fit trên training fold. `SimpleImputer` là bổ sung kỹ thuật theo repository (mục 1.4).
3. **Chọn biến**: Quy tắc repository cho biến số là $|r| \ge 0.30$ và $p < 0.05$; biến phân loại dùng ANOVA $p < 0.05$. Bài 05 tr. 37 nêu “ngoài -0.3 đến 0.3”; dấu bằng và điều kiện p kết hợp là quy ước repository. Không dùng kết quả kiểm định toàn bộ EDA để chọn biến cho mô hình. Nếu chọn biến theo dữ liệu, phải thực hiện lại trong từng training fold; cách đóng gói bước này là bổ sung kỹ thuật theo repository. Nếu không còn biến phù hợp, báo cáo lý do chưa xây dựng mô hình.
4. **Mô hình trong bài**: Bắt đầu với hồi quy tuyến tính đơn biến, mở rộng đa biến và so sánh Ridge khi đủ biến phù hợp. Đa thức bậc thấp chỉ bổ sung nếu train/CV và phần dư gợi ý cần thiết; không tạo đa thức trên mọi dummy khu vực. Diễn giải hệ số theo đơn vị/thang chuẩn hóa; hệ số khác 0 không tự chứng minh ý nghĩa thống kê.
5. **Pipeline và CV**: Bao gói các phép biến đổi trên X và mô hình trong Pipeline. Dùng CV 4-fold trên train theo repository; nếu cần `GridSearchCV`, ghi “Bổ sung kỹ thuật theo repository” như mục 1.4. Giới hạn lưới alpha, ví dụ `[0.001, 0.01, 0.1, 1, 10, 100, 1000]` từ Bài 07 tr. 28. Chọn bậc/alpha dựa trên CV; không dùng test để chọn cấu hình.
   - Phân nhánh số/phân loại bằng `ColumnTransformer`; encoder học trên training fold và xử lý danh mục chưa thấy. Không truyền chuỗi `room_type` trực tiếp vào StandardScaler hoặc tạo dummy trên toàn bộ dữ liệu trước CV. Dùng cùng split/folds khi so sánh mô hình; công bố danh sách biến sau lựa chọn cuối trên train.
6. **Thước đo và đồ thị**: Báo cáo MSE, $R^2$ trên train/test và trung bình, độ lệch chuẩn qua CV; ghi rõ tập đánh giá. MSE dùng đơn vị bình phương của giá, $R^2$ không có đơn vị. MAE/RMSE chỉ bổ sung khi thực hiện phần tìm hiểu thêm. So sánh train/CV theo bậc để nhận xét underfitting/overfitting. Quan sát phần dư quanh 0, dạng cong, độ phân tán tăng; so sánh phân phối giá thực–dự đoán theo Bài 06. Đồ thị là bằng chứng chẩn đoán, không khẳng định đã kiểm chứng mọi giả định.
7. **Tái lập**: Cố định `random_state=42` ở bước ngẫu nhiên; lưu phiên bản thư viện, cấu hình, số mẫu train/test và kết quả. Notebook 04 phải nêu rõ nội dung Bài 06–07 đã thực hiện hoặc lý do chưa áp dụng.

---

## 5. Quy Chuẩn Slide Thuyết Trình (Slides.pptx)

- **Thời lượng theo mẫu**: 10 phút thuyết trình + 5 phút demo; mẫu có slide Q&A riêng, không nêu thời lượng Q&A.
- **Phạm vi theo mẫu `Slides.pptx`**: Giới thiệu 1 slide, mô tả dữ liệu không quá 2 slide, nội dung không quá 10 slide, kết quả 1–2 slide. Slide giới thiệu nhóm bắt buộc với hệ online. Mẫu cho phép tùy chỉnh thiết kế.
- **Phương án của nhóm**: Dự kiến 14 slide nội dung/bìa theo phân bổ dưới đây; đây không phải giới hạn tổng số slide do giảng viên quy định. Bổ sung slide giới thiệu nhóm khi học online và slide Q&A khi cần:
  - **Slide 1**: Trang tiêu đề (Tên đề tài, Nhóm 10, Thành viên, GVHD ThS. Phạm Thế Sơn).
  - **Slide 2**: Giới thiệu đề tài, mục tiêu và cam kết minh bạch nguồn Inside Airbnb (ý ngắn gọn như template).
  - **Slide 3 - 4 (Tối đa 2 slide)**: Mô tả bộ dữ liệu & Quy trình phân tích (Bảng tóm tắt biến cốt lõi, sơ đồ quy trình).
  - **Slide 5 - 12 (Tối đa 8 slide)**: Nội dung phân tích chính (Mỗi slide tập trung vào 1 câu hỏi nghiên cứu then chốt kèm biểu đồ trực quan chất lượng cao và insight định lượng).
  - **Slide 13**: Kết quả then chốt (3–4 phát hiện có bằng chứng).
  - **Slide 14**: Kết luận & Hướng phát triển (Tóm lược kết quả và hạn chế).
- **Yêu cầu kỹ thuật buổi báo cáo**:
  - Sử dụng 1 laptop duy nhất cho cả nhóm.
  - Mở sẵn file Báo cáo Word, Slide thuyết trình và Notebook/Code đã chạy sẵn kết quả.
  - Giao diện IDE/Notebook để chế độ nền sáng (Light Theme) theo yêu cầu của GV.

---

## 6. Quy Trình Thực Hiện 10 Bước Tuần Tự (Execution Workflow)

**Hạn nộp: 18/10/2026**, theo thông tin người dùng cung cấp ngày 10/10/2026. Giờ chốt, kênh nộp và ngày/giờ thuyết trình chưa xác nhận riêng. Mục tiêu nội bộ là hoàn tất bộ nộp, kiểm tra và tổng duyệt vào 17/10/2026.

**Lịch và phân công chi tiết được theo dõi duy nhất tại [README — Hạn nộp và phân công từng chặng](../../../workspaces/final-project/README.md#ke-hoach-trien-khai)**: từng chặng có mốc ngày, người phụ trách, người kiểm tra chéo, đầu ra và trạng thái. Cả hai bản đặc tả dùng chung bảng này để tránh lệch tiến độ. Trước Bước 1, hoàn tất chuẩn bị tài liệu/lịch và môi trường Python; sau Bước 10, kiểm tra toàn bộ bộ nộp và lưu bằng chứng nộp thành công.

Nhóm thực thi 10 bước dưới đây, bước sau kế thừa kết quả đã được nghiệm thu của bước trước. Tại ngày 10/10/2026, các bước thực nghiệm chưa triển khai; Bước 2 mới có RQ dự kiến:

```text
[Bước 1: Kiểm toán Dataset Bangkok & Xác minh Ngữ nghĩa Price] (CHƯA TRIỂN KHAI)
    └── Kiểm tra số dòng/cột, schema, missing, duplicates; xác minh bản chất price & đơn vị quan trắc
           ↓
[Bước 2: Xác lập Hệ Câu Hỏi Nghiên Cứu (Research Questions)]
    └── Bốn RQ và mô hình bổ trợ theo mục 1.5; điều chỉnh nếu chất lượng dữ liệu không đáp ứng
           ↓
[Bước 3: Thiết Kế & Chốt Phương Án Làm Sạch Dữ Liệu (Data Cleaning)]
    └── Lập bảng giải trình 4 cột (Vấn đề -> Xử lý -> Lý do -> Ảnh hưởng), phân định 2 nhánh EDA vs Model
           ↓
[Bước 4: Thực Thi Code Làm Sạch & Xuất Dataset Processed]
    └── Viết code sạch trong src/wrangling.py và notebook notebooks/01_data_audit_and_cleaning.ipynb
           ↓
[Bước 5: Thực Hiện Phân Tích Thăm Dò (EDA) & Trực Quan Hóa Biến Trung Tâm]
    └── Khảo sát phân bố biến price (Mean, Median, Skew, Kurt, IQR, Hist, Boxplot) trong notebooks/02_...
           ↓
[Bước 6: Phân Tích Mối Liên Hệ Giữa Từng Yếu Tố Với Giá]
    └── Kiểm định ở notebook 02; xuất biểu đồ 300 DPI ở notebook 03
           ↓
[Bước 7: Xây Dựng Mô Hình Hồi Quy Bổ Trợ (Nếu Phù Hợp - Chống Rò Rỉ Data)]
    └── Bài 06–07: Linear/Polynomial/Ridge, Pipeline, CV trên train, MSE/R² và chẩn đoán trong notebooks/04_regression_modeling.ipynb
           ↓
[Bước 8: Tổng Hợp 3–4 Kết Quả Có Bằng Chứng & Viết Giới Thiệu/Kết Luận]
    └── Đảm bảo 100% nhận xét đều có số liệu thực nghiệm làm bằng chứng xác thực
           ↓
[Bước 9: Soạn Thảo Báo Cáo Word (Nhom10_Bao_cao.docx & .pdf) Theo Đúng Template]
    └── Khống chế dung lượng 5 - 10 trang, chuẩn hóa style heading, bảng biểu, tài liệu tham khảo
           ↓
[Bước 10: Thiết Kế Slide Thuyết Trình (Nhom10_Slides.pptx) & Tổng Duyệt Demo]
    └── Hoàn thiện bộ slide ngắn gọn, chuẩn bị kịch bản 10 phút thuyết trình + 5 phút demo; rà soát checklist mục 9
```

---

## 7. Giao Thức Nhiệm Vụ Đầu Tiên: Phiếu Kiểm Toán Dữ Liệu Thực Tế

Bước 1 chưa triển khai. Cần thu thập bản Bangkok vào `workspaces/final-project/data/raw/`, tạo manifest nguồn và SHA-256, phiếu kiểm toán `docs/DATA_AUDIT.md`, script `src/data_audit.py` và số liệu máy đọc tại `reports/audit/`. Các đường dẫn sau đường dẫn dữ liệu được tính từ gốc đồ án. Chỉ nghiệm thu khi chạy lại được kiểm toán và có bằng chứng ngữ nghĩa giá; kiểm toán không đồng nghĩa đã làm sạch/EDA/mô hình. Khi đổi file đầu vào phải thực hiện lại các mục dưới đây trước khi viết kết quả cuối kỳ.

### 7.1 Điều kiện tiên quyết: Xác minh ngữ nghĩa của `price` và Đơn vị quan trắc

Bắt buộc xác định tiền tệ, bản chất giá và đơn vị quan sát trước khi tổng hợp giá. Phần thuế/phí chưa rõ phải ghi là chưa xác nhận, không tự quy thành 0; kết quả chỉ mô tả đúng trường giá quan sát:

1. **Đơn vị tiền tệ chính xác**: Xác minh `price` trong file Bangkok có đơn vị THB hay đơn vị khác bằng tài liệu nguồn; không suy luận chỉ từ tên thành phố hoặc ký hiệu `$`. Kiểm tra dấu nhóm nghìn và dấu thập phân, giữ đơn vị gốc đã xác minh. Nếu có `price_quote_raw`, đối chiếu ký hiệu tiền tệ và lưu bằng chứng trong báo cáo kiểm toán.
2. **Bản chất của giá niêm yết (Pricing Granularity)**:
   - Giá tính theo đêm (`price per night`) hay theo tuần/tháng/cả kỳ lưu trú (`total stay`)?
   - Giá đã bao gồm các phụ phí hay chưa (phí dọn dẹp `cleaning_fee`, phí dịch vụ `service_fee`, phụ thu thêm khách)?
3. **Đơn vị quan sát của từng dòng (Unit of Observation)**:
   - Mỗi dòng đại diện cho một chỗ ở duy nhất (Listing snapshot - ví dụ file `listings.csv` của Inside Airbnb)?
   - Hay mỗi dòng đại diện cho một cặp chỗ ở - ngày lịch biểu (Listing-Date pair - ví dụ file `calendar.csv` của Inside Airbnb)?
   - *Rủi ro nếu không xác định*: Nếu là dữ liệu listing-date (dạng calendar), việc xuất hiện nhiều dòng cùng `id` listing là hoàn toàn bình thường (mỗi dòng ứng với một ngày khác nhau trong năm). Nếu vội vàng xóa trùng lặp theo `id` sẽ làm mất dữ liệu lịch sử giá; nếu gộp tính trung bình mà không phân nhóm theo thời gian sẽ làm sai lệch phân bố giá. Ngược lại, nếu là listing snapshot, các dòng trùng `id` mới là duplicates cần xử lý.

### 7.2 Mười một đầu mục kiểm toán chi tiết

1. **Kích thước thực tế**: Tổng số dòng (quan trắc) và tổng số cột (thuộc tính).
2. **Danh mục cột & Ý nghĩa**: Liệt kê đầy đủ tên từng cột và giải thích ý nghĩa nghiệp vụ (nếu không rõ ghi *"Chưa đủ thông tin để xác định"*).
3. **Kiểu dữ liệu (dtypes)**: Chi tiết từng cột (`int64`, `float64`, `object`, `datetime`, `bool`).
4. **Thống kê giá trị khuyết (Missing Values)**: Số lượng và tỷ lệ % khuyết trên từng cột.
5. **Dòng trùng lặp (Duplicates)**: Số dòng trùng hoàn toàn và số dòng trùng định danh (ID nếu có), phân tích dựa trên đơn vị quan sát đã xác định ở 7.1.
6. **Các vấn đề chất lượng dữ liệu**: Giá trị âm, giá trị bằng 0, định dạng chuỗi tiền tệ, phân loại không đồng nhất.
7. **Phạm vi & Phân bố sơ bộ của biến mục tiêu `price`**: Min, Max, Mean, Median, Độ lệch chuẩn, Tứ phân vị $Q_1, Q_3$, đánh giá sơ bộ độ lệch (Skewness).
8. **Danh sách các biến tiềm năng để phân tích giá**: Phân loại rõ nhóm định lượng (numerical) và nhóm định tính (categorical) thực sự có ý nghĩa phân tích.
9. **Bốn câu hỏi phân tích và một phần mô hình bổ trợ**: Bám bảng mục 1.5 và chất lượng biến thực tế; không mở rộng mặc định.
10. **Bảng ma trận phân tích cho từng câu hỏi**:
    - Câu hỏi nghiên cứu (RQ).
    - Các biến sử dụng.
    - Phương pháp phân tích (Thống kê mô tả, Pearson correlation, One-way ANOVA), kèm bài học và trang PDF; kỹ thuật bổ sung phải có nhãn theo mục 1.4.
    - Dạng biểu đồ trực quan hóa (Matplotlib OO API).
    - Giả thuyết / Kết quả cần kiểm nghiệm thực tế.
11. **Báo cáo thu hẹp phạm vi**: Chỉ rõ RQ không thể thực hiện do thiếu biến, thiếu chất lượng hoặc vượt nội dung bài học. Khoảng cách địa lý và NLP không thuộc kế hoạch mặc định ngay cả khi có tọa độ/văn bản; tiện ích chỉ phân tích như biến phân loại có sẵn và đã xác minh ý nghĩa.

---

## 8. Kiến Trúc Lưu Trữ Sản Phẩm Dự Án (Dự Kiến Triển Khai)

Cấu trúc dự kiến tại `workspaces/final-project/` được liệt kê dưới đây. Hiện có README, đặc tả, hai template và bản khung `reports/Nhom10_Bao_cao.docx` cùng PDF xem trước `reports/Nhom10_Bao_cao_Khung.pdf` và hướng dẫn `reports/README.md`. Bản khung có Giới thiệu hai đoạn và các chỗ chờ dữ liệu/kết quả; chưa phải báo cáo hoàn chỉnh. Dữ liệu, mã nguồn, cấu hình môi trường, test, notebook và kết quả thực nghiệm trong cây đều chưa được tạo:

```text
workspaces/final-project/
├── README.md                           # Thông tin nhóm 10, tên đề tài và nhật ký tiến độ
├── docs/                               # Tài liệu hướng dẫn & tài liệu thiết kế
│   ├── SPECIFICATION.md                # Bản sao đặc tả thiết kế làm việc nội bộ
│   ├── Template_IE313.docx             # Template báo cáo Word gốc
│   ├── Slides.pptx                     # Template slide PowerPoint gốc
│   ├── DATA_AUDIT.md                  # Dự kiến Bước 1: phiếu kiểm toán
│   └── sources/                      # Dự kiến Bước 1: từ điển nguồn
├── data/                               # Dữ liệu phân tích
│   ├── raw/                            # Chứa dữ liệu gốc (BẤT BIẾN - READ ONLY)
│   ├── processed/                      # Dữ liệu sạch: chưa thực hiện
│   └── source_manifest.json            # URL, phiên bản, SHA-256, đơn vị và giới hạn
├── notebooks/                          # Jupyter Notebooks thực nghiệm (chuẩn hóa tên file)
│   ├── 01_data_audit_and_cleaning.ipynb # Kiểm toán và làm sạch dữ liệu
│   ├── 02_eda_and_statistical_tests.ipynb # EDA, kiểm định Pearson và ANOVA
│   ├── 03_visualization_figures.ipynb  # Sinh ảnh biểu đồ chất lượng cao 300 DPI
│   └── 04_regression_modeling.ipynb    # Mô hình hồi quy bổ trợ và chẩn đoán
├── src/                                # Mã nguồn tái sử dụng (chuẩn hóa tên file)
│   ├── __init__.py
│   ├── data_audit.py                   # Dự kiến Bước 1: kiểm toán chỉ đọc
│   ├── data_loader.py                  # Module nạp và kiểm tra dữ liệu
│   ├── wrangling.py                    # Module làm sạch và chuẩn hóa
│   ├── eda_stats.py                    # Module tính toán thống kê và kiểm định
│   └── visualization.py                # Module vẽ biểu đồ chuẩn Matplotlib OO API
├── requirements.txt                    # Dự kiến bước chuẩn bị: thư viện
├── requirements-dev.txt                # Pytest và Ruff
├── tests/test_data_audit.py             # Test đọc giá, checksum và báo giá thiếu
└── reports/                            # Kiểm toán và sản phẩm cuối kỳ dự kiến
    ├── audit/                          # Dự kiến: JSON + schema/missing thực tế
    ├── qa_audit_report.md               # Dự kiến: kiểm tra trước khi nộp
    ├── figures/                        # Thư viện ảnh 300 DPI (chèn vào Word & Slide)
    ├── Nhom10_Bao_cao.docx             # Đã có bản khung; chờ kết quả ở Bước 9
    ├── Nhom10_Bao_cao_Khung.pdf       # Đã có PDF xem trước bản khung
    ├── Nhom10_Bao_cao.pdf              # Báo cáo PDF xuất từ Word
    ├── Nhom10_Slides.pptx              # Slide thuyết trình hoàn thiện
    ├── Nhom10_Dataset.docx             # Link dataset > 50 MB; cần xác minh mốc trong template
    └── Nhom10_Video.docx               # Link video > 60 MB (nếu học trực tuyến)
```

---

## 9. Kiểm Tra Bám Sát Bài Học Trước Khi Nghiệm Thu

Trạng thái ngày 10/10/2026: repo có tài liệu thiết kế, template và bản khung báo cáo Word; chưa có dữ liệu Airbnb, manifest, script/test kiểm toán, notebook hoặc kết quả thực nghiệm. Checklist chỉ đánh dấu nội dung có minh chứng; lịch và phân công nằm trong README:

- [x] Hai bản đặc tả đồng bộ, README thống nhất tên đề tài, bốn RQ dự kiến và trạng thái chưa kiểm toán.
- [x] Đã ghi hạn nộp 18/10/2026, lịch nội bộ, người phụ trách và người kiểm tra chéo từng chặng.
- [ ] Đã xác nhận giờ/kênh nộp, lịch thuyết trình và các yêu cầu nộp còn chưa rõ.
- [ ] Đã thiết lập môi trường tái lập cho hai thành viên.
- [ ] Đã có nguồn Bangkok, phiên bản, checksum và phiếu kiểm toán có thể chạy lại.
- [ ] Đã xác minh schema, đơn vị quan sát, tiền tệ và ý nghĩa `price` bằng dữ liệu thực.

- [ ] Mỗi phương pháp có bài học/trang PDF hoặc nhãn “Bổ sung kỹ thuật theo repository” / “Mở rộng ngoài bài học” với nguồn và lý do rõ ràng.
- [ ] Notebook 01 thể hiện Bài 01–02: nhập/xuất, kiểm tra kiểu dữ liệu, xử lý khuyết/đơn vị; giải trình scaling/binning/dummy đã dùng hoặc chưa phù hợp.
- [ ] Notebook 02 thể hiện Bài 05: thống kê mô tả, IQR, Pearson r–p, ANOVA F–p, groupby/pivot khi có biến phù hợp; không dùng ngôn ngữ nhân quả.
- [ ] Notebook 03 thể hiện Bài 03–04: mỗi biểu đồ gắn RQ, quy trình 5 bước, nhãn/đơn vị/chú giải, OO API và ảnh 300 DPI; không thêm biểu đồ chỉ để đủ số lượng.
- [ ] Notebook 04 thể hiện Bài 06–07: hồi quy tuyến tính, cân nhắc đa thức/Ridge, Pipeline, train/test, CV, MSE/R², nhận xét độ khớp và residual/distribution plot; nếu không thực hiện phải có lý do từ dữ liệu.
- [ ] Không đưa biến tạo từ price hay kết quả chọn biến toàn bộ EDA vào mô hình; không dùng test để tinh chỉnh.
- [ ] Báo cáo và slide ghi rõ phần tìm hiểu thêm/mở rộng; số liệu và hình phải truy được về notebook đã chạy.
- [x] Đã tạo Word bản khung từ template, điền thông tin nhóm và Giới thiệu hai đoạn; các phần chưa xác nhận được đánh dấu chờ bổ sung.
- [ ] Bộ báo cáo/slide cuối kỳ phân biệt đúng quy định của giảng viên với lựa chọn của nhóm.

**Ghi nhận rà soát ngày 04/10/2026**: Đã đối chiếu đặc tả với 8 PDF và hai template cục bộ; thu hẹp phương pháp mặc định về nội dung môn học, bổ sung ánh xạ nguồn và phân loại phần tìm hiểu thêm. Đây là rà soát tài liệu thiết kế, chưa xác nhận schema Airbnb, kết quả thống kê hay chất lượng mô hình.

**Ghi nhận thiết kế ngày 07/10/2026**: Chuyển sang Bangkok và bổ sung thiết kế xử lý rủi ro báo giá khác kỳ lưu trú, dữ liệu cùng chủ nhà, cột làm lộ mục tiêu, Pipeline số/phân loại và giới hạn thuế/phí. Ghi nhận cũ về việc đã kiểm toán và có script/test được đính chính ở lần rà soát dưới đây.

**Đính chính ngày 10/10/2026**: Đối chiếu filesystem cho thấy chưa có dữ liệu Airbnb, nguồn/manifest, phiếu kiểm toán hoặc script/test trong repo. Các con số và ngữ nghĩa giá từng ghi là kết quả được chuyển về trạng thái chưa xác minh. Đồng bộ README và hai bản đặc tả, bổ sung hạn nộp 18/10/2026 và lịch phân công từng chặng; chưa có kết quả thực nghiệm. Tiếp đó đã tạo bản khung báo cáo Word từ template, gồm Giới thiệu hai đoạn và các mục chờ dữ liệu/kết quả; chưa nghiệm thu báo cáo cuối kỳ.

---

*Bản đặc tả Bangkok cập nhật ngày 10/10/2026, kế thừa cấu trúc thiết kế từ ngày 03/10/2026.*
