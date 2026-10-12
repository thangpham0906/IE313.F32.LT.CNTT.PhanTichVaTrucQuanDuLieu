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
- **Báo cáo đã điền kết quả**: [Word](reports/Nhom10_Bao_cao.docx) và [PDF](reports/Nhom10_Bao_cao.pdf) — 8 trang phần thân; chờ nhóm đọc/kiểm tra chéo.
- **Slide**: [PowerPoint](reports/Nhom10_Slides.pptx), [PDF xem trước](reports/Nhom10_Slides.pdf) — 12 trang, đã có ghi chú người trình bày.
- **Trình bày và nộp bài**: [Kịch bản 10 + 5 phút](reports/Nhom10_Kich_ban_thuyet_trinh.md), [danh mục nộp](reports/Nhom10_Huong_dan_nop.md).
- **Hướng dẫn sản phẩm**: [reports/README.md](reports/README.md); bản khung cũ được giữ riêng để truy vết.
- **Template slide gốc**: [docs/Slides.pptx](docs/Slides.pptx).

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

**Cập nhật 12/10/2026 — Bước 1–9 hoàn tất phần kỹ thuật/nội dung; Bước 10 đã có slide và kịch bản, chưa tổng duyệt. Chưa nộp bài.**

- **Bước 1–4**: Raw 31.069×90; baseline **28.987×16**; loại 2.082 dòng thiếu giá, giữ giá dương và missing predictor. [Review Bước 1–4](reports/qa_review_step_01_04.md).
- **Bước 5–6**: 12 artifact thống kê + metadata, 5 hình EDA 300 DPI và [4 phát hiện](reports/eda_findings.md). Codex đã review/sửa số mẫu, biểu đồ giới hạn trục, diễn giải ANOVA và số liệu. [Review Bước 5–6](reports/qa_review_step_05_06.md).
- **Bước 7**: Đã review/sửa bàn giao Claude; chọn biến riêng trên training folds, giữ chẩn đoán ANOVA thực, sửa R² bị làm tròn và triển khai nhánh huấn luyện khả thi có kiểm thử. Dữ liệu Bangkok **chưa có predictor theo chính sách hiện tại**: không biến số đạt |r|≥0,30 và p<0,05; điều kiện dùng ANOVA làm bộ lọc phân loại chưa xác nhận. Đây không phải kết luận dữ liệu không thể mô hình hóa. Chỉ báo cáo mốc trung bình; test MSE 315.021.203,83 THB², R²≈−0,000014334. [Review Bước 7](reports/qa_review_step_07.md), [phương pháp](docs/MODELING_METHODS.md).
- **Bước 8–9**: Đã tổng hợp bốn RQ vào Word/PDF, điền Giới thiệu đúng hai đoạn và cam kết minh bạch theo xác nhận của nhóm. PDF 11 trang = bìa + **8 trang thân** + tham khảo + phụ lục; không còn ô chờ kết quả. [Hướng dẫn báo cáo](reports/README.md).
- **Bước 10**: Đã có 12 slide, ghi chú người nói, kịch bản 10 phút + demo 5 phút. Chưa có tổng duyệt hoặc video của nhóm.
- **Kiểm chứng**: 91 tests passed, coverage `src/` 89,18%; notebook 01–03 đã chạy ở review Bước 5–6, notebook 04 chạy lại sau sửa Bước 7. Tái lập độc lập split/fold, chọn biến và MSE/R² đạt; raw giữ hash/mtime, baseline và template giữ hash. [Kiểm tra tổng hợp](reports/qa_audit_report.md), [JSON Bước 7](reports/qa_step_07_verification.json).
- **Việc còn lại của nhóm**: chạy trên máy cá nhân, đọc/kiểm tra chéo Word–PDF–slide, tổng duyệt, xác nhận giờ/kênh nộp và yêu cầu video, sau đó nộp trước hạn. Chưa ghi nhận những việc này đã hoàn tất.

<a id="ke-hoach-trien-khai"></a>

## Hạn Nộp Và Phân Công Từng Chặng

- **Hạn nộp: 18/10/2026**, theo thông tin người dùng cung cấp ngày 10/10/2026.
- **Giờ chốt nộp và kênh nộp**: chưa xác nhận; Thắng kiểm tra thông báo chính thức của giảng viên trong ngày 12/10. Không mặc định hạn chót là 23:59.
- **Ngày/giờ thuyết trình**: chưa xác nhận riêng; Thắng cập nhật khi có thông báo.
- **Mục tiêu nội bộ**: hoàn tất bộ nộp và tổng duyệt vào 17/10/2026; dành 18/10 để kiểm tra và nộp trước giờ chốt.
- Các mốc bên dưới là **kế hoạch nội bộ**, không phải ngày hoàn thành thực tế hay lịch giảng viên giao. Ngày tháng theo giờ Việt Nam (UTC+7).

Trong bảng: **Thắng = Phạm Quốc Thắng**, **Thiện = Lê Minh Thiện**. Người phụ trách tạo đầu ra; người kiểm tra chéo đối chiếu đầu ra với tiêu chí trước khi chuyển trạng thái sang “Hoàn thành”.

| Chặng | Mốc nội bộ | Phụ trách | Kiểm tra chéo | Đầu ra và điều kiện hoàn thành | Trạng thái 12/10 |
|---|---|---|---|---|---|
| Chuẩn bị: tài liệu và lịch | 10/10/2026 | Thắng | Thiện | README và hai đặc tả thống nhất; có hạn nộp, phân công và tiêu chí bàn giao | Đã cập nhật tài liệu; chờ nhóm kiểm tra |
| Chuẩn bị: môi trường | 10/10/2026 | Thiện | Thắng | `requirements.txt`, `requirements-dev.txt`, `requirements-lock.txt`, `pyproject.toml`, `.venv`, `docs/RUNBOOK.md`; hai thành viên cài và chạy được môi trường | Đã có môi trường/lock và chạy notebook; chờ hai thành viên chạy trên máy cá nhân |
| Bước 1: thu thập và kiểm toán | 11/10/2026 | Thiện | Thắng | `data/raw/`, `data/source_manifest.json`, `docs/DATA_AUDIT.md`, `src/data_audit.py`, `reports/audit/`, test kiểm toán; xác minh schema, giá, đơn vị quan sát và checksum; chạy lại được | Hoàn tất kỹ thuật 10/10; Codex review và kiểm tra độc lập; xem reports/qa_review_step_01_04.md |
| Bước 2: chốt RQ | 11/10/2026, sau Bước 1 | Thắng | Thiện | Ma trận RQ–biến–phương pháp–biểu đồ–giới hạn trong `docs/DATA_AUDIT.md`; chỉ giữ RQ có dữ liệu đáp ứng | Giữ 4 RQ theo dữ liệu thực; đã kiểm định chi tiết ở Bước 5–6 |
| Bước 3: phương án làm sạch | 12/10/2026 | Thiện | Thắng | Bảng Vấn đề–Xử lý–Lý do–Ảnh hưởng trong `docs/CLEANING_PLAN.md`; tách EDA/mô hình, không điền giá thiếu | Hoàn tất kỹ thuật 10/10: docs/CLEANING_PLAN.md; Codex đối chiếu code với phương án |
| Bước 4: thực thi làm sạch | 12/10/2026, sau Bước 3 | Thiện | Thắng | `src/wrangling.py`, notebook 01, `data/processed/`; ghi số dòng trước/sau, kiểm tra dữ liệu và giữ nguyên file thô | Hoàn tất kỹ thuật 10/10: wrangling, notebook 01, baseline và nhật ký; Codex kiểm tra tái lập |
| Bước 5: EDA biến giá | 13/10/2026 | Thắng | Thiện | Notebook 02 có thống kê mô tả, phân bố và ngoại lệ; nhận xét truy được về kết quả chạy | Hoàn tất kỹ thuật, Codex review/sửa ngày 11/10: src/eda_stats.py, notebook 02, reports/stats/, reports/eda_findings.md; chờ nhóm kiểm tra chéo |
| Bước 6: yếu tố liên quan và hình | 14/10/2026 | Thắng (hình/diễn giải), Thiện (kiểm định) | Kiểm tra chéo phần của nhau | Notebook 02–03, bảng r–p/F–p khi đủ điều kiện, số mẫu hợp lệ và ảnh 300 DPI trả lời RQ | Hoàn tất kỹ thuật, Codex review/sửa ngày 11/10: src/visualization.py, notebook 03, 5 ảnh 300 DPI và catalog tại reports/figures/; chờ nhóm kiểm tra chéo |
| Bước 7: hồi quy bổ trợ | 15/10/2026 | Thiện | Thắng | Notebook 04: train/test, CV, chọn biến, MSE/R²; mô hình nếu phù hợp hoặc giải trình bằng dữ liệu | Hoàn tất kỹ thuật và review: 91 tests, notebook 04, 5 artifact; chưa xây hồi quy theo chính sách hiện tại, chỉ benchmark; xem qa_review_step_07.md; chờ nhóm kiểm tra chéo |
| Bước 8: tổng hợp kết quả | 16/10/2026 | Thắng | Thiện | 3–4 phát hiện kèm bảng/hình, giới hạn và nguồn kết quả; đưa vào bản thảo báo cáo | Đã tổng hợp bốn phát hiện, bằng chứng, Giới thiệu/Kết luận vào Word/PDF ngày 12/10; chờ nhóm rà soát nội dung |
| Bước 9: báo cáo và hồ sơ | 16/10/2026, sau Bước 8 | Thắng | Thiện | Word/PDF đúng template, phần thân 5–10 trang, phân công chi tiết và nguồn dữ liệu; chuẩn bị link dataset/video nếu thuộc diện yêu cầu | Đã có Word/PDF điền kết quả, 8 trang thân, nguồn và phân công; chờ nhóm đọc, kiểm tra trên máy cá nhân và chốt quy cách nộp |
| Bước 10: slide và tổng duyệt | 17/10/2026 | Thắng (slide), cả hai (demo) | Thiện kiểm tra số liệu và thời lượng | Slide, kịch bản 10 phút + demo 5 phút, video nếu học online; hai thành viên trình bày được phần mình | Đã có 12 slide và kịch bản 10 + 5 phút ngày 12/10; chưa tổng duyệt, chưa quay video |
| Kiểm tra toàn bộ bộ nộp | 17/10/2026 | Thiện | Thắng | `reports/qa_audit_report.md`: notebook chạy từ đầu đến cuối, test/lint đạt, checksum nguyên vẹn, số liệu Word/PDF/slide khớp; mở thử toàn bộ file | Đã kiểm tra kỹ thuật, số liệu và bố cục; qa_audit_report.md ghi minh chứng; còn kiểm tra chéo/máy cá nhân/tổng duyệt của nhóm |
| Nộp bài | 18/10/2026, trước giờ chốt được xác nhận | Thắng | Thiện | Đúng tên `Nhom10_...`, đủ sản phẩm theo template, link tải hoạt động nếu dùng; lưu bằng chứng nộp thành công | Chưa triển khai |

**Quy tắc cập nhật**: README là nơi duy nhất theo dõi lịch và phân công; hai đặc tả dẫn về bảng này. Khi bàn giao, ghi đường dẫn đầu ra, ngày hoàn thành thực tế và người kiểm tra vào ô trạng thái. Chưa có đầu ra hoặc chưa kiểm tra thì không đánh dấu hoàn thành. Nếu trễ mốc, ghi nguyên nhân và cập nhật các chặng phụ thuộc; ưu tiên bốn RQ và bộ nộp, chưa mở rộng dashboard/NLP/bản đồ.

**Các việc Thắng cần xác nhận từ thông báo giảng viên**: giờ/kênh nộp, lịch thuyết trình, yêu cầu video theo hình thức học, và ngưỡng dataset 50 MB/60 MB đang mâu thuẫn trong template.

---

## Cấu Trúc Thư Mục (Hiện Tại)

```text
workspaces/final-project/
├── README.md                  # Lịch, phân công và trạng thái duy nhất
├── docs/                      # Đặc tả, template bất biến, audit/methods/runbook
├── data/
│   ├── raw/                   # Inside Airbnb Bangkok 29/06/2026, bất biến
│   ├── processed/             # Baseline 28.987×16
│   └── source_manifest.json   # Nguồn, đơn vị, giấy phép, SHA-256
├── notebooks/                 # 01 kiểm toán; 02 EDA; 03 hình; 04 train/CV
├── src/                       # Module phân tích và mô hình
├── tests/                     # 91 kiểm thử
├── scripts/                   # Template notebook, dựng Word/slide/sơ đồ
├── requirements*.txt          # Phân tích/dev/lock; docs tách môi trường
├── pyproject.toml             # Ruff và pytest
└── reports/
    ├── audit/ cleaning/ stats/ # Bảng và nhật ký tính từ dữ liệu
    ├── figures/               # 5 hình EDA 300 DPI + sơ đồ quy trình báo cáo
    ├── modeling/              # Split, chọn biến, benchmark, metadata, findings
    ├── Nhom10_Bao_cao.docx     # Nội dung đã hoàn thiện, chờ nhóm đọc
    ├── Nhom10_Bao_cao.pdf      # 11 trang tổng, 8 trang thân
    ├── Nhom10_Slides.pptx     # 12 slide và ghi chú người trình bày
    ├── Nhom10_Slides.pdf      # Bản xem trước
    ├── Nhom10_Kich_ban_thuyet_trinh.md
    ├── Nhom10_Huong_dan_nop.md
    ├── qa_audit_report.md     # Kiểm tra tổng hợp và việc còn lại
    ├── qa_review_step_*.md    # Review từng chặng
    ├── qa_step_*verification.json
    ├── verification_step_*/   # Log kiểm chứng
    ├── archive/               # Word khung trước khi điền kết quả
    └── Nhom10_Bao_cao_Khung.pdf # PDF khung lịch sử, không nộp
```

Không có `models/best_pipeline.joblib` hay chẩn đoán hồi quy cho Bangkok vì chưa có predictor qua chính sách. Tài liệu link dataset/video chỉ tạo khi phát sinh điều kiện và đã có link thật; xem hướng dẫn nộp.
