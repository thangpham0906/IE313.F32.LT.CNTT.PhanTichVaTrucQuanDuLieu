# Hướng dẫn chạy và tái lập — Nhóm 10

Cập nhật 12/10/2026, phạm vi Bước 1–10 (triển khai kỹ thuật và chuẩn bị tài liệu). Làm việc trong `workspaces/final-project/`. Đã chạy trên Python 3.12.3/Linux; chưa xác nhận môi trường máy cá nhân của hai thành viên. Phương pháp Bước 7 xem `MODELING_METHODS.md`; kiểm tra chéo/tổng duyệt của nhóm còn pending.

## 1. Môi trường

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-lock.txt
```

Lock ghi các phiên bản đang dùng; việc cài thành công còn phụ thuộc Python/hệ điều hành. `requirements.txt` và `requirements-dev.txt` mô tả các phụ thuộc gốc; không tự nâng phiên bản khi tái lập.

## 2. Tái sử dụng hoặc thu thập raw

Raw bất biến: `data/raw/bangkok_listings_2026-06-29.csv.gz`, 20.625.983 bytes (20,626 MB thập phân; 19,670 MiB). Hàm bên dưới xác minh checksum trước khi tái sử dụng. Nếu chưa có file, tải vào thư mục tạm riêng ngoài raw, xác minh rồi tạo đích không ghi đè. Nếu file hiện có sai hash thì báo lỗi và giữ nguyên.

```bash
python - <<'PY'
from src.data_loader import safe_acquire_raw_data
print(safe_acquire_raw_data(
    source_url="https://data.insideairbnb.com/thailand/central-thailand/bangkok/2026-06-29/data/listings.csv.gz",
    target_filepath="data/raw/bangkok_listings_2026-06-29.csv.gz",
    expected_sha256="b17b99f9c421c566cc26a1c89a0b3d16b4c7f3dc74e659141900ccbac316b20e",
))
PY
```

Không dùng `mv` hay một tên tệp tạm cố định trong raw để thay thế quy trình này. Manifest tại `data/source_manifest.json`; không ghi lại thời điểm tải nếu chỉ tái sử dụng.

## 3. Kiểm toán và làm sạch — Bước 1–4

```bash
python -m src.data_audit \
  --input data/raw/bangkok_listings_2026-06-29.csv.gz \
  --output-dir reports/audit \
  --manifest data/source_manifest.json \
  --data-dictionary docs/sources/inside_airbnb_data_dictionary_v4.3.csv \
  --generate-markdown docs/DATA_AUDIT.md

python -m src.wrangling \
  --input data/raw/bangkok_listings_2026-06-29.csv.gz \
  --manifest data/source_manifest.json \
  --output-dir data/processed \
  --report-dir reports/cleaning
```

Baseline `data/processed/bangkok_cleaned.csv`: **28.987 × 16**, SHA-256 `961a01ad225e35f989ec81f124925488e392baca2ef3800ff4028b4423d5f9a7`. Xuất lại có thể thay mtime baseline; nội dung/hash phải giữ nguyên. Raw phải giữ cả nội dung/hash và mtime. Phương án: `docs/CLEANING_PLAN.md`.

## 4. EDA, hình và nhận xét — Bước 5–6

```bash
python -m src.eda_stats \
  --input data/processed/bangkok_cleaned.csv \
  --output-dir reports/stats \
  --expected-sha256 961a01ad225e35f989ec81f124925488e392baca2ef3800ff4028b4423d5f9a7

python -m src.visualization \
  --input data/processed/bangkok_cleaned.csv \
  --output-dir reports/figures

python -m src.eda_report
```

Đầu ra thống kê gồm **12 artifact + `eda_metadata.json`**: phân phối giá JSON/CSV, thống kê room_type JSON/CSV, điều kiện ANOVA JSON, Pearson JSON/CSV, 3 pivot median/count/IQR CSV, tóm tắt khu vực JSON và minh họa Bài 02 JSON. Metadata ghi checksum và thời điểm chạy; timestamp thay đổi khi tái lập, các số liệu phải khớp.

5 hình PNG 300 DPI và catalog JSON/CSV:

| Tệp | Quy tắc đọc |
|---|---|
| `fig1_price_distribution.png` | Histogram toàn miền, trục log10; panel ≤10.000 THB: 28.210 dòng hiển thị, 777 ngoài khung. Không biến đổi giá trong thống kê. |
| `fig2_price_by_room_type.png` | Hộp/râu/trung vị tính toàn nhóm, sau đó giới hạn trục 8.000 THB; đoạn Q1–Q3 không phải khoảng tin cậy. |
| `fig3_price_vs_size_scatter.png` | Pearson/OLS toàn bộ cặp hợp lệ; lấy tối đa 3.000 điểm seed42 để vẽ, chỉ hiển thị điểm ≤20.000 THB. Catalog ghi n chọn, n vẽ và n ngoài trục từng panel. |
| `fig4_price_by_neighbourhood_heatmap.png` | 15 quận đông listing, nhãn trung vị và n; ô ít mẫu n<5 có dấu *. |
| `fig4_price_top_neighbourhoods_bar.png` | So sánh trong cùng Entire home/apt, ngưỡng n≥20 chỉ là lựa chọn hiển thị. |

`reports/eda_findings.md` được sinh từ bảng/catalog; không sửa số liệu bằng tay rồi để lần chạy sau ghi đè. Chỉnh nội dung sinh tại `src/eda_report.py` nếu cần. Phương pháp, giới hạn ANOVA và nhãn mở rộng Levene/qcut tại [EDA_METHODS.md](EDA_METHODS.md).

## 5. Hồi quy bổ trợ & Đánh giá khả thi — Bước 7

```bash
python -m src.modeling \
  --input data/processed/bangkok_cleaned.csv \
  --output-dir reports/modeling \
  --expected-sha256 961a01ad225e35f989ec81f124925488e392baca2ef3800ff4028b4423d5f9a7
```

Đầu ra mô hình hóa gồm **5 artifact**:
1. `split_assignments.csv`: Phân chia 70% Train ($n=20.290$) và 30% Test ($n=8.697$) với `random_state=42`, phân fold 0..3 cho tập train.
2. `feature_selection.json`: Kết quả chọn biến độc lập trong 4 training folds và full train. Tất cả 7 biến số có $|r| < 0,12$ (không đạt ngưỡng $|r| \ge 0,30$), các điều kiện dùng ANOVA làm bộ lọc phân loại chưa được xác nhận; lưu chẩn đoán thực của từng biến/fold, không gán sẵn vi phạm.
3. `model_comparison.csv`: Bảng so sánh giữa mốc DummyRegressor (y_train mean benchmark) và 4 mô hình hồi quy học thuật (SLR, MLR, Poly-2, Ridge) với trạng thái chưa khả thi theo chính sách chọn biến hiện tại.
4. `modeling_metadata.json`: Siêu dữ liệu mô hình, phân tích giao thoa chủ nhà (82,81% test listing thuộc chủ nhà đã có ở train), quyết định chưa triển khai hồi quy theo chính sách hiện tại và giải trình lý do; không chứng minh dữ liệu không thể mô hình hóa.
5. `modeling_findings.md`: Báo cáo kết quả và giải trình khoa học Bước 7.

*Các artifact có điều kiện (`models/best_pipeline.joblib`, `reports/diagnostics/model_diagnostics.npz`, `reports/figures/model_*.png`)* không được tạo do không có mô hình hồi quy đạt chuẩn; tránh tạo artifact giả mạo.

## 6. Notebook từ đầu đến cuối

Thực thi tuần tự sau khi kích hoạt `.venv`:

```bash
python -m jupyter nbconvert --to notebook --execute notebooks/01_data_audit_and_cleaning.ipynb --inplace --ExecutePreprocessor.timeout=180
python -m jupyter nbconvert --to notebook --execute notebooks/02_eda_and_statistical_tests.ipynb --inplace --ExecutePreprocessor.timeout=180
python -m jupyter nbconvert --to notebook --execute notebooks/03_visualization_figures.ipynb --inplace --ExecutePreprocessor.timeout=180
python -m jupyter nbconvert --to notebook --execute notebooks/04_regression_modeling.ipynb --inplace --ExecutePreprocessor.timeout=180
```

Notebook 03 cũng đồng bộ nhận xét EDA. Notebook 04 thực thi phân chia tập, chọn biến trong fold, đánh giá mốc cơ sở DummyRegressor và báo cáo giải trình khoa học. `scripts/build_notebooks.py` khôi phục notebook từ bản mẫu đã review, mặc định giữ tệp hiện có. Chỉ dùng `--overwrite` khi chủ động muốn khôi phục; không dùng để mất sửa đổi/đầu ra notebook đang làm.

## 7. Kiểm tra kỹ thuật

```bash
pytest tests --cov=src --cov-report=term-missing
ruff check .
ruff format --check .
```

Mốc kiểm chứng 11/10/2026: **91 passed**, coverage unit-test `src/` **89,18%**, Ruff toàn thư mục đạt 100% clean. `src/eda_report.py` được kiểm tra qua CLI/notebook trên dữ liệu thực.

Minh chứng: [review Bước 1–4](../reports/qa_review_step_01_04.md), [review Bước 5–6](../reports/qa_review_step_05_06.md), [review Bước 7](../reports/qa_review_step_07.md). Nghiệm thu gồm raw nguyên vẹn, baseline khớp hash, cả 4 notebook không có cell lỗi, 12 bảng EDA tái lập, hình đúng tập mẫu/300 DPI, 5 artifact Bước 7 xuất bản đầy đủ. Kiểm tra kỹ thuật này chưa thay thế kiểm tra chéo của Thắng và Thiện.

## 8. Dựng Word, slide và PDF

Nội dung được quản lý tại `scripts/build_report.py` và `scripts/build_slides.py`; sửa các script này khi thay đổi bản thảo để lần dựng sau không mất sửa đổi. Nếu sửa trực tiếp Word/PPTX, lưu bản riêng trước khi chạy builder. Builder giữ template gốc; Word lấy bìa/styles từ `reports/archive/Nhom10_Bao_cao_Khung_20261010.docx`.

```bash
python3 -m venv .venv-docs
.venv-docs/bin/pip install -r requirements-docs.txt
.venv/bin/python scripts/create_report_flow.py
.venv-docs/bin/python scripts/build_report.py
.venv-docs/bin/python scripts/build_slides.py
```

Xuất PDF bằng Word/PowerPoint hoặc LibreOffice đã cài trên máy:

```bash
libreoffice --headless --convert-to pdf --outdir reports reports/Nhom10_Bao_cao.docx reports/Nhom10_Slides.pptx
```

Lần kiểm tra này dùng LibreOffice 24.2.7 trong môi trường tạm để xuất PDF, không đưa runtime vào bộ nộp. DOCX giữ Times New Roman theo mẫu; mở lại trên máy nhóm để kiểm tra font và phân trang của phần mềm sử dụng. PDF đã kiểm tra có 11 trang tổng/8 trang thân, slide 12 trang. Không nộp PDF khung cũ.

Kịch bản và việc còn lại: `reports/Nhom10_Kich_ban_thuyet_trinh.md`, `reports/Nhom10_Huong_dan_nop.md`. Không chạy lại mô hình để tìm kết quả đẹp hơn sau khi đã xem test; mọi thay đổi chính sách phải được ghi thành phương án mới và đánh giá phù hợp.
