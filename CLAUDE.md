# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.
For universal multi-agent collaboration across multiple AI assistants (Claude, GPT-4o/o1/o3, Gemini 2.0, DeepSeek, Copilot), refer to and maintain sync with `AGENTS.md`.

---

## 1. Academic Context & Course Profile

- **Môn học**: Phân tích và trực quan dữ liệu (Data Analysis and Visualization)
- **Mã môn học / Lớp**: `IE313` / `IE313.F32.LT.CNTT` (Hệ Liên thông Đại học - Ngành Công nghệ Thông tin)
- **Đơn vị đào tạo**: Trường Đại học Công nghệ Thông tin - Đại học Quốc gia TP.HCM (UIT / VNU-HCM)
- **Giảng viên phụ trách**: ThS. Phạm Thế Sơn
- **Tài liệu bài giảng chính thức**: Thư mục `slide-study/` (chứa 8 file bài giảng PDF gốc, xem chi tiết ở mục 3)
- **Bộ dữ liệu nghiên cứu xuyên suốt môn học**:
  - *UCI Automobile Dataset*: Dự báo và định giá xe hơi cũ (`https://archive.ics.uci.edu/ml/machine-learning-databases/autos/imports-85.data`)
  - *UN International Migration*: Thống kê dòng người nhập cư vào Canada từ 1980 - 2013 (`https://github.com/datasethub/ds105/blob/master/Canada.xlsx`)
  - *Bộ dữ liệu EDA & Modeling*: Các tập dữ liệu từ kho bài giảng `https://raw.githubusercontent.com/datasethub/ds105/master/` (`EDA_automobile.csv`, `Model_Dataset.csv`, `Model_Dataset_Lab.csv`, `Model-Evaluation-and-Refinement.csv`)

---

## 2. Development Environment & Common Commands

### 2.1 Môi trường ảo & Quản lý gói phụ thuộc

Ưu tiên sử dụng `uv` hoặc `venv` chuẩn của Python 3.10+:

```bash
# Thiết lập môi trường ảo với uv (khuyến nghị cho tốc độ cao)
uv venv .venv && source .venv/bin/activate
uv pip install -r requirements.txt

# Hoặc thiết lập bằng python3 venv tiêu chuẩn
python3 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Cài đặt toàn bộ bộ thư viện cốt lõi của môn học
pip install pandas numpy matplotlib seaborn scipy scikit-learn statsmodels wordcloud pywaffle dash jupyterlab ruff pytest
```

### 2.2 Khởi chạy JupyterLab / Notebook

```bash
# Khởi chạy JupyterLab không tự động mở trình duyệt (thích hợp môi trường server/WSL)
jupyter lab --no-browser --port=8888 --ip=0.0.0.0

# Khởi chạy Classic Notebook
jupyter notebook --no-browser --port=8888 --ip=0.0.0.0

# Thực thi notebook ở chế độ headless (chạy ngầm tự động không qua GUI)
jupyter nbconvert --to notebook --execute notebooks/01_data_ingestion.ipynb

# Chuyển đổi notebook sang script Python sạch để kiểm thử hoặc đóng gói
jupyter nbconvert --to script notebooks/02_data_wrangling.ipynb
```

### 2.3 Kiểm tra chất lượng mã nguồn & Định dạng

```bash
# Kiểm tra linting với Ruff
ruff check .

# Tự động sửa các lỗi linting có thể sửa tự động
ruff check . --fix

# Định dạng mã nguồn chuẩn PEP 8 với Ruff
ruff format .
```

### 2.4 Kiểm thử (Testing)

```bash
# Chạy toàn bộ unit tests
pytest

# Chạy kiểm thử cho một module cụ thể với hiển thị chi tiết (verbose)
pytest tests/test_wrangling.py -v

# Chạy kiểm thử kết hợp đo độ bao phủ code (coverage)
pytest --cov=src tests/
```

### 2.5 Thực thi các script xử lý dữ liệu

```bash
# Tải về bộ dữ liệu gốc từ nguồn mở
python src/ingestion.py --dataset automobile

# Chạy pipeline làm sạch dữ liệu
python src/wrangling.py --input datasets/raw/imports-85.data --output datasets/processed/automobile_cleaned.csv

# Huấn luyện và đánh giá mô hình hồi quy
python src/models.py --train
```

---

## 3. Course Syllabus & Slide Study Mapping

Tài liệu trong thư mục `slide-study/` đóng vai trò là kim chỉ nam về mặt lý thuyết, phương pháp luận và chuẩn công nghệ của môn học:

### Bài Thực Hành 01: Kỹ thuật Lập trình Python cho PTDL (`slide-study/Bai_Giang_TH_01_Python_for_DA.pdf`)
- **Nội dung**: Các kiểu dữ liệu cơ sở (`int`, `float`, `str`, `list`, `tuple`, `dict`, `set`, `bool`), cấu trúc điều khiển (`if/elif/else`, `for`, `while`), List/Dict Comprehensions.
- **Hàm & Lập trình hàm**: Định nghĩa hàm `def`, `*args`, `**kwargs`, hàm ẩn danh `lambda`, `map()`, `filter()`.
- **Cấu trúc dữ liệu phân tích cơ sở**: Giới thiệu về cấu trúc `Series` và `DataFrame` trong Pandas, mảng đa chiều trong NumPy.

### Bài 01: Giới thiệu Phân tích Dữ liệu - Nhập & Xuất Bộ Dữ Liệu (`slide-study/Bai01_Gioi_thieu_PTDL-Nhap_Xuat_Bo_du_lieu.pdf`)
- **Nội dung**: Tầm quan trọng của phân tích dữ liệu, bài toán định giá xe ô tô cũ (Used car valuation), cấu trúc thuộc tính và quan trắc.
- **Thư viện chính**: Pandas (`import pandas as pd`).
- **Thao tác I/O**: `pd.read_csv()`, `pd.read_excel()`, `pd.read_json()`, `pd.read_sql()`, `df.to_csv()`, `df.to_excel()`, `df.to_json()`, `df.to_sql()`.
- **Khám phá ban đầu**: `df.head()`, `df.tail()`, `df.info()`, `df.dtypes`, `df.describe()`, gán header khi file thiếu tiêu đề cột (`names=headers`).

### Bài 02: Sắp xếp Dữ liệu - Data Wrangling (`slide-study/Bai02_Sap_xep_DL.pdf`)
- **Xử lý giá trị khuyết (Missing Values)**: Phát hiện ký hiệu thiếu (`?`, `NaN`, `NA`), đếm giá trị thiếu `df.isnull().sum()`, loại bỏ dòng thiếu mục tiêu `df.dropna(subset=['price'], axis=0)`, điền giá trị thay thế bằng trung bình/trung vị `df.fillna()` hoặc `sklearn.impute.SimpleImputer`, `KNNImputer`.
- **Định dạng dữ liệu (Data Formatting)**: Ép kiểu dữ liệu phù hợp `df[col].astype()`, chuyển đổi đơn vị đo lường (ví dụ `mpg` sang `L/100km`).
- **Chuẩn hóa dữ liệu (Data Normalization)**:
  - *Simple Feature Scaling*: $x_{new} = \frac{x}{x_{max}}$
  - *Min-Max Scaling*: $x_{new} = \frac{x - x_{min}}{x_{max} - x_{min}}$ (`sklearn.preprocessing.MinMaxScaler`)
  - *Z-score Standardization*: $x_{new} = \frac{x - \mu}{\sigma}$ (`scipy.stats.zscore`, `StandardScaler`)
- **Phân nhóm dữ liệu (Binning)**: `pd.cut()` (chia khoảng đều về độ rộng), `pd.qcut()` (chia khoảng đều về tần số).
- **Mã hóa biến phân loại (Categorical Encoding)**: One-Hot Encoding / Dummy Variables thông qua `pd.get_dummies()`.

### Bài 03: Trực quan Dữ liệu Cơ bản - Matplotlib (`slide-study/Bai03_Truc_quan.pdf`)
- **Kiến trúc Matplotlib 3 tầng**:
  1. *Backend Layer*: `FigureCanvas`, `Renderer`, `Event`.
  2. *Artist Layer*: `Figure`, `Axes`, `Axis`, `Line2D`, `Text`, `Patch`.
  3. *Scripting Layer*: `matplotlib.pyplot`.
- **Các dạng biểu đồ cơ bản**: Line Plot, Area Plot, Histogram, Bar Chart (dọc/ngang), Pie Chart, Box Plot, Scatter Plot.
- **Bài toán thực tế**: Phân tích xu hướng nhập cư Canada từ 1980 đến 2013 (`Canada.xlsx`).

### Bài 04: Công cụ Trực quan Nâng cao (`slide-study/Bai04_Cong_cu_TQ.pdf`)
- **Quy trình 5 bước thiết kế trực quan**: Làm rõ vấn đề $\rightarrow$ Khám phá dữ liệu $\rightarrow$ Xác định thông điệp $\rightarrow$ Chọn biểu đồ phù hợp $\rightarrow$ Hoàn thiện hình thức (màu sắc, font chữ, chú thích).
- **Kỹ thuật biểu đồ chuyên sâu**:
  - *Waffle Chart*: Trực quan hóa tỷ lệ phần trăm đóng góp (`pywaffle`).
  - *Word Cloud*: Trực quan hóa tần suất văn bản/từ khóa (`wordcloud.WordCloud`).
  - *Seaborn Advanced*: Phân phối xác suất KDE, JointPlot, PairPlot.
  - *Data Dashboards*: Xây dựng dashboard tương tác bằng Plotly Dash hoặc subplot tổng hợp.

### Bài 05: Phân tích Thăm dò Dữ liệu - EDA (`slide-study/Bai05_PT_Tham_do.pdf`)
- **Thống kê mô tả (Descriptive Statistics)**:
  - Độ tập trung: Mean, Median, Mode.
  - Độ biến thiên: Range, Quartiles, IQR, Variance, Standard Deviation.
  - Hình dạng phân phối: Skewness (`df.skew()`), Kurtosis (`df.kurt()`).
- **Phân tích tương quan (Correlation Analysis)**:
  - Hệ số tương quan Pearson $r$ và mức ý nghĩa $p$-value (`scipy.stats.pearsonr`).
  - Ma trận tương quan trực quan qua Heatmap (`sns.heatmap(df.corr(), annot=True)`).
- **Phân nhóm và Bảng chéo**: `df.groupby()`, `pd.pivot_table()`.
- **Kiểm định ANOVA (Analysis of Variance)**: Kiểm định sai khác trung bình giữa các nhóm phân loại đối với biến số mục tiêu qua $F$-test và $p$-value (`scipy.stats.f_oneway`).

### Bài 06: Phát triển Mô hình Hồi quy (`slide-study/Bai06_Mo_hinh.pdf`)
- **Mô hình hồi quy tuyến tính**:
  - Đơn biến (SLR): $Y = b_0 + b_1 X$ (`sklearn.linear_model.LinearRegression`).
  - Đa biến (MLR): $Y = b_0 + b_1 X_1 + b_2 X_2 + \dots + b_n X_n$.
- **Chẩn đoán mô hình trực quan**:
  - Regression Plot: `sns.regplot`.
  - Residual Plot: `sns.residplot` (kiểm tra giả định phần dư ngẫu nhiên, không có mẫu hình đường cong hay phương sai thay đổi).
  - Distribution Plot: `sns.kdeplot` so sánh phân phối giá trị thực $Y$ và giá trị dự báo $\hat{Y}$.
- **Hồi quy đa thức (Polynomial Regression)**: `np.polyfit`, `sklearn.preprocessing.PolynomialFeatures`.
- **Scikit-Learn Pipeline**: Tích hợp chuẩn hóa `StandardScaler`, tạo đặc trưng bậc cao `PolynomialFeatures`, và `LinearRegression` vào `sklearn.pipeline.Pipeline`.
- **Thước đo đánh giá in-sample**: Sai số toàn phương trung bình (MSE - `mean_squared_error`), Hệ số xác định ($R^2$ / `r2_score`).

### Bài 07: Đánh giá và Tinh chỉnh Mô hình (`slide-study/Bai07_Danh_gia_MH.pdf`)
- **Phân chia tập dữ liệu**: Train/Test split (`sklearn.model_selection.train_test_split`) với `random_state` cố định.
- **Kiểm định chéo (Cross-Validation)**: $K$-Fold Cross Validation (`cross_val_score`, `cross_val_predict`).
- **Chẩn đoán Overfitting và Underfitting**: So sánh sai số trên tập Train vs tập Test theo bậc của đa thức.
- **Kỹ thuật điều chuẩn (Regularization)**: Hồi quy Ridge ($L_2$ regularization - `sklearn.linear_model.Ridge`) với siêu tham số điều chuẩn $\alpha$.
- **Tối ưu hóa siêu tham số (Hyperparameter Tuning)**: Tìm kiếm trên lưới `GridSearchCV` để xác định $\alpha$ tối ưu.

---

## 4. Standard Data Science Pipeline Flow

Mọi bài tập, đồ án hoặc mã nguồn thực hành trong repository này đều phải tuân thủ nghiêm ngặt quy trình 6 bước:

```
[1. Ingestion]     -> Đọc dữ liệu từ file/nguồn mạng, kiểm tra metadata ban đầu (shape, dtypes, nulls)
       ↓
[2. Wrangling]     -> Xử lý nulls, ép kiểu, chuẩn hóa (Min-Max/Z-score), binning, mã hóa dummy
       ↓
[3. EDA]           -> Thống kê mô tả, kiểm tra phân phối (skew/kurt), tương quan Pearson, ANOVA
       ↓
[4. Visualization] -> Trực quan hóa đặc trưng bằng Matplotlib/Seaborn có đầy đủ nhãn và chú thích
       ↓
[5. Modeling]      -> Xây dựng Pipeline (Scaler + PolyFeatures + LinearRegression/Ridge)
       ↓
[6. Evaluation]    -> K-Fold CV, chẩn đoán Residual/Distribution plot, đo lường MSE & R², Grid Search
```

---

## 5. Repository Directory Architecture

Đề xuất kiến trúc thư mục chuẩn cho bài tập, thí nghiệm và đồ án môn học:

```
IE313.F32.LT.CNTT.PhanTichVaTrucQuanDuLieu/
├── AGENTS.md                           # Tiêu chuẩn đa tác tử AI (Universal Multi-Agent Specification)
├── CLAUDE.md                           # Tài liệu chỉ dẫn Claude Code (file này)
├── requirements.txt                    # Danh sách thư viện cần thiết cho môn học
├── pyproject.toml                      # Cấu hình ruff, pytest và thông tin dự án
├── .gitignore                          # Bỏ qua virtualenv, cache jupyter, và checkpoints
│
├── slide-study/                        # 8 bài giảng PDF chính thức (Tài liệu gốc tham khảo)
│   ├── Bai01_Gioi_thieu_PTDL-Nhap_Xuat_Bo_du_lieu.pdf
│   ├── Bai02_Sap_xep_DL.pdf
│   ├── Bai03_Truc_quan.pdf
│   ├── Bai04_Cong_cu_TQ.pdf
│   ├── Bai05_PT_Tham_do.pdf
│   ├── Bai06_Mo_hinh.pdf
│   ├── Bai07_Danh_gia_MH.pdf
│   └── Bai_Giang_TH_01_Python_for_DA.pdf
│
├── datasets/                           # Lưu trữ tập dữ liệu (không sửa đổi dữ liệu gốc)
│   ├── raw/                            # Dữ liệu thô tải từ UCI, UN, hoặc GitHub
│   └── processed/                      # Dữ liệu đã làm sạch qua bước Wrangling
│
├── notebooks/                          # Jupyter Notebooks tương ứng với từng chủ đề bài giảng
│   ├── 00_python_fundamentals.ipynb    # Thực hành nền tảng Python (TH 01)
│   ├── 01_data_ingestion.ipynb         # Nhập xuất dữ liệu & khám phá sơ bộ (Bài 01)
│   ├── 02_data_wrangling.ipynb         # Tiền xử lý dữ liệu (Bài 02)
│   ├── 03_basic_visualization.ipynb    # Trực quan hóa Matplotlib cơ bản (Bài 03)
│   ├── 04_advanced_visualization.ipynb # Trực quan hóa nâng cao (Bài 04)
│   ├── 05_exploratory_data_analysis.ipynb # Thống kê, tương quan & ANOVA (Bài 05)
│   ├── 06_model_development.ipynb      # Hồi quy tuyến tính & Pipeline (Bài 06)
│   └── 07_model_evaluation.ipynb       # Đánh giá, Ridge & Grid Search (Bài 07)
│
├── labs/                               # Bài nộp thực hành định kỳ & Đồ án môn học
│   ├── lab01/                          # Bài thực hành Lab 01
│   ├── lab02/                          # Bài thực hành Lab 02
│   └── final_project/                  # Đồ án cuối kỳ (ví dụ: Định giá xe hơi, Bất động sản)
│       ├── data/
│       ├── notebooks/
│       └── report/
│
├── src/                                # Mã nguồn module hóa (phục vụ tái sử dụng)
│   ├── __init__.py
│   ├── ingestion.py                    # Module tải và nạp dữ liệu
│   ├── wrangling.py                    # Module làm sạch, chuẩn hóa và mã hóa
│   ├── eda.py                          # Module tính tương quan, thống kê và ANOVA
│   ├── visualization.py                # Module vẽ biểu đồ chuẩn hóa
│   └── models.py                       # Module huấn luyện pipeline và tinh chỉnh Ridge
│
├── tests/                              # Unit tests kiểm định tính đúng đắn của pipeline
│   ├── __init__.py
│   ├── test_wrangling.py               # Kiểm tra hàm điền null, scaling, encoding
│   └── test_models.py                  # Kiểm tra pipeline hồi quy và độ đo MSE/R2
│
└── reports/                            # Kết quả xuất bản
    └── figures/                        # File ảnh PNG/PDF biểu đồ xuất ra phục vụ báo cáo
```

---

## 6. Code Quality & Visualization Guidelines

Khi tạo hoặc sửa đổi mã nguồn trong repository này, luôn tuân thủ các chuẩn mực:

1. **Object-Oriented Matplotlib API**:
   - Tránh dùng state-machine (`plt.plot(...)`) khi vẽ biểu đồ phức tạp.
   - Luôn khởi tạo rõ ràng Figure và Axes:
     ```python
     fig, ax = plt.subplots(figsize=(10, 6))
     ax.plot(x, y, label="Trend")
     ax.set_title("Biểu đồ Xu hướng", fontsize=14, pad=12)
     ax.set_xlabel("Năm", fontsize=12)
     ax.set_ylabel("Số lượng (người)", fontsize=12)
     ax.legend(loc="best")
     ax.grid(True, linestyle="--", alpha=0.6)
     plt.tight_layout()
     ```
2. **Quy chuẩn ghi nhãn biểu đồ**:
   - Mọi biểu đồ trực quan hóa bắt buộc phải có: Tiêu đề rõ ràng, Nhãn trục $X$ và $Y$ (kèm đơn vị tính như `USD`, `km/h`, `L/100km`), và Chú giải (Legend) khi có nhiều hơn một chuỗi dữ liệu.
3. **Tính tái lập trong phân tích (Reproducibility)**:
   - Luôn cố định `random_state` (ví dụ `random_state=42` hoặc `0`) trong các hàm phân chia tập dữ liệu (`train_test_split`), chia $K$-Fold CV, và các thuật toán có yếu tố ngẫu nhiên.
4. **Bảo toàn dữ liệu thô (Raw Data Immutability)**:
   - Tuyệt đối không ghi đè dữ liệu trực tiếp lên file trong `datasets/raw/`. File sạch phải được lưu riêng sang `datasets/processed/`.
5. **Clean Code & Type Hints**:
   - Viết docstring mô tả tham số và kiểu trả về cho các hàm trong thư mục `src/`.
   - Sử dụng Type Hints (`pd.DataFrame`, `tuple[float, float]`, v.v.) để tăng tính rõ ràng và hỗ trợ công cụ phân tích tĩnh.
