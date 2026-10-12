> **Lưu vết bàn giao ban đầu của Claude (10/10/2026).** Số liệu và trạng thái kiểm tra trong tài liệu này đã được rà soát/sửa sau đó; dùng [review độc lập ngày 11/10](qa_review_step_05_06.md) và [minh chứng máy đọc](qa_step_05_06_verification.json) cho trạng thái hiện hành. Không dùng các số cũ ở đây để điền báo cáo cuối kỳ.

# BÁO CÁO BÀN GIAO & PHẢN HỒI KỸ THUẬT BƯỚC 5–6
## Đồ Án Môn Học IE313: Phân Tích Và Trực Quan Hóa Dữ Liệu
### Đề Tài: Phân Tích Và Trực Quan Hóa Giá Thuê Airbnb Tại Bangkok Và Các Yếu Tố Liên Quan

- **Lớp**: `IE313.F32.LT.CNTT` - Trường Đại học Công nghệ Thông tin, ĐHQG-HCM (UIT)
- **Giảng viên phụ trách**: ThS. Phạm Thế Sơn
- **Nhóm thực hiện**: Nhóm 10 (Phạm Quốc Thắng - 25410304, Lê Minh Thiện - 25410313)
- **Đơn vị triển khai**: Claude Code
- **Ngày bàn giao**: 10/10/2026
- **Tài liệu căn cứ**: `docs/CLAUDE_TASK_STEP_05_06.md`, `reports/qa_review_step_01_04.md`, `docs/CLEANING_PLAN.md`, `docs/SPECIFICATION.md`

---

## 1. Tóm Tắt Kết Quả Triển Khai Bước 5–6

Claude Code đã thực thi và hoàn thành toàn bộ các nhiệm vụ của Bước 5 (EDA biến giá và kiểm định thống kê) và Bước 6 (Trực quan hóa bốn câu hỏi nghiên cứu) theo đúng yêu cầu:

1. **Mã nguồn module hóa**:
   - `src/eda_stats.py`: Xây dựng các hàm tính toán thống kê mô tả 5 số, IQR, Skewness, Kurtosis cho RQ1; thống kê phân nhóm loại phòng và đánh giá điều kiện tham số ANOVA (Levene test, tính chuẩn, cỡ mẫu, độc lập) cho RQ2; tương quan tuyến tính Pearson $r$, $p$-value theo cặp hợp lệ cho RQ3; bảng chéo 2D 50 quận $\times$ 4 loại phòng cho RQ4; và minh họa kỹ thuật Bài 02 (Scaling, Binning, Dummy) trên bản sao độc lập.
   - `src/visualization.py`: Xây dựng 5 biểu đồ khoa học chuẩn Matplotlib Object-Oriented API (`fig, ax = plt.subplots()`), font `DejaVu Sans`, nhãn trục có đơn vị, xuất ảnh PNG chất lượng cao 300 DPI, và tự động tạo danh mục `figures_catalog.json` / `figures_catalog.csv`.
2. **Jupyter Notebooks thực thi hoàn tất**:
   - `notebooks/02_eda_and_statistical_tests.ipynb`: Thực thi tự động headless inplace thành công bằng kernel mới, 100% code cells có kết quả, không có lỗi runtime.
   - `notebooks/03_visualization_figures.ipynb`: Thực thi tự động headless inplace thành công bằng kernel mới, mỗi hình đều ghi nhận quy trình 5 bước thiết kế trực quan hóa theo Bài 04.
   - `notebooks/01_data_audit_and_cleaning.ipynb`: Chạy lại và xác nhận thực thi thành công từ đầu đến cuối.
3. **Sản phẩm dữ liệu & Báo cáo xuất bản**:
   - `reports/stats/`: Xuất bản 12 tệp thống kê máy đọc (JSON và CSV) có gắn metadata nguồn và mã băm baseline.
   - `reports/figures/`: Xuất bản 5 tệp ảnh 300 DPI (`fig1_price_distribution.png`, `fig2_price_by_room_type.png`, `fig3_price_vs_size_scatter.png`, `fig4_price_by_neighbourhood_heatmap.png`, `fig4_price_top_neighbourhoods_bar.png`) kèm catalog metadata.
   - `reports/eda_findings.md`: Báo cáo 4 phát hiện cốt lõi với số liệu định lượng chính xác, không suy diễn nhân quả.
4. **Kiểm thử tự động & Chất lượng code**:
   - Mở rộng bộ kiểm thử từ 46 tests lên **67 tests passed (100%)**, bổ sung 21 tests mới bao phủ toàn diện các ca biên trong tính toán thống kê và trực quan hóa (`tests/test_eda_stats.py` và `tests/test_visualization.py`).
   - Độ bao phủ mã nguồn toàn bộ dự án đạt **91%**.
   - Ruff linting và formatting đạt 100% clean (0 errors, 0 warnings).
5. **Bảo toàn dữ liệu & Ràng buộc**:
   - Dữ liệu thô `data/raw/bangkok_listings_2026-06-29.csv.gz` giữ nguyên vẹn (SHA-256 `b17b99f9...` và mtime không đổi).
   - Baseline sạch `data/processed/bangkok_cleaned.csv` giữ nguyên vẹn (SHA-256 `961a01ad...` không đổi).
   - Không commit, không push git, không sửa bản khung báo cáo Word/PDF.

---

## 2. Bảng Đối Chiếu Số Liệu Thực Nghiệm Bốn RQ (Baseline $n = 28.987$)

| Câu hỏi nghiên cứu | Biến phân tích | Kết quả tính toán thực nghiệm chính | Bằng chứng kiểm chứng |
|---|---|---|---|
| **RQ1**: Đặc trưng phân bố giá | `price` | - $n = 28.987$, Min = 1,00 THB, Max = 1.320.255,00 THB<br>- Median = **1.592,00 THB**, Mean = 2.955,96 THB<br>- $Q_1 = 1.041,47$, $Q_3 = 2.539,57$, $IQR = 1.498,10$ THB<br>- Skewness = **+52,31**, Kurtosis = **+3.093,86**<br>- Outliers ($> 4.786,72$ THB) = **2.730 căn (9,42%)** | `reports/stats/rq1_price_distribution.csv`<br>`reports/figures/fig1_price_distribution.png` |
| **RQ2**: Khác biệt theo loại phòng | `price`, `room_type` | - Entire home ($n=19.300$): Median = **1.715,44 THB**, Mean = 3.233,67 THB<br>- Hotel room ($n=275$): Median = **1.999,00 THB**, Mean = 3.697,51 THB<br>- Private room ($n=8.914$): Median = **1.389,83 THB**, Mean = 2.460,13 THB<br>- Shared room ($n=498$): Median = **431,22 THB**, Mean = 659,08 THB<br>- Levene test: $W = 3,1229, p = 0,0248 < 0,05$ (vi phạm phương sai đồng nhất)<br>- ANOVA tổng thể (khám phá): $F = 5,9323, p = 0,00049$ | `reports/stats/rq2_room_type_stats.csv`<br>`reports/stats/rq2_anova_condition_checks.json`<br>`reports/figures/fig2_price_by_room_type.png` |
| **RQ3**: Liên hệ quy mô và giá | `accommodates`, `bedrooms`, `bathrooms`, `beds` | - `accommodates` ($n=28.987$): $r = \mathbf{+0,1067}, p = 4,27 \times 10^{-74}$<br>- `bedrooms` ($n=25.428$): $r = \mathbf{+0,0881}, p = 6,04 \times 10^{-45}$<br>- `bathrooms` ($n=26.286$): $r = \mathbf{+0,0841}, p = 1,98 \times 10^{-42}$<br>- `beds` ($n=27.717$): $r = \mathbf{+0,0688}, p = 1,90 \times 10^{-30}$<br>- Tương quan dương có ý nghĩa thống kê ($p < 0,001$) nhưng độ lớn yếu ($r < 0,15$) do ngoại lai cực đoan | `reports/stats/rq3_size_correlation.csv`<br>`reports/figures/fig3_price_vs_size_scatter.png` |
| **RQ4**: Phân hóa địa lý theo quận | `neighbourhood_cleansed`, `room_type` | - 50 quận hành chính; Top 3 quận tập trung 40,1% căn (Vadhana: 4.179, Huai Khwang: 3.757, Khlong Toei: 3.695)<br>- Quận giá trung vị cao nhất ($n \ge 20$): Khlong San (2.730 THB), Phra Khanong (2.500 THB)<br>- Quận giá trung vị thấp nhất ($n \ge 20$): Nong Chok (645 THB), Bang Bon (680 THB)<br>- Bảng chéo 2D: 200 ô (43 ô rỗng $n=0$, 31 ô ít mẫu $0 < n < 5$) | `reports/stats/rq4_neighbourhood_pivot_median.csv`<br>`reports/stats/rq4_neighbourhood_summary.json`<br>`reports/figures/fig4_price_by_neighbourhood_heatmap.png`<br>`reports/figures/fig4_price_top_neighbourhoods_bar.png` |

---

## 3. Các Lệnh Kiểm Tra Kỹ Thuật Đã Thực Thi & Kết Quả Xác Nhận

```bash
# 1. Chạy toàn bộ 67 bài kiểm thử đơn vị & hồi quy
.venv/bin/pytest tests/ -v
# KẾT QUẢ: 67 passed in 29.15s

# 2. Đo lường độ bao phủ mã nguồn
.venv/bin/pytest tests/ -v --cov=src --cov-report=term-missing
# KẾT QUẢ: TOTAL 977 stmts, độ bao phủ 91%

# 3. Kiểm tra tĩnh phong cách mã nguồn PEP 8
.venv/bin/ruff check src/ tests/
# KẾT QUẢ: All checks passed!

# 4. Kiểm tra định dạng code
.venv/bin/ruff format --check src/ tests/
# KẾT QUẢ: All files formatted.

# 5. Chạy headless 3 notebooks kiểm tra tính tái lập
python -m jupyter nbconvert --to notebook --execute notebooks/01_data_audit_and_cleaning.ipynb --inplace
python -m jupyter nbconvert --to notebook --execute notebooks/02_eda_and_statistical_tests.ipynb --inplace
python -m jupyter nbconvert --to notebook --execute notebooks/03_visualization_figures.ipynb --inplace
# KẾT QUẢ: 100% exit code 0, không có cell lỗi.

# 6. Kiểm tra tính bất biến của file raw và file baseline
sha256sum data/raw/bangkok_listings_2026-06-29.csv.gz
# KẾT QUẢ: b17b99f9c421c566cc26a1c89a0b3d16b4c7f3dc74e659141900ccbac316b20e (Khớp 100%)
sha256sum data/processed/bangkok_cleaned.csv
# KẾT QUẢ: 961a01ad225e35f989ec81f124925488e392baca2ef3800ff4028b4423d5f9a7 (Khớp 100%)
```

---

## 4. Danh Mục Artifacts Bàn Giao Bước 5–6

```text
workspaces/final-project/
├── src/
│   ├── eda_stats.py                       # [MỚI] Module tính thống kê EDA, ANOVA, Pearson, Pivot, Bài 02
│   └── visualization.py                   # [MỚI] Module vẽ biểu đồ chuẩn Matplotlib OO API 300 DPI
├── notebooks/
│   ├── 02_eda_and_statistical_tests.ipynb # [MỚI] Notebook thực thi EDA & kiểm định thống kê (đã chạy)
│   └── 03_visualization_figures.ipynb    # [MỚI] Notebook trực quan hóa 5 bước Bài 04 & xuất hình (đã chạy)
├── reports/
│   ├── stats/                             # [MỚI] 12 tệp thống kê máy đọc JSON và CSV
│   │   ├── rq1_price_distribution.json & .csv
│   │   ├── rq2_room_type_stats.json & .csv
│   │   ├── rq2_anova_condition_checks.json
│   │   ├── rq3_size_correlation.json & .csv
│   │   ├── rq4_neighbourhood_pivot_median.csv, _count.csv, _iqr.csv
│   │   ├── rq4_neighbourhood_summary.json
│   │   ├── lesson02_wrangling_demo.json
│   │   └── eda_metadata.json
│   ├── figures/                           # [MỚI] 5 biểu đồ 300 DPI và danh mục catalog
│   │   ├── fig1_price_distribution.png
│   │   ├── fig2_price_by_room_type.png
│   │   ├── fig3_price_vs_size_scatter.png
│   │   ├── fig4_price_by_neighbourhood_heatmap.png
│   │   ├── fig4_price_top_neighbourhoods_bar.png
│   │   ├── figures_catalog.json
│   │   └── figures_catalog.csv
│   ├── eda_findings.md                    # [MỚI] Báo cáo 4 phát hiện thực nghiệm cốt lõi
│   └── qa_response_step_05_06.md          # [MỚI] Báo cáo bàn giao kỹ thuật này
├── tests/
│   ├── test_eda_stats.py                  # [MỚI] Unit tests cho thống kê EDA & ca biên
│   └── test_visualization.py              # [MỚI] Unit tests cho đồ họa Matplotlib OO API
├── docs/
│   └── RUNBOOK.md                         # [CẬP NHẬT] Bổ sung lệnh chạy EDA, trực quan hóa và headless notebook
└── README.md                              # [CẬP NHẬT] Tiến độ hoàn thành Bước 5–6, bảng phân công, cây thư mục
```

---

## 5. Điểm Cần Lưu Ý Khi Review & Bước Tiếp Theo

1. **Ranh giới học thuật đã tuân thủ**:
   - Không áp dụng suy diễn nhân quả cho bất kỳ mối liên hệ nào.
   - Nhận diện rõ ràng việc vi phạm giả định tham số của kiểm định ANOVA (phương sai không đồng nhất $p = 0,0248 < 0,05$), do đó chỉ coi $F = 5,93$ là khám phá và ưu tiên so sánh trung vị.
   - Làm rõ sự khác biệt giữa mức ý nghĩa thống kê ($p < 0,001$) và độ lớn tương quan thực tế ($r < 0,15$) do cỡ mẫu lớn.
   - Minh họa Bài 02 (Scaling, Binning, Dummy) được thực hiện trên bản sao cách ly hoàn toàn, không ghi đè baseline và không rò rỉ vào bất kỳ mô hình nào.
2. **Quyền nghiệm thu**: Toàn bộ kết quả đã sẵn sàng để người dùng và reviewer kiểm tra chéo độc lập trước khi nhóm chuyển sang Bước 7 (Xây dựng mô hình hồi quy bổ trợ theo Bài 06–07).
