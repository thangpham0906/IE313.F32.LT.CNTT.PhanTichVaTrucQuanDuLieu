# ĐỒ ÁN MÔN HỌC IE313: PHÂN TÍCH VÀ TRỰC QUAN DỮ LIỆU

- **Trường**: Đại học Công nghệ Thông tin - ĐHQG-HCM (UIT)
- **Lớp**: `IE313.F32.LT.CNTT` (Hệ Liên thông Đại học - Ngành CNTT)
- **Giảng viên phụ trách**: ThS. Phạm Thế Sơn
- **Nhóm thực hiện**: **Nhóm 10**

## Thành viên nhóm

| STT | MSSV | Họ và Tên | Vai trò chính |
| :---: | :---: | :--- | :--- |
| 1 | 25410304 | Phạm Quốc Thắng | Trưởng nhóm, Phân tích & Trực quan hóa |
| 2 | 25410313 | Lê Minh Thiện | Tiền xử lý dữ liệu & Kiểm định thống kê |
| 3 | 25410324 | Trần Bình Trọng | Mô hình hóa bổ trợ & Soạn thảo báo cáo |

---

## Tên Đề Tài

> **PHÂN TÍCH CÁC YẾU TỐ ẢNH HƯỞNG ĐẾN GIÁ THUÊ AIRBNB TẠI ĐÀ LẠT, LÂM ĐỒNG, VIỆT NAM**

- **Bản đặc tả thiết kế chính thức (Official Spec)**: [docs/superpowers/specs/2026-10-03-airbnb-dalat-analysis-design.md](../../docs/superpowers/specs/2026-10-03-airbnb-dalat-analysis-design.md)
- **Bản đặc tả làm việc nội bộ (Working Spec)**: [docs/SPECIFICATION.md](docs/SPECIFICATION.md)
- **Template báo cáo**: [docs/Template_IE313.docx](docs/Template_IE313.docx)
- **Template slide**: [docs/Slides.pptx](docs/Slides.pptx)

## Phạm Vi Theo Bài Học

Đồ án ưu tiên phân tích, trực quan hóa và diễn giải dữ liệu; phần hồi quy vận dụng Bài 06–07. Tỷ lệ công sức dự kiến 85% phân tích / 15% mô hình trong đặc tả là lựa chọn của nhóm, không phải tỷ trọng chấm điểm.

| Bài học trong [slide-study](../../slide-study/) | Áp dụng dự kiến | Notebook |
|---|---|---|
| TH 01, Bài 01 | Python/Pandas, nhập/xuất, kiểm tra schema và mô tả biến | `01_data_audit_and_cleaning.ipynb` |
| Bài 02 | Xử lý khuyết, ép kiểu/đơn vị, scaling, binning, dummy khi phù hợp | `01_data_audit_and_cleaning.ipynb` |
| Bài 05 | Thống kê mô tả, IQR, Pearson r–p, ANOVA F–p, groupby/pivot/heatmap | `02_eda_and_statistical_tests.ipynb` |
| Bài 03–04 | Quy trình 5 bước; histogram, boxplot, bar, scatter và biểu đồ phù hợp RQ | `03_visualization_figures.ipynb` |
| Bài 06 | Hồi quy tuyến tính đơn/đa biến, đa thức, Pipeline; regression/residual/distribution plot | `04_regression_modeling.ipynb` |
| Bài 07 | Train/test, CV, overfitting/underfitting, Ridge/chọn alpha; MSE và R² | `04_regression_modeling.ipynb` |

Phạm vi và nguồn theo **trang PDF** nằm ở mục 1.3–1.4 của [đặc tả](docs/SPECIFICATION.md). Không bắt buộc áp dụng mọi kỹ thuật; khi dữ liệu không đủ điều kiện phải ghi lý do.

- **Cốt lõi đánh giá mô hình**: MSE, R²; MAE/RMSE là phần **bài giảng giao tìm hiểu thêm** tại Bài 07 tr. 9–10. KNNImputer cũng thuộc phần tìm hiểu thêm của Bài 02 tr. 10.
- **Có trong bài nhưng chỉ dùng khi phù hợp**: Waffle, word cloud, dashboard (Bài 04); không bắt buộc xây ứng dụng web.
- **Quy chuẩn repository**: OO API, font tiếng Việt, PNG 300 DPI, dữ liệu thô bất biến, seed 42 và CV 4-fold. `SimpleImputer`/`GridSearchCV`, nếu dùng, ghi **“Bổ sung kỹ thuật theo repository”**; chưa xác nhận các API này trong PDF.
- **Không dùng mặc định**: Spearman, Decision Tree/Random Forest, SHAP, biến đổi log giá, tính khoảng cách địa lý, NLP/phân tích cảm xúc. Nếu cần bổ sung, ghi **[MỞ RỘNG NGOÀI BÀI HỌC]** ngay tại phương pháp/code/kết quả, kèm nguồn, lý do và giới hạn theo mẫu ở mục 1.4.

## Trạng Thái Và Nguyên Tắc Thực Hiện

- **04/10/2026**: Đã rà soát và đồng bộ hai bản đặc tả với 8 bài giảng PDF, template Word và PowerPoint. Cấu trúc thư mục phía dưới là kế hoạch triển khai; chưa có kết quả phân tích Airbnb được xác nhận trong lần rà soát này.
- **Bước tiếp theo**: Tiếp nhận dataset, xác minh tiền tệ, cách tính `price`, đơn vị quan sát (listing hay listing-date), rồi lập phiếu kiểm toán theo mục 7 của đặc tả. Các cột và RQ dự kiến chưa phải schema thực tế.
- **Phân tích**: Báo cáo cả trị thống kê và p-value, không diễn giải tương quan thành nhân quả. Phân tích giá gốc; không tự xóa giá cao hợp lệ hay điền giá thiếu.
- **Mô hình**: Chia train/test trước khi học cách điền khuyết/chuẩn hóa/chọn biến; CV và chọn cấu hình chỉ trên train. Giải trình nếu dữ liệu không cho phép thực hiện Bài 06–07.
- **Nộp bài**: Phần thân báo cáo 5–10 trang. Phương án 14 slide là lựa chọn nhóm; mẫu yêu cầu thêm giới thiệu nhóm với hệ online. Dataset có hai mốc 50/60 MB cần xác minh trước khi nộp (tạm theo mốc 50 MB); video dùng mốc 60 MB. Chi tiết ở mục 3 và 5 của đặc tả.

---

## Cấu Trúc Thư Mục (Dự Kiến Triển Khai)

```text
workspaces/final-project/
├── README.md                           # File này
├── docs/                               # Tài liệu hướng dẫn & Đặc tả thiết kế
│   ├── SPECIFICATION.md                # Bản sao đặc tả thiết kế làm việc nội bộ
│   ├── Template_IE313.docx             # Mẫu báo cáo Word chính thức
│   ├── Slides.pptx                     # Mẫu slide thuyết trình chính thức
│   └── extracted_template.txt          # Nội dung trích xuất từ template
├── data/
│   ├── raw/                            # Dữ liệu thô ban đầu (BẤT BIẾN - READ ONLY)
│   └── processed/                      # Dữ liệu đã làm sạch qua bước Wrangling
├── notebooks/                          # Jupyter Notebooks thực nghiệm từng bước
│   ├── 01_data_audit_and_cleaning.ipynb # Kiểm toán và làm sạch dữ liệu
│   ├── 02_eda_and_statistical_tests.ipynb # EDA, kiểm định Pearson và ANOVA
│   ├── 03_visualization_figures.ipynb  # Sinh ảnh biểu đồ chất lượng cao 300 DPI
│   └── 04_regression_modeling.ipynb    # Mô hình hồi quy bổ trợ và chẩn đoán
├── src/                                # Mã nguồn Python tái sử dụng (clean code)
│   ├── __init__.py
│   ├── data_loader.py                  # Module nạp và kiểm tra dữ liệu
│   ├── wrangling.py                    # Module làm sạch và chuẩn hóa
│   ├── eda_stats.py                    # Module tính toán thống kê và kiểm định
│   └── visualization.py                # Module vẽ biểu đồ chuẩn Matplotlib OO API
└── reports/                            # Sản phẩm nghiệm thu cuối kỳ
    ├── figures/                        # Ảnh biểu đồ xuất bản 300 DPI
    ├── Nhom10_Bao_cao.docx             # Báo cáo Word hoàn chỉnh (5 - 10 trang)
    ├── Nhom10_Bao_cao.pdf              # Báo cáo PDF xuất từ Word
    ├── Nhom10_Slides.pptx              # Slide thuyết trình hoàn thiện
    ├── Nhom10_Dataset.docx             # Link dataset > 50 MB; cần xác minh mốc trong template
    └── Nhom10_Video.docx               # Link video > 60 MB (nếu học trực tuyến)
```
