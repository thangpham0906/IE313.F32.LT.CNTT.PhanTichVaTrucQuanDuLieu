# ĐỒ ÁN MÔN HỌC IE313: PHÂN TÍCH VÀ TRỰC QUAN DỮ LIỆU

- **Trường**: Đại học Công nghệ Thông tin - ĐHQG-HCM (UIT)
- **Lớp**: `IE313.F32.LT.CNTT` (Hệ Liên thông Đại học - Ngành CNTT)
- **Giảng viên phụ trách**: ThS. Phạm Thế Sơn
- **Nhóm thực hiện**: **Nhóm 10** (2 thành viên)

## Thành viên nhóm

| STT | MSSV | Họ và Tên | Vai trò chính |
| :---: | :---: | :--- | :--- |
| 1 | 25410304 | Phạm Quốc Thắng | Trưởng nhóm, Phân tích & Trực quan hóa, Tổng hợp báo cáo & Slide |
| 2 | 25410313 | Lê Minh Thiện | Tiền xử lý dữ liệu, Kiểm định thống kê, Mô hình bổ trợ & Đánh giá |

---

## Tên Đề Tài

> **PHÂN TÍCH VÀ TRỰC QUAN HÓA GIÁ THUÊ AIRBNB TẠI BANGKOK VÀ CÁC YẾU TỐ LIÊN QUAN**

- **Bản đặc tả thiết kế chính thức (Official Spec)**: [docs/superpowers/specs/2026-10-07-airbnb-bangkok-analysis-design.md](../../docs/superpowers/specs/2026-10-07-airbnb-bangkok-analysis-design.md)
- **Bản đặc tả làm việc nội bộ (Working Spec)**: [docs/SPECIFICATION.md](docs/SPECIFICATION.md)
- **Template báo cáo**: [docs/Template_IE313.docx](docs/Template_IE313.docx)
- **Template slide**: [docs/Slides.pptx](docs/Slides.pptx)

## Phạm Vi Theo Bài Học

Đồ án ưu tiên phân tích, trực quan hóa và diễn giải dữ liệu; phần hồi quy vận dụng Bài 06–07. Tỷ lệ công sức dự kiến 80% phân tích (kiểm toán, làm sạch, EDA, trực quan) / 20% mô hình trong đặc tả là lựa chọn của nhóm, không phải tỷ trọng chấm điểm.

| Bài học trong [slide-study](../../slide-study/) | Áp dụng dự kiến | Notebook |
| :--- | :--- | :--- |
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

## Trạng Thái Dự Án Hiện Tại

- **Hiện trạng thực tế**: Dự án hiện đang ở giai đoạn **Lập kế hoạch & Đặc tả thiết kế (Planning & Specification)**. Nhóm **chưa triển khai mã nguồn hay nạp dữ liệu thực tế** vào repository.
- **Đã hoàn thành**:
  - Chốt đề tài: *Phân tích và trực quan hóa giá thuê Airbnb tại Bangkok và các yếu tố liên quan*.
  - Lập tài liệu đặc tả thiết kế kỹ thuật chi tiết ([SPECIFICATION.md](docs/SPECIFICATION.md)), phân công vai trò 2 thành viên và xác lập hệ thống 10 bước triển khai.
  - Phân định rõ phạm vi nội dung môn học (8 bài giảng PDF) và nguyên tắc chống rò rỉ dữ liệu / không suy diễn nhân quả.
- **Kế hoạch tiếp theo (Bắt đầu từ Bước 1)**:
  - Thu thập bộ dữ liệu Inside Airbnb Bangkok và đưa vào `data/raw/`.
  - Thực hiện kiểm toán dữ liệu thực tế (schema 90 cột, missing, duplicates, xác minh đơn vị tiền tệ THB/đêm).
  - Soạn thảo phiếu kiểm toán `docs/DATA_AUDIT.md` và hiện thực hóa script kiểm toán `src/data_audit.py`.

---

## Cấu Trúc Thư Mục (Dự Kiến Triển Khai)

Toàn bộ cây thư mục dưới đây là **cấu trúc chuẩn dự kiến sẽ tạo và hoàn thiện dần** qua 10 bước thực hiện:

```text
workspaces/final-project/
├── README.md                           # Thông tin nhóm 10, tên đề tài và nhật ký tiến độ
├── docs/                               # Tài liệu hướng dẫn & tài liệu thiết kế
│   ├── SPECIFICATION.md                # Bản sao đặc tả thiết kế làm việc nội bộ
│   ├── Template_IE313.docx             # Template báo cáo Word gốc của GV
│   ├── Slides.pptx                     # Template slide PowerPoint gốc của GV
│   ├── DATA_AUDIT.md                   # (Dự kiến Bước 1) Phiếu kiểm toán dữ liệu thực tế
│   └── sources/                        # (Dự kiến Bước 1) Bản từ điển dữ liệu nguồn
├── data/                               # Dữ liệu phân tích
│   ├── raw/                            # (Dự kiến Bước 1) Chứa dữ liệu gốc (BẤT BIẾN - READ ONLY)
│   ├── processed/                      # (Dự kiến Bước 4) Dữ liệu sạch xuất từ wrangling
│   └── source_manifest.json            # (Dự kiến Bước 1) Manifest nguồn, SHA-256
├── notebooks/                          # Jupyter Notebooks thực nghiệm từng chặng
│   ├── 01_data_audit_and_cleaning.ipynb # (Dự kiến Bước 4) Kiểm toán và làm sạch dữ liệu
│   ├── 02_eda_and_statistical_tests.ipynb # (Dự kiến Bước 5-6) EDA, kiểm định Pearson và ANOVA
│   ├── 03_visualization_figures.ipynb  # (Dự kiến Bước 6) Xuất ảnh biểu đồ chuẩn OO API 300 DPI
│   └── 04_regression_modeling.ipynb    # (Dự kiến Bước 7) Mô hình hồi quy bổ trợ và chẩn đoán
├── src/                                # Mã nguồn module hóa tái sử dụng
│   ├── __init__.py
│   ├── data_audit.py                   # (Dự kiến Bước 1) Module kiểm toán dữ liệu thô
│   ├── data_loader.py                  # (Dự kiến Bước 1) Module nạp và kiểm tra dữ liệu
│   ├── wrangling.py                    # (Dự kiến Bước 4) Module làm sạch và chuẩn hóa
│   ├── eda_stats.py                    # (Dự kiến Bước 6) Module tính thống kê và kiểm định
│   └── visualization.py                # (Dự kiến Bước 6) Module vẽ biểu đồ chuẩn Matplotlib OO API
├── requirements.txt                    # Danh sách thư viện phụ thuộc
├── requirements-dev.txt                # Thư viện dev (pytest, ruff)
├── tests/test_data_audit.py            # Unit tests kiểm định dữ liệu
└── reports/                            # Sản phẩm báo cáo và nghiệm thu
    ├── audit/                          # Báo cáo và bảng kiểm toán dữ liệu
    ├── figures/                        # Thư viện ảnh 300 DPI nhúng vào Word & Slide
    ├── Nhom10_Bao_cao.docx             # (Dự kiến Bước 9) Báo cáo Word hoàn chỉnh (5 - 10 trang)
    ├── Nhom10_Bao_cao.pdf              # (Dự kiến Bước 9) Báo cáo PDF xuất từ Word
    ├── Nhom10_Slides.pptx              # (Dự kiến Bước 10) Slide thuyết trình hoàn thiện
    ├── Nhom10_Dataset.docx             # (Dự kiến Bước 9) Link Drive dataset nếu > 50 MB
    └── Nhom10_Video.docx               # (Dự kiến Bước 9) Link Drive video nếu học trực tuyến
```
