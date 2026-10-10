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
- **Báo cáo Word bản khung**: [reports/Nhom10_Bao_cao.docx](reports/Nhom10_Bao_cao.docx) — đã có bìa, Giới thiệu hai đoạn và khung nội dung; chưa có kết quả thực nghiệm.
- **PDF xem trước bản khung**: [reports/Nhom10_Bao_cao_Khung.pdf](reports/Nhom10_Bao_cao_Khung.pdf) — chưa phải bản PDF nộp cuối kỳ.
- **Hướng dẫn hoàn thiện bản khung**: [reports/README.md](reports/README.md)
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

**Cập nhật ngày 10/10/2026**, căn cứ các tệp hiện có trong repository:

- **Đã có**: README, hai bản đặc tả đồng bộ, template báo cáo Word và slide PowerPoint, bản khung báo cáo `reports/Nhom10_Bao_cao.docx`; đề tài Bangkok, bốn câu hỏi nghiên cứu dự kiến và nguyên tắc triển khai.
- **Chưa có trong repo**: dữ liệu Airbnb, manifest/checksum, phiếu kiểm toán, mã nguồn, thư viện phụ thuộc, test, notebook và kết quả phân tích. Dữ liệu Automobile ở thư mục khác là bài tập, không phải dữ liệu đồ án.
- **Chưa xác minh**: phiên bản dữ liệu 29/06/2026, schema, số dòng/cột, số giá hợp lệ, đơn vị và ý nghĩa của `price`. Không dùng các con số trong bản đặc tả cũ như kết quả đã kiểm toán.
- **Việc tiếp theo**: thiết lập môi trường, thu thập dữ liệu gốc, lưu nguồn và SHA-256, rồi chạy kiểm toán trước khi nghiệm thu Bước 1.

Bốn câu hỏi dự kiến: **RQ1** phân bố giá; **RQ2** khác biệt theo loại phòng; **RQ3** liên hệ giữa quy mô chỗ ở và giá; **RQ4** khác biệt theo khu vực. Chốt khả năng thực hiện sau kiểm toán. Hồi quy là phần bổ trợ theo Bài 06–07.

<a id="ke-hoach-trien-khai"></a>

## Hạn Nộp Và Phân Công Từng Chặng

- **Hạn nộp: 18/10/2026**, theo thông tin người dùng cung cấp ngày 10/10/2026.
- **Giờ chốt nộp và kênh nộp**: chưa xác nhận; Thắng kiểm tra thông báo chính thức của giảng viên trước 11/10. Không mặc định hạn chót là 23:59.
- **Ngày/giờ thuyết trình**: chưa xác nhận riêng; Thắng cập nhật khi có thông báo.
- **Mục tiêu nội bộ**: hoàn tất bộ nộp và tổng duyệt vào 17/10/2026; dành 18/10 để kiểm tra và nộp trước giờ chốt.
- Các mốc bên dưới là **kế hoạch nội bộ**, không phải ngày hoàn thành thực tế hay lịch giảng viên giao. Ngày tháng theo giờ Việt Nam (UTC+7).

Trong bảng: **Thắng = Phạm Quốc Thắng**, **Thiện = Lê Minh Thiện**. Người phụ trách tạo đầu ra; người kiểm tra chéo đối chiếu đầu ra với tiêu chí trước khi chuyển trạng thái sang “Hoàn thành”.

| Chặng | Mốc nội bộ | Phụ trách | Kiểm tra chéo | Đầu ra và điều kiện hoàn thành | Trạng thái 10/10 |
|---|---|---|---|---|---|
| Chuẩn bị: tài liệu và lịch | 10/10/2026 | Thắng | Thiện | README và hai đặc tả thống nhất; có hạn nộp, phân công và tiêu chí bàn giao | Đã cập nhật tài liệu; chờ nhóm kiểm tra |
| Chuẩn bị: môi trường | 10/10/2026 | Thiện | Thắng | `requirements.txt`, `requirements-dev.txt`, hướng dẫn chạy; hai thành viên cài và chạy được môi trường | Chưa triển khai |
| Bước 1: thu thập và kiểm toán | 11/10/2026 | Thiện | Thắng | `data/raw/`, `data/source_manifest.json`, `docs/DATA_AUDIT.md`, `src/data_audit.py`, `reports/audit/`, test kiểm toán; xác minh schema, giá, đơn vị quan sát và checksum; chạy lại được | Chưa triển khai |
| Bước 2: chốt RQ | 11/10/2026, sau Bước 1 | Thắng | Thiện | Ma trận RQ–biến–phương pháp–biểu đồ–giới hạn trong `docs/DATA_AUDIT.md`; chỉ giữ RQ có dữ liệu đáp ứng | Có bản dự kiến; chưa nghiệm thu |
| Bước 3: phương án làm sạch | 12/10/2026 | Thiện | Thắng | Bảng Vấn đề–Xử lý–Lý do–Ảnh hưởng trong `docs/DATA_AUDIT.md`; tách EDA/mô hình, không điền giá thiếu | Chưa triển khai |
| Bước 4: thực thi làm sạch | 12/10/2026, sau Bước 3 | Thiện | Thắng | `src/wrangling.py`, notebook 01, `data/processed/`; ghi số dòng trước/sau, kiểm tra dữ liệu và giữ nguyên file thô | Chưa triển khai |
| Bước 5: EDA biến giá | 13/10/2026 | Thắng | Thiện | Notebook 02 có thống kê mô tả, phân bố và ngoại lệ; nhận xét truy được về kết quả chạy | Chưa triển khai |
| Bước 6: yếu tố liên quan và hình | 14/10/2026 | Thắng (hình/diễn giải), Thiện (kiểm định) | Kiểm tra chéo phần của nhau | Notebook 02–03, bảng r–p/F–p khi đủ điều kiện, số mẫu hợp lệ và ảnh 300 DPI trả lời RQ | Chưa triển khai |
| Bước 7: hồi quy bổ trợ | 15/10/2026 | Thiện | Thắng | Notebook 04: Pipeline, train/test, CV, MSE/R² và chẩn đoán; hoặc giải trình bằng dữ liệu vì sao chưa phù hợp | Chưa triển khai |
| Bước 8: tổng hợp kết quả | 16/10/2026 | Thắng | Thiện | 3–4 phát hiện kèm bảng/hình, giới hạn và nguồn kết quả; đưa vào bản thảo báo cáo | Chưa triển khai |
| Bước 9: báo cáo và hồ sơ | 16/10/2026, sau Bước 8 | Thắng | Thiện | Word/PDF đúng template, phần thân 5–10 trang, phân công chi tiết và nguồn dữ liệu; chuẩn bị link dataset/video nếu thuộc diện yêu cầu | Đã có Word bản khung ngày 10/10; chờ dữ liệu, kết quả và kiểm tra cuối |
| Bước 10: slide và tổng duyệt | 17/10/2026 | Thắng (slide), cả hai (demo) | Thiện kiểm tra số liệu và thời lượng | Slide, kịch bản 10 phút + demo 5 phút, video nếu học online; hai thành viên trình bày được phần mình | Chưa triển khai |
| Kiểm tra toàn bộ bộ nộp | 17/10/2026 | Thiện | Thắng | `reports/qa_audit_report.md`: notebook chạy từ đầu đến cuối, test/lint đạt, checksum nguyên vẹn, số liệu Word/PDF/slide khớp; mở thử toàn bộ file | Chưa triển khai |
| Nộp bài | 18/10/2026, trước giờ chốt được xác nhận | Thắng | Thiện | Đúng tên `Nhom10_...`, đủ sản phẩm theo template, link tải hoạt động nếu dùng; lưu bằng chứng nộp thành công | Chưa triển khai |

**Quy tắc cập nhật**: README là nơi duy nhất theo dõi lịch và phân công; hai đặc tả dẫn về bảng này. Khi bàn giao, ghi đường dẫn đầu ra, ngày hoàn thành thực tế và người kiểm tra vào ô trạng thái. Chưa có đầu ra hoặc chưa kiểm tra thì không đánh dấu hoàn thành. Nếu trễ mốc, ghi nguyên nhân và cập nhật các chặng phụ thuộc; ưu tiên bốn RQ và bộ nộp, chưa mở rộng dashboard/NLP/bản đồ.

**Các việc Thắng cần xác nhận từ thông báo giảng viên**: giờ/kênh nộp, lịch thuyết trình, yêu cầu video theo hình thức học, và ngưỡng dataset 50 MB/60 MB đang mâu thuẫn trong template.

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
    ├── Nhom10_Bao_cao.docx             # Đã có bản khung; hoàn thiện ở Bước 9
    ├── Nhom10_Bao_cao_Khung.pdf       # Đã có PDF xem trước bản khung
    ├── Nhom10_Bao_cao.pdf              # (Dự kiến Bước 9) Báo cáo PDF xuất từ Word
    ├── Nhom10_Slides.pptx              # (Dự kiến Bước 10) Slide thuyết trình hoàn thiện
    ├── Nhom10_Dataset.docx             # (Dự kiến Bước 9) Link Drive dataset nếu > 50 MB
    └── Nhom10_Video.docx               # (Dự kiến Bước 9) Link Drive video nếu học trực tuyến
```
