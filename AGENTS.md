# AGENTS.md - Universal Multi-AI Agent Specification & Operating System
# Bản Đặc Tả Hệ Thống Đa Tác Tử AI - Môn học IE313: Phân Tích Và Trực Quan Dữ Liệu

> **Course**: IE313 - Phân tích và trực quan dữ liệu (Data Analysis and Visualization)  
> **Class**: `IE313.F32.LT.CNTT` - Hệ Liên thông Đại học, Khoa Công nghệ Thông tin  
> **Institution**: Trường Đại học Công nghệ Thông tin - Đại học Quốc gia TP.HCM (UIT - VNU-HCM)  
> **Instructor**: ThS. Phạm Thế Sơn  
> **Companion Governance Document**: [CLAUDE.md](./CLAUDE.md) (Quy chuẩn kỹ thuật, môi trường, và ánh xạ bài giảng)  
> **Primary Slide Knowledge Base**: Thư mục `slide-study/` (8 file bài giảng PDF chính thức)  
> **Target Audience**: Sinh viên UIT, Giảng viên, Trợ giảng, và các hệ thống AI (Claude Code, OpenAI GPT-4o/o1/o3, Google Gemini 2.0, DeepSeek V3/R1, Cursor, GitHub Copilot)

---

## Table of Contents / Mục Lục

1. [Tổng Quan Kiến Trúc & Khung Đa Tác Tử (Architectural Overview & Multi-AI Framework)](#1-tổng-quan-kiến-trúc--khung-đa-tác-tử-architectural-overview--multi-ai-framework)
   - [1.1 Chuẩn Mở AGENTS.md & Khả Năng Tương Thích (Open AGENTS.md Standard)](#11-chuẩn-mở-agentsmd--khả-năng-tương-thích-open-agentsmd-standard)
   - [1.2 Bối Cảnh Học Thuật & Liên Kết Hai Chiều (Academic Context & Two-way Document Linkage)](#12-bối-cảnh-học-thuật--liên-kết-hai-chiều-academic-context--two-way-document-linkage)
   - [1.3 Quy Trình Khoa Học Dữ Liệu Chuẩn 6 Bước (Standard 6-Stage Pipeline Flow)](#13-quy-trình-khoa-học-dữ-liệu-chuẩn-6-bước-standard-6-stage-pipeline-flow)
   - [1.4 Ma Trận Phân Công Mô Hình AI (Cross-AI Model Assignment Matrix)](#14-ma-trận-phân-công-mô-hình-ai-cross-ai-model-assignment-matrix)
2. [Hệ Sinh Thái & Vai Trò Tác Tử Chuyên Biệt (Specialized AI Agent Roles)](#2-hệ-sinh-thái--vai-trò-tác-tử-chuyên-biệt-specialized-ai-agent-roles)
   - [Role 1: Data Ingestion & Wrangling Agent (Thu thập & Xử lý Dữ liệu)](#role-1-data-ingestion--wrangling-agent-thu-thập--xử-lý-dữ-liệu)
   - [Role 2: EDA & Statistical Testing Agent (Khám phá & Kiểm định Thống kê)](#role-2-eda--statistical-testing-agent-khám-phá--kiểm-định-thống-kê)
   - [Role 3: Visualization Design Agent (Thiết kế Trực quan hóa Dữ liệu)](#role-3-visualization-design-agent-thiết-kế-trực-quan-hóa-dữ-liệu)
   - [Role 4: ML & Pipeline Modeling Agent (Mô hình hóa & Đánh giá Học máy)](#role-4-ml--pipeline-modeling-agent-mô-hình-hóa--đánh-giá-học-máy)
   - [Role 5: Academic Reviewer / QA Agent (Đánh giá Học thuật & Kiểm thử Tự động)](#role-5-academic-reviewer--qa-agent-đánh-giá-học-thuật--kiểm-thử-tự-động)
3. [Giao Thức Bàn Giao & Hợp Đồng Dữ Liệu (Inter-Agent Handoff Protocols & Data Contracts)](#3-giao-thức-bàn-giao--hợp-đồng-dữ-liệu-inter-agent-handoff-protocols--data-contracts)
   - [3.1 Danh Mục Bàn Giao & Vị Trí File Chuẩn (Standard Handoff Artifact Manifest)](#31-danh-mục-bàn-giao--vị-trí-file-chuẩn-standard-handoff-artifact-manifest)
   - [3.2 Chi Tiết Hợp Đồng & Định Dạng Schema (Detailed Data Contracts & Metadata Schemas)](#32-chi-tiết-hợp-đồng--định-dạng-schema-detailed-data-contracts--metadata-schemas)
4. [Mẫu Prompt Sẵn Sàng Thực Thi (Ready-to-Use Agent Dispatch Prompt Templates)](#4-mẫu-prompt-sẵn-sàng-thực-thi-ready-to-use-agent-dispatch-prompt-templates)
   - [4.1 Dispatch Prompt: Data Ingestion & Wrangling Agent](#41-dispatch-prompt-data-ingestion--wrangling-agent)
   - [4.2 Dispatch Prompt: EDA & Statistical Testing Agent](#42-dispatch-prompt-eda--statistical-testing-agent)
   - [4.3 Dispatch Prompt: Visualization Design Agent](#43-dispatch-prompt-visualization-design-agent)
   - [4.4 Dispatch Prompt: ML & Pipeline Modeling Agent](#44-dispatch-prompt-ml--pipeline-modeling-agent)
   - [4.5 Dispatch Prompt: Academic Reviewer / QA Agent](#45-dispatch-prompt-academic-reviewer--qa-agent)
5. [Chỉ Dẫn Tích Hợp Đa Nền Tảng AI (Multi-AI Platform Directives)](#5-chỉ-dẫn-tích-hợp-đa-nền-tảng-ai-multi-ai-platform-directives)
   - [5.1 Claude Code (CLI Subagents & Turn Control)](#51-claude-code-cli-subagents--turn-control)
   - [5.2 OpenAI ChatGPT & Codex (GPT-4o, o1, o3-mini)](#52-openai-chatgpt--codex-gpt-4o-o1-o3-mini)
   - [5.3 Cursor AI & Windsurf (Modern `.cursor/rules/*.mdc` Architecture)](#53-cursor-ai--windsurf-modern-cursorrulesmdc-architecture)
   - [5.4 GitHub Copilot (`.github/copilot-instructions.md`)](#54-github-copilot-githubcopilot-instructionsmd)
   - [5.5 Google Gemini 2.0 (Pro / Flash / Code Assist)](#55-google-gemini-20-pro--flash--code-assist)
   - [5.6 DeepSeek V3 / R1 (Aider / Shell / API)](#56-deepseek-v3--r1-aider--shell--api)
   - [5.7 Khung Điều Phối Tự Động (LangGraph, AutoGen, CrewAI)](#57-khung-điều-phối-tự-động-langgraph-autogen-crewai)
6. [Quy Chuẩn Bất Biến & Ràng Buộc Vận Hành (Strict Operational Constraints & Invariants)](#6-quy-chuẩn-bất-biến--ràng-buộc-vận-hành-strict-operational-constraints--invariants)
   - [6.1 Tính Bất Biến Của Dữ Liệu Thô (Raw Data Immutability)](#61-tính-bất-biến-của-dữ-liệu-thô-raw-data-immutability)
   - [6.2 Tính Tái Lập Tuyệt Đối (Reproducibility & random_state=42)](#62-tính-tái-lập-tuyệt-đối-reproducibility--random_state42)
   - [6.3 Chuẩn Mực Thống Kê & Ý Nghĩa p-value (Statistical Rigor & alpha=0.05)](#63-chuẩn-mực-thống-kê--ý-nghĩa-p-value-statistical-rigor--alpha005)
   - [6.4 Bắt Buộc Sử Dụng Matplotlib Object-Oriented API & Cấu Hình Font Tiếng Việt](#64-bắt-buộc-sử-dụng-matplotlib-object-oriented-api--cấu-hình-font-tiếng-việt)
   - [6.5 Không Rò Rỉ Dữ Liệu (Zero Data Leakage via Scikit-Learn Pipeline)](#65-không-rò-rỉ-dữ-liệu-zero-data-leakage-via-scikit-learn-pipeline)
   - [6.6 Quy Ước Ranh Giới Ngôn Ngữ (Bilingual Language Boundary Rules)](#66-quy-ước-ranh-giới-ngôn-ngữ-bilingual-language-boundary-rules)
7. [Bộ Lệnh Thực Thi & Kiểm Tra Chuẩn (Standard Toolchains & Verification Commands)](#7-bộ-lệnh-thực-thi--kiểm-tra-chuẩn-standard-toolchains--verification-commands)

---

## 1. Tổng Quan Kiến Trúc & Khung Đa Tác Tử (Architectural Overview & Multi-AI Framework)

### 1.1 Chuẩn Mở AGENTS.md & Khả Năng Tương Thích (Open AGENTS.md Standard)
Tệp `AGENTS.md` là tiêu chuẩn mở phổ quát (Universal Open Standard) nhằm định nghĩa cấu trúc vai trò, phạm vi quyền hạn, công cụ được phép sử dụng, và giao thức bàn giao dữ liệu khi nhiều hệ thống AI khác nhau cùng tham gia phát triển trong một dự án mã nguồn.

Trong môi trường môn học **IE313 (UIT - VNU-HCM)**, tài liệu này cho phép sinh viên và giảng viên kết hợp sức mạnh của nhiều trợ lý AI tiên tiến nhất hiện nay mà không gặp hiện tượng phân mảnh mã nguồn, xung đột quy ước hoặc hallucination:
- **Claude Code (Anthropic)**: Đóng vai trò điều phối kiến trúc tổng thể (Lead Architect), quản lý file, kiểm soát quy trình và thực thi subagents.
- **OpenAI (GPT-4o, o1, o3-mini)**: Phân tích toán học, kiểm định thống kê chuyên sâu, tính toán ma trận và tối ưu hóa siêu tham số.
- **Google Gemini 2.0 (Pro / Flash)**: Đọc hiểu tài liệu bài giảng PDF đa phương thức trong `slide-study/`, trích xuất công thức và đối chiếu bài tập.
- **DeepSeek (V3, R1)**: Triển khai thuật toán xử lý dữ liệu phức tạp, sinh mã kiểm thử `pytest` chính xác cao.
- **Cursor / Windsurf / GitHub Copilot**: Hỗ trợ sinh mã nội dòng (inline code completion) tuân thủ nghiêm ngặt chuẩn PEP 8 và Matplotlib OO API.

### 1.2 Bối Cảnh Học Thuật & Liên Kết Hai Chiều (Academic Context & Two-way Document Linkage)
Tài liệu này và [CLAUDE.md](./CLAUDE.md) tạo thành cặp tài liệu quản trị hai chiều (two-way governance documents):
- `CLAUDE.md` đóng vai trò là tài liệu hướng dẫn kỹ thuật chi tiết dành riêng cho Claude Code CLI.
- `AGENTS.md` đóng vai trò là bản thiết kế hệ sinh thái đa tác tử mở dành cho tất cả các mô hình AI và môi trường IDE.

**Thông tin môn học cơ sở**:
- **Tên môn**: Phân tích và trực quan dữ liệu (Data Analysis and Visualization) - Mã môn: `IE313`
- **Lớp**: `IE313.F32.LT.CNTT` (Hệ Liên thông Đại học - Khoa Công nghệ Thông tin, UIT)
- **Giảng viên**: ThS. Phạm Thế Sơn
- **Kho bài giảng chính thức**: `slide-study/` gồm 8 file PDF (chi tiết ánh xạ tại Mục 2).
- **Bộ dữ liệu chuẩn**:
  - *UCI Automobile Dataset*: `datasets/raw/imports-85.data` (205 dòng, 26 thuộc tính, bài toán định giá xe hơi cũ).
  - *UN International Migration*: `datasets/raw/Canada.xlsx` (Dòng người nhập cư vào Canada 1980 - 2013).
  - *Course Tabular Datasets*: `EDA_automobile.csv`, `Model_Dataset.csv`, `Model-Evaluation-and-Refinement.csv`.

### 1.3 Quy Trình Khoa Học Dữ Liệu Chuẩn 6 Bước (Standard 6-Stage Pipeline Flow)
Mọi tác tử AI khi tham gia giải quyết bất kỳ bài tập, lab hay đồ án nào trong repository đều phải tuân thủ nghiêm ngặt quy trình 6 giai đoạn:

```
[Raw Datasets] (datasets/raw/ - Bất biến)
      │
      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 1. DATA INGESTION & WRANGLING AGENT                                     │
│    Ánh xạ: Bai 01, Bai 02, TH 01                                        │
│    Nhiệm vụ: Đọc dữ liệu, xử lý '?', điền null, ép kiểu, scaling, dummy │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ Cleaned Data (H1, H2)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 2. EDA & STATISTICAL TESTING AGENT                                      │
│    Ánh xạ: Bai 05                                                       │
│    Nhiệm vụ: 5-number summary, Pearson r + p-value, ANOVA F-test, IQR   │
└──────────────────┬───────────────────────────────────┬──────────────────┘
                   │                                   │
                   │ Statistical Metrics (H4)          │ Significant Features (H3)
                   ▼                                   ▼
┌──────────────────────────────────────┐   ┌──────────────────────────────────────┐
│ 3. VISUALIZATION DESIGN AGENT        │   │ 4. ML & PIPELINE MODELING AGENT      │
│    Ánh xạ: Bai 03, Bai 04            │   │    Ánh xạ: Bai 06, Bai 07            │
│    Nhiệm vụ: Matplotlib OO API,      │   │    Nhiệm vụ: Pipeline (Scaler + Poly │
│    Seaborn KDE/PairPlot, Waffle,     │   │    + Ridge), CV, Residual, GridSearch│
│    WordCloud, 300 DPI Figures        │   │    Diagnostic Arrays (H5)            │
└──────────────────┬───────────────────┘   └──────────────────┬───────────────────┘
                   │                                          │
                   │ Figures & Dashboards                     │ Trained Pipeline & Metrics
                   └─────────────────────┬────────────────────┘
                                         │
                                         ▼ Full Repo State (H6)
┌─────────────────────────────────────────────────────────────────────────┐
│ 5. ACADEMIC REVIEWER / QA AGENT                                         │
│    Ánh xạ: Chuẩn đầu ra IE313, Thang Bloom, PEP 8, Ruff, Pytest         │
│    Nhiệm vụ: Chạy pytest, ruff check, headless jupyter nbconvert        │
└─────────────────────────────────────────────────────────────────────────┘
```

### 1.4 Ma Trận Phân Công Mô Hình AI (Cross-AI Model Assignment Matrix)

| Vai Trò Tác Tử (Agent Role) | Mô Hình Đề Xuất (Primary AI) | Mô Hình Dự Phòng (Fallback) | Nhiệm Vụ Trọng Tâm |
|---|---|---|---|
| **Role 1: Ingestion & Wrangling** | **DeepSeek V3 / Claude 3.7 Sonnet** | GPT-4o | Làm sạch dữ liệu, xử lý nulls, KNNImputer, unit conversion, scaling, binning, dummy |
| **Role 2: EDA & Statistical Testing** | **OpenAI o1 / o3-mini / GPT-4o** | Claude 3.7 Sonnet | Thống kê mô tả, CV, skewness, kurtosis, tương quan Pearson ($|r| \ge 0.3$), ANOVA $F$-test cặp nhóm |
| **Role 3: Visualization Design** | **Claude 3.7 Sonnet / Cursor** | GPT-4o | Matplotlib OO API, font Tiếng Việt, 5 bước trực quan hóa, Waffle, Word Cloud, Seaborn |
| **Role 4: ML & Pipeline Modeling** | **OpenAI o1 / Claude 3.7 Sonnet** | DeepSeek R1 | Scikit-Learn Pipeline, chẩn đoán 3 dạng Residual plot, $K$-Fold CV, điều chuẩn Ridge, GridSearchCV |
| **Role 5: Academic Reviewer / QA** | **Claude Code CLI / Cursor Agent** | Gemini 2.0 Pro / Flash | Chạy kiểm thử tự động, linting Ruff, headless nbconvert, kiểm tra immutability dữ liệu thô |

---

## 2. Hệ Sinh Thái & Vai Trò Tác Tử Chuyên Biệt (Specialized AI Agent Roles)

---

### Role 1: Data Ingestion & Wrangling Agent (Thu thập & Xử lý Dữ liệu)

- **Mục tiêu học thuật**: Làm chủ kỹ thuật đọc/ghi nhiều định dạng dữ liệu, chuẩn hóa cấu trúc dữ liệu bảng, xử lý triệt để các vấn đề chất lượng dữ liệu (khuyết thiếu, sai kiểu, không đồng nhất đơn vị) phục vụ phân tích.
- **Ánh xạ bài giảng chính thức (`slide-study/`)**:
  - `Bai_Giang_TH_01_Python_for_DA.pdf`: Nền tảng Python (kiểu dữ liệu nguyên thủy, cấu trúc điều khiển `if/else`, vòng lặp `for/while`, List/Dict Comprehensions, hàm `lambda`, mảng NumPy `ndarray`, cấu trúc Pandas `Series` và `DataFrame`).
  - `Bai01_Gioi_thieu_PTDL-Nhap_Xuat_Bo_du_lieu.pdf`: I/O dữ liệu (`read_csv`, `read_excel`, `read_json`, `read_sql`), quan sát sơ bộ (`head`, `tail`, `info`, `describe`, `dtypes`), gán danh sách tiêu đề (`names=headers`).
  - `Bai02_Sap_xep_DL.pdf`: Phát hiện ký hiệu thiếu (`?`, `NaN`), xóa dòng thiếu biến mục tiêu (`dropna(subset=['price'])`), điền khuyết bằng trung bình/trung vị/yếu vị (`fillna`, `SimpleImputer`, `KNNImputer`), ép kiểu (`astype`), chuyển đổi đơn vị (`mpg` sang `L/100km`), 3 phương pháp chuẩn hóa số học (Simple Feature Scaling, Min-Max, Z-score), phân khoảng (`pd.cut`, `np.linspace`), tạo biến giả (`pd.get_dummies`).

#### Nhiệm vụ cụ thể (Detailed Responsibilities):
1. **Nạp dữ liệu & Kiểm tra lược đồ (Schema Inspection)**:
   - Đọc dữ liệu từ file thô (`datasets/raw/imports-85.data`, `datasets/raw/Canada.xlsx`) an toàn, không làm biến đổi file gốc.
   - Gán đúng 26 header chuẩn cho bộ dữ liệu ô tô UCI:
     `['symboling', 'normalized-losses', 'make', 'fuel-type', 'aspiration', 'num-of-doors', 'body-style', 'drive-wheels', 'engine-location', 'wheel-base', 'length', 'width', 'height', 'curb-weight', 'engine-type', 'num-of-cylinders', 'engine-size', 'fuel-system', 'bore', 'stroke', 'compression-ratio', 'horsepower', 'peak-rpm', 'city-mpg', 'highway-mpg', 'price']`.
   - Đối với tập di dân Canada (`Canada.xlsx`), sử dụng tham số nạp chuẩn xác:
     `pd.read_excel('datasets/raw/Canada.xlsx', sheet_name='Canada by Citizenship', skiprows=range(20), skipfooter=2)`.
2. **Chiến lược xử lý giá trị khuyết (Missing Data Strategy - Bai02)**:
   - Thay thế toàn bộ ký tự `'?'` bằng `np.nan`.
   - *Khuyết trên biến mục tiêu (`price`)*: Bắt buộc loại bỏ dòng (`df.dropna(subset=['price'], axis=0, inplace=True)`), tuyệt đối không suy diễn giá trị mục tiêu.
   - *Khuyết biến số phân phối chuẩn (`normalized-losses`, `bore`, `stroke`)*: Điền bằng giá trị trung bình (`df[col].fillna(df[col].mean(), inplace=True)`).
   - *Khuyết biến số phân phối lệch / có ngoại lai (`horsepower`, `peak-rpm`)*: Điền bằng trung vị (`df[col].fillna(df[col].median(), inplace=True)`).
   - *Khuyết biến phân loại (`num-of-doors`)*: Điền bằng yếu vị (`df[col].fillna(df[col].mode()[0], inplace=True)`).
   - *Khuyết đa biến phức tạp*: Cho phép áp dụng `sklearn.impute.KNNImputer(n_neighbors=5, weights='distance')` cho các biến số có mối tương quan phi tuyến.
3. **Quy chuẩn chuyển đổi đơn vị đo lường (Unit Conversion - Bai02 p. 13)**:
   - Chuyển đổi mức tiêu hao nhiên liệu từ US mpg sang chuẩn quốc tế L/100km theo công thức:
     $$\text{city-L/100km} = \frac{235}{\text{city-mpg}}, \quad \text{highway-L/100km} = \frac{235}{\text{highway-mpg}}$$
   - *Quy chuẩn cấu trúc cột*: Thêm hai cột mới `city-L/100km` và `highway-L/100km` đồng thời lưu giữ hai cột gốc `city-mpg` và `highway-mpg` (kết quả bảng dữ liệu sạch đạt 28 cột) phục vụ đối chiếu phân tích.
4. **Chi tiết 3 phương pháp chuẩn hóa dữ liệu (Feature Scaling - Bai02)**:
   - *Simple Feature Scaling*: $x_{\text{new}} = \frac{x_{\text{old}}}{x_{\text{max}}}$
   - *Min-Max Normalization*: $x_{\text{new}} = \frac{x_{\text{old}} - x_{\text{min}}}{x_{\text{max}} - x_{\text{min}}} \in [0, 1]$ (áp dụng trên `length`, `width`, `height`)
   - *Z-score Standardization*: $x_{\text{new}} = \frac{x_{\text{old}} - \mu}{\sigma}$ (sử dụng `scipy.stats.zscore` hoặc `StandardScaler`)
5. **Rời rạc hóa (Binning) & Mã hóa biến giả (One-Hot Encoding)**:
   - Phân khoảng thuộc tính `price` thành 3 phân khúc (`Low`, `Medium`, `High`) bằng cách chia khoảng đều:
     ```python
     bins = np.linspace(min(df['price']), max(df['price']), 4)
     group_names = ['Low', 'Medium', 'High']
     df['price-binned'] = pd.cut(df['price'], bins, labels=group_names, include_lowest=True)
     ```
   - Mã hóa biến giả nhị phân: `pd.get_dummies(df, columns=['fuel-type', 'aspiration'], drop_first=True, dtype=int)`.

- **Dữ liệu đầu vào (Input Artifacts)**: `datasets/raw/imports-85.data`, `datasets/raw/Canada.xlsx`.
- **Kết quả bàn giao (Output Artifacts)**:
  - File dữ liệu sạch: `datasets/processed/automobile_cleaned.csv` (201 dòng, 28 cột), `datasets/processed/canada_cleaned.csv`.
  - File metadata bàn giao: `datasets/processed/automobile_cleaned_meta.json`.
  - Mã nguồn: `src/ingestion.py`, `src/wrangling.py`.
  - Notebooks: `notebooks/00_python_fundamentals.ipynb`, `01_data_ingestion.ipynb`, `02_data_wrangling.ipynb`.
- **Công cụ cho phép (Allowed Tools)**: Python 3.10+, `pandas`, `numpy`, `scipy.stats`, `scikit-learn` (`SimpleImputer`, `KNNImputer`, `MinMaxScaler`, `StandardScaler`).
- **Ràng buộc nghiêm ngặt (Strict Constraints)**:
  - *Tính bất biến*: Tuyệt đối không sửa đổi file trong `datasets/raw/`.
  - *Không còn kiểu object*: Các cột số liên tục sau khi xử lý bắt buộc phải có dtype `float64` hoặc `int64`.
  - *Biến mục tiêu sạch*: Cột `price` phải có đúng 0 giá trị null.

---

### Role 2: EDA & Statistical Testing Agent (Khám phá & Kiểm định Thống kê)

- **Mục tiêu học thuật**: Khám phá cấu trúc tiềm ẩn của dữ liệu thông qua các đại lượng thống kê mô tả, đo lường độ lệch, phát hiện ngoại lai, và kiểm định giả thuyết thống kê (tương quan Pearson, phân tích phương sai ANOVA) với mức ý nghĩa $\alpha = 0.05$.
- **Ánh xạ bài giảng chính thức (`slide-study/`)**:
  - `Bai05_PT_Tham_do.pdf`: Phân tích thăm dò dữ liệu (EDA).
  - Thống kê mô tả: Độ tập trung (Mean, Median, Mode), Độ phân tán (Range, Quartiles, $IQR = Q_3 - Q_1$, Variance, Standard Deviation $s$), Hệ số biến thiên ($CV = \frac{s}{\bar{x}} \times 100\%$).
  - Hình dạng phân phối: Skewness (`scipy.stats.skew`), Kurtosis (`scipy.stats.kurtosis`), ranh giới ngoại lai ($Q_1 - 1.5 \times IQR$ và $Q_3 + 1.5 \times IQR$).
  - Tương quan tuyến tính: Hệ số Pearson $r$ kèm giá trị $p$-value (`scipy.stats.pearsonr`), tiêu chuẩn chọn lọc $|r| \ge 0.30$ và $p < 0.05$.
  - Phân nhóm & Bảng chéo: `df.groupby()`, `pd.pivot_table()`.
  - Kiểm định ANOVA: Phân tích phương sai một yếu tố (`scipy.stats.f_oneway`) với kiểm định $F$-test, $p$-value và Pairwise Subgroup ANOVA.

#### Nhiệm vụ cụ thể (Detailed Responsibilities):
1. **Thống kê mô tả & Phân tích phân phối (Descriptive Statistics - Bai05)**:
   - Tính toán bảng tóm tắt 5 số (Min, $Q_1$, Median, $Q_3$, Max), trung bình, phương sai, độ lệch chuẩn.
   - Tính toán Hệ số biến thiên: $CV = \frac{s}{\bar{x}} \times 100\%$ để so sánh mức độ biến động giữa các biến có thứ nguyên khác nhau.
   - Đo lường Skewness (`df.skew()`) và Kurtosis (`df.kurt()`) để phát hiện phân phối lệch phải, lệch trái hoặc có đuôi nặng.
   - Xác định danh sách dòng chứa giá trị ngoại lai theo quy tắc $1.5 \times IQR$ cho các biến cốt lõi (`price`, `engine-size`, `horsepower`).
2. **Kiểm định tương quan Pearson & Tiêu chuẩn chọn lọc biến dự báo (Bai05 p. 37)**:
   - Tính hệ số tương quan Pearson $r$ và $p$-value (`scipy.stats.pearsonr`) giữa các biến số với biến mục tiêu `price`.
   - Áp dụng tiêu chuẩn học thuật của slide Bai05:
     - Tương quan mạnh: $|r| \ge 0.70$ và $p < 0.001$ (Đặc trưng ưu tiên cao nhất).
     - Tương quan trung bình: $0.40 \le |r| < 0.70$ và $p < 0.05$ (Đặc trưng có ý nghĩa).
     - Ngưỡng tối thiểu chọn vào mô hình: Bắt buộc $|r| \ge 0.30$ VÀ $p < 0.05$. Các biến có $|r| < 0.30$ hoặc $p \ge 0.05$ bị loại bỏ.
3. **Phân nhóm dữ liệu & Bảng chéo (Groupby & Pivot Table)**:
   - Sử dụng `df.groupby()` để nhóm theo các biến phân loại (`drive-wheels`, `body-style`) và tính giá trị trung bình của `price`.
   - Xây dựng `pd.pivot_table()` biểu diễn mối quan hệ 2 chiều giữa `drive-wheels` (hàng) và `body-style` (cột) đối với `price`.
4. **Kiểm định ANOVA One-way & Phân tích cặp nhóm con (Pairwise Subgroup ANOVA)**:
   - Bản chất toán học của $F$-score theo Bai05 p. 34:
     $$F = \frac{\text{Biến thiên giữa các nhóm (Variation between group means)}}{\text{Biến thiên nội tại trong nhóm (Variation within group)}}$$
   - Thực hiện kiểm định ANOVA tổng thể (`scipy.stats.f_oneway`) trên biến mục tiêu `price` giữa các nhóm của `drive-wheels` (`fwd`, `rwd`, `4wd`) và `make`.
   - Khi kiểm định tổng thể đạt mức ý nghĩa ($p < 0.05$), tiến hành kiểm định từng cặp nhóm con (ví dụ: `honda` vs `subaru`, `honda` vs `jaguar`) để xác định chính xác cặp nhóm nào tạo nên sự khác biệt thống kê.

- **Dữ liệu đầu vào (Input Artifacts)**: `datasets/processed/automobile_cleaned.csv` (Handoff H1).
- **Kết quả bàn giao (Output Artifacts)**:
  - Danh sách đặc trưng đã chọn lọc: `models/selected_features_h3.json` (Handoff H3).
  - Bảng tổng hợp thống kê & pivot: `reports/stats/eda_summary_tables.json` (Handoff H4).
  - Mã nguồn: `src/eda.py`.
  - Notebook: `notebooks/05_exploratory_data_analysis.ipynb`.
- **Công cụ cho phép (Allowed Tools)**: `pandas`, `numpy`, `scipy.stats` (`pearsonr`, `f_oneway`, `skew`, `kurtosis`), `statsmodels`.
- **Ràng buộc nghiêm ngặt (Strict Constraints)**:
  - *Báo cáo kép (Dual Reporting)*: Mọi kết luận kiểm định bắt buộc phải nêu cả trị thống kê ($r$ hoặc $F$) VÀ $p$-value.
  - *Ngưỡng bác bỏ $H_0$*: Không được đưa biến vào mô hình nếu $p \ge 0.05$ hoặc $|r| < 0.30$.
  - *Phân biệt Tương quan và Nhân quả*: Tuyệt đối không dùng cụm từ chỉ nguyên nhân - kết quả (causality) khi chỉ kiểm định tương quan thống kê (correlation).

---

### Role 3: Visualization Design Agent (Thiết kế Trực quan hóa Dữ liệu)

- **Mục tiêu học thuật**: Chuyển hóa dữ liệu và kết quả phân tích thành các đồ họa trực quan chuyên nghiệp, đúng chuẩn truyền thông khoa học dữ liệu, phục vụ người xem nắm bắt thông tin nhanh chóng và chính xác.
- **Ánh xạ bài giảng chính thức (`slide-study/`)**:
  - `Bai03_Truc_quan.pdf`: Kiến trúc 3 tầng của Matplotlib:
    1. *Backend Layer*: `FigureCanvas`, `Renderer`, `Event`.
    2. *Artist Layer*: Phân định Primitives (`Line2D`, `Rectangle`, `Circle`, `Polygon`, `Text`, `Patch`) và Containers (`Figure`, `Axes`, `Axis`, `Tick`).
    3. *Scripting Layer*: `matplotlib.pyplot` (chỉ dùng để tạo khung hoặc hiển thị chung; mọi xử lý vẽ phải dùng OO API).
    - 7 dạng đồ thị cơ sở: Line plot, Area plot, Histogram, Bar chart (đứng & ngang), Pie chart, Box plot, Scatter plot trên bộ dữ liệu `Canada.xlsx`.
  - `Bai04_Cong_cu_TQ.pdf`:
    - Quy trình 5 bước thiết kế trực quan:
      1. Làm rõ câu hỏi nghiên cứu (Clarify analytical question).
      2. Khám phá cấu trúc dữ liệu & phác thảo sơ bộ (Explore data & sketch).
      3. Xác định thông điệp trọng tâm (Identify core message).
      4. Chọn dạng biểu đồ chuẩn hóa phù hợp (Select chart type).
      5. Tinh chỉnh thị giác: màu sắc, kích thước font chữ, chú giải, nhãn tiếng Việt (Refine styling & labels).
    - Công cụ trực quan hóa nâng cao: Waffle Chart (`pywaffle`), Word Cloud (`wordcloud`), Seaborn đa biến (`regplot`, `residplot`, `kdeplot`, `jointplot`, `pairplot`).

#### Nhiệm vụ cụ thể (Detailed Responsibilities):
1. **Thực thi quy trình thiết kế 5 bước (Bai04)**:
   - Khảo sát bản chất biến số (liên tục/rời rạc, xu hướng/so sánh/phân phối/tương quan/tỉ trọng) trước khi chọn biểu đồ.
2. **Triển khai chuẩn Matplotlib Object-Oriented API & Cấu hình Font**:
   - Luôn sử dụng cú pháp hướng đối tượng: `fig, ax = plt.subplots(figsize=(10, 6))`.
   - Cấu hình hỗ trợ tiếng Việt trên Linux/WSL2 tránh lỗi font tofu:
     ```python
     import matplotlib.pyplot as plt
     plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Liberation Sans', 'Arial']
     plt.rcParams['axes.unicode_minus'] = False
     ```
   - Trực quan hóa xu hướng nhập cư Canada (1980 - 2013) cho Top 5 quốc gia bằng Line Plot và Stacked Area Plot.
   - Trực quan hóa phân phối `price` theo `drive-wheels` bằng Box Plot.
   - Vẽ Scatter Plot có đường xu hướng hồi quy biểu diễn tương quan giữa `engine-size` và `price`.
3. **Triển khai biểu đồ chuyên biệt nâng cao**:
   - *Waffle Chart*: Sử dụng `pywaffle` với `FigureClass=Waffle` hiển thị tỉ trọng đóng góp của các lục địa di dân hoặc phân khúc xe:
     ```python
     from pywaffle import Waffle
     fig = plt.figure(FigureClass=Waffle, rows=5, values=composition_dict, figsize=(11, 6))
     ```
   - *Word Cloud*: Sử dụng thư viện `wordcloud.WordCloud` kèm bộ từ dừng `STOPWORDS` trực quan hóa tần suất từ/quốc gia.
   - *Seaborn Multi-panel*: Xây dựng `sns.jointplot`, `sns.pairplot`, và KDE distribution so sánh $Y$ và $\hat{Y}$.
4. **Quy chuẩn xuất bản & Bố cục đồ họa**:
   - 100% biểu đồ có: Tiêu đề (`ax.set_title`), Nhãn trục $X$ có đơn vị tính (`ax.set_xlabel`), Nhãn trục $Y$ có đơn vị tính (`ax.set_ylabel`), và Chú giải (`ax.legend`).
   - Sử dụng `plt.tight_layout()` hoặc `constrained_layout=True`.
   - Xuất file chất lượng cao 300 DPI vào `reports/figures/*.png`.

- **Dữ liệu đầu vào (Input Artifacts)**: `datasets/processed/automobile_cleaned.csv`, `datasets/processed/canada_cleaned.csv`, `reports/stats/eda_summary_tables.json` (Handoff H4), `reports/diagnostics/model_diagnostics.npz` (Handoff H5).
- **Kết quả bàn giao (Output Artifacts)**:
  - Mã nguồn: `src/visualization.py`.
  - Notebooks: `notebooks/03_basic_visualization.ipynb`, `04_advanced_visualization.ipynb`.
  - Thư viện hình ảnh xuất bản: `reports/figures/*.png` (300 DPI).
- **Công cụ cho phép (Allowed Tools)**: `matplotlib`, `seaborn`, `pywaffle`, `wordcloud`, `dash`.
- **Ràng buộc nghiêm ngặt (Strict Constraints)**:
  - *Cấm tuyệt đối pyplot state-machine*: Bắt buộc dùng `fig, ax = plt.subplots()`. Không chấp nhận `plt.plot()`.
  - *Đầy đủ nhãn và đơn vị*: Không chấp nhận biểu đồ thiếu tiêu đề, nhãn trục, hoặc thiếu đơn vị đo lường.
  - *Màu sắc trợ năng (Color Accessibility)*: Ưu tiên bảng màu thân thiện người khiếm thị màu (`viridis`, `plasma`, `Set2`).

---

### Role 4: ML & Pipeline Modeling Agent (Mô hình hóa & Đánh giá Học máy)

- **Mục tiêu học thuật**: Xây dựng mô hình hồi quy giải thích và dự báo giá trị mục tiêu, áp dụng Scikit-Learn Pipeline chống rò rỉ dữ liệu, chẩn đoán phần dư theo 3 kịch bản, phát hiện hiện tượng Overfitting/Underfitting, và áp dụng kỹ thuật điều chuẩn Ridge với tinh chỉnh siêu tham số bằng Cross-Validation.
- **Ánh xạ bài giảng chính thức (`slide-study/`)**:
  - `Bai06_Mo_hinh.pdf`:
    - Hồi quy tuyến tính đơn biến (SLR): $Y = b_0 + b_1 X$.
    - Hồi quy tuyến tính đa biến (MLR): $Y = b_0 + b_1 X_1 + \dots + b_n X_n$.
    - Chẩn đoán trực quan 3 kịch bản Residual Plot (`sns.residplot`), Regression Plot (`sns.regplot`), Distribution Plot (`sns.kdeplot`).
    - Hồi quy đa thức (Polynomial Regression): `PolynomialFeatures(degree=d)`.
    - Scikit-Learn `Pipeline`: Tích hợp `StandardScaler` $\rightarrow$ `PolynomialFeatures` $\rightarrow$ `Ridge` / `LinearRegression`.
    - Thước đo in-sample: Sai số toàn phương trung bình (MSE) và Hệ số xác định $R^2$:
      $$R^2 = 1 - \frac{\text{MSE}_{\text{model}}}{\text{MSE}_{\text{mean}}} = 1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2}$$
  - `Bai07_Danh_gia_MH.pdf`:
    - Phân chia tập dữ liệu: `train_test_split(..., test_size=0.3, random_state=42)`.
    - Đánh giá chéo: $K$-Fold Cross Validation (`cross_val_score`, `cross_val_predict`) với $k=4$.
    - Chẩn đoán Underfitting vs Overfitting theo bậc đa thức (Train MSE vs Test MSE).
    - Hồi quy Ridge ($L_2$ Regularization): $\min \left\{ \text{MSE} + \alpha \sum w_j^2 \right\}$.
    - Tinh chỉnh siêu tham số $\alpha$ qua `GridSearchCV` với 2 dải giá trị chuẩn (rời rạc và logspace).

#### Nhiệm vụ cụ thể (Detailed Responsibilities):
1. **Huấn luyện mô hình cơ sở (SLR & MLR)**:
   - Xây dựng mô hình SLR trên thuộc tính có tương quan mạnh nhất (`engine-size`).
   - Xây dựng mô hình MLR trên tập đặc trưng được bàn giao từ Handoff H3 (`['horsepower', 'curb-weight', 'engine-size', 'highway-L/100km']`).
2. **Chẩn đoán mô hình trực quan theo 3 trường hợp Residual Plot (Bai06 p. 18-19)**:
   - Áp dụng `sns.residplot` và bắt buộc phân loại kết luận:
     - *Trường hợp 1 (Phần dư phân bố ngẫu nhiên đều quanh trục 0)*: Giả định tuyến tính thỏa mãn, mô hình tuyến tính phù hợp.
     - *Trường hợp 2 (Phần dư uốn lượn có dạng đường cong)*: Mối quan hệ thực tế là phi tuyến, bắt buộc dùng Hồi quy đa thức (Polynomial Regression).
     - *Trường hợp 3 (Phần dư loe rộng hình nón / Heteroscedasticity)*: Phương sai sai số không đồng nhất, mô hình tuyến tính không đáng tin cậy.
3. **Phân định rõ ranh giới đánh giá In-sample vs Out-of-sample**:
   - Sử dụng đánh giá in-sample ($R^2$, MSE) chỉ để chẩn đoán sơ bộ độ khớp ban đầu theo `Bai06`.
   - Mọi kết luận về hiệu năng và chọn lựa mô hình cuối cùng bắt buộc phải dựa trên out-of-sample metrics trên tập Test độc lập và Cross-Validation theo `Bai07`.
4. **Xây dựng Scikit-Learn Pipeline & Tinh chỉnh Ridge $\alpha$**:
   - Xây dựng Pipeline chống rò rỉ dữ liệu:
     ```python
     from sklearn.pipeline import Pipeline
     from sklearn.preprocessing import StandardScaler, PolynomialFeatures
     from sklearn.linear_model import Ridge

     pipe = Pipeline([
         ('scaler', StandardScaler()),
         ('poly', PolynomialFeatures(degree=2, include_bias=False)),
         ('ridge', Ridge(random_state=42))
     ])
     ```
   - Tinh chỉnh siêu tham số $\alpha$ bằng `GridSearchCV(pipe, param_grid, cv=4)` với 2 dải giá trị chuẩn của slide Bai07:
     - Dải rời rạc: `{'ridge__alpha': [0.001, 0.01, 0.1, 1, 10, 100, 1000]}`
     - Dải logspace liên tục: `{'ridge__alpha': np.logspace(-3, 4, 60)}`
   - Xuất khẩu mảng chẩn đoán serialized chuẩn sang đĩa theo Handoff H5.

- **Dữ liệu đầu vào (Input Artifacts)**: `datasets/processed/automobile_cleaned.csv`, `models/selected_features_h3.json`.
- **Kết quả bàn giao (Output Artifacts)**:
  - File đóng gói pipeline đã huấn luyện: `models/best_ridge_pipeline.joblib`.
  - Mảng dữ liệu chẩn đoán serialized: `reports/diagnostics/model_diagnostics.npz` (Handoff H5).
  - Metadata đánh giá mô hình: `reports/diagnostics/model_diagnostics_meta.json` (Handoff H5).
  - Mã nguồn: `src/models.py`.
  - Notebooks: `notebooks/06_model_development.ipynb`, `07_model_evaluation.ipynb`.
- **Công cụ cho phép (Allowed Tools)**: `scikit-learn`, `numpy`, `scipy`, `seaborn`, `joblib`.
- **Ràng buộc nghiêm ngặt (Strict Constraints)**:
  - *Không rò rỉ dữ liệu (Zero Data Leakage)*: Toàn bộ quá trình scale và tạo đa thức phải nằm bên trong `Pipeline` hoặc chỉ `fit` trên `X_train`.
  - *Cố định hạt giống ngẫu nhiên*: Bắt buộc đặt `random_state=42`.
  - *Quyết định dựa trên Out-of-sample*: Cấm chọn mô hình chỉ dựa trên Train $R^2$.

---

### Role 5: Academic Reviewer / QA Agent (Đánh giá Học thuật & Kiểm thử Tự động)

- **Mục tiêu học thuật**: Đóng vai trò là Trợ giảng và Chuyên gia Đảm bảo Chất lượng phần mềm học thuật, tiến hành kiểm tra toàn diện mã nguồn, tính đúng đắn của phương pháp thống kê, sự tuân thủ chuẩn đầu ra môn học IE313 theo thang đo Bloom, và đảm bảo 100% tính tái lập độc lập.
- **Ánh xạ bài giảng chính thức (`slide-study/`)**:
  - Chuẩn đầu ra môn học IE313 (ThS. Phạm Thế Sơn - UIT).
  - Kiểm tra thang đo Bloom:
    - *Remember & Understand*: Giải thích rõ ràng khái niệm trong docstring và markdown notebook.
    - *Apply*: Ứng dụng chính xác các hàm thư viện Pandas, Matplotlib, Scipy, Scikit-Learn.
    - *Analyze*: Phân tích thống kê đúng đắn, không ngụy biện thống kê.
    - *Evaluate*: Đánh giá mô hình khách quan dựa trên tập kiểm thử độc lập và kiểm định chéo.
  - Chuẩn mực mã nguồn: PEP 8, Ruff static analysis, Pytest unit tests, Headless execution (`jupyter nbconvert`).

#### Nhiệm vụ cụ thể (Detailed Responsibilities):
1. **Kiểm tra tuân thủ quy trình khoa học dữ liệu**:
   - Đối chiếu toàn bộ bài làm với quy trình 6 bước chuẩn (Ingestion $\rightarrow$ Wrangling $\rightarrow$ EDA $\rightarrow$ Visualization $\rightarrow$ Modeling $\rightarrow$ Evaluation).
   - Kiểm tra tính đầy đủ của các notebook từ `00_` đến `07_`.
2. **Xây dựng & Thực thi bộ kiểm thử tự động (Unit Tests)**:
   - Viết và chạy các bài kiểm tra trong thư mục `tests/`:
     - `tests/test_wrangling.py`: Kiểm tra không còn giá trị null ở biến mục tiêu, các cột số có đúng kiểu `float/int`, giá trị Min-Max nằm trong $[0, 1]$, Z-score có trung bình xấp xỉ 0.
     - `tests/test_eda.py`: Kiểm tra hệ số Pearson thỏa mãn $-1 \le r \le 1$, $p$-value thỏa mãn $0 \le p \le 1$, kết quả ANOVA trả về $F \ge 0$.
     - `tests/test_models.py`: Kiểm tra pipeline có thể dự báo với dữ liệu mới, MSE $> 0$, và $R^2 \le 1.0$.
3. **Hai chế độ vận hành (Two Operating Modes)**:
   - *Mode A (Execution Harness - Claude Code, Cursor Agent, Terminal)*: Trực tiếp chạy `pytest tests/`, `ruff check .`, và `jupyter nbconvert`. Ghi lại stderr/stdout và kiểm tra mã thoát.
   - *Mode B (Chat / Generator - ChatGPT, Gemini Studio, Copilot)*: Sinh toàn bộ mã nguồn file test hoàn chỉnh (`tests/test_*.py`) và script shell kiểm tra tự động để người dùng tự thực thi.
4. **Kiểm tra tính bất biến của dữ liệu thô**:
   - Kiểm tra mã băm SHA-256 hoặc `git status` của thư mục `datasets/raw/` để đảm bảo dữ liệu gốc hoàn toàn nguyên vẹn.

- **Dữ liệu đầu vào (Input Artifacts)**: Toàn bộ repository (`src/*.py`, `notebooks/*.ipynb`, `datasets/`, `reports/figures/`, `tests/*.py`).
- **Kết quả bàn giao (Output Artifacts)**:
  - Bộ kiểm thử hoàn chỉnh: `tests/test_wrangling.py`, `tests/test_eda.py`, `tests/test_models.py`, `tests/conftest.py`.
  - Báo cáo đánh giá chất lượng học thuật: `reports/qa_audit_report.md` (Handoff H6).
- **Công cụ cho phép (Allowed Tools)**: `pytest`, `pytest-cov`, `ruff`, `jupyter nbconvert`, `git`.
- **Ràng buộc nghiêm ngặt (Strict Constraints)**:
  - *Không có cell lỗi*: Mọi notebook phải chạy trơn tru từ đầu đến cuối mà không sinh exception.
  - *Bảo toàn dữ liệu thô tuyệt đối*: Nếu phát hiện bất kỳ file nào trong `datasets/raw/` bị sửa đổi, bài làm bị đánh giá không đạt (Fail).
  - *Ruff Clean*: Không còn lỗi linting nghiêm trọng trước khi nghiệm thu.

---

## 3. Giao Thức Bàn Giao & Hợp Đồng Dữ Liệu (Inter-Agent Handoff Protocols & Data Contracts)

### 3.1 Danh Mục Bàn Giao & Vị Trí File Chuẩn (Standard Handoff Artifact Manifest)

Nhằm đảm bảo tính tương thích tuyệt đối giữa các mô hình AI khác nhau (kể cả các mô hình không chia sẻ bộ nhớ RAM), toàn bộ dữ liệu bàn giao **BẮT BUỘC PHẢI ĐƯỢC SERIALIZE RA FILE TRÊN ĐĨA** tại các đường dẫn cố định dưới đây:

| Mã Hợp Đồng | Tác Tử Bàn Giao (Producer) | Tác Tử Nhận (Consumer) | File Dữ Liệu Trên Đĩa (Primary Artifact) | File Metadata Hợp Đồng (Contract JSON) | Tiêu Chí Nghiệm Thu (Validation Criteria) |
|---|---|---|---|---|---|
| **H1: Clean Automobile** | Ingestion & Wrangling | EDA & Statistical Testing | `datasets/processed/automobile_cleaned.csv` | `datasets/processed/automobile_cleaned_meta.json` | - Cột `price` có 0 giá trị null<br>- Không còn ký tự `'?'`<br>- 28 cột chuẩn (kèm `city-L/100km`, `highway-L/100km`)<br>- Kiểu dữ liệu số là `float64`/`int64` |
| **H2: Clean Canada** | Ingestion & Wrangling | Visualization Design | `datasets/processed/canada_cleaned.csv` | `datasets/processed/canada_cleaned_meta.json` | - Ingestion đúng tham số (`skiprows=20`, `skipfooter=2`)<br>- Sẵn sàng cho Line/Area/Waffle chart |
| **H3: Feature Selection** | EDA & Statistical Testing | ML & Pipeline Modeling | `models/selected_features_h3.json` | *(Bản thân file JSON là hợp đồng)* | - Đặc trưng liên tục có $|r| \ge 0.30$ và $p < 0.05$<br>- Đặc trưng phân loại có ANOVA $p < 0.05$ |
| **H4: Aggregated Stats** | EDA & Statistical Testing | Visualization Design | `reports/stats/eda_summary_tables.json` | *(Bản thân file JSON là hợp đồng)* | - Bảng pivot và ngưỡng $1.5 \times IQR$ phục vụ Box plot, Heatmap, PairPlot |
| **H5: Model Diagnostics** | ML & Pipeline Modeling | Visualization Design | `reports/diagnostics/model_diagnostics.npz` | `reports/diagnostics/model_diagnostics_meta.json` | - File `.npz` chứa mảng `y_test_actual`, `y_test_predicted`, `residuals`<br>- Metadata ghi nhận 3 kịch bản residual plot |
| **H6: Full Repo QA State** | Toàn bộ các Tác tử | Academic Reviewer / QA | Toàn bộ repo (`src/`, `notebooks/`, `tests/`) | `reports/qa_audit_report.md` | - `pytest` vượt qua 100%<br>- `ruff check .` không lỗi<br>- `jupyter nbconvert` không sinh lỗi runtime |

### 3.2 Chi Tiết Hợp Đồng & Định Dạng Schema (Detailed Data Contracts & Metadata Schemas)

#### Hợp đồng H1: Metadata File `datasets/processed/automobile_cleaned_meta.json`
```json
{
  "contract_id": "H1_CLEAN_DATA",
  "source_file": "datasets/raw/imports-85.data",
  "output_file": "datasets/processed/automobile_cleaned.csv",
  "num_rows_initial": 205,
  "num_rows_cleaned": 201,
  "dropped_rows_reason": "Missing target value in column 'price' (4 rows dropped)",
  "total_columns": 28,
  "retained_original_mpg_columns": true,
  "imputed_features": {
    "normalized-losses": {"strategy": "mean", "imputed_value": 122.0},
    "bore": {"strategy": "mean", "imputed_value": 3.33},
    "stroke": {"strategy": "mean", "imputed_value": 3.25},
    "horsepower": {"strategy": "median", "imputed_value": 95.0},
    "peak-rpm": {"strategy": "median", "imputed_value": 5200.0},
    "num-of-doors": {"strategy": "mode", "imputed_value": "four"}
  },
  "knn_imputed_features": [],
  "unit_conversions": [
    {"from": "city-mpg", "to": "city-L/100km", "formula": "235 / city-mpg"},
    {"from": "highway-mpg", "to": "highway-L/100km", "formula": "235 / highway-mpg"}
  ],
  "scaling_applied": {
    "length": {"method": "min_max", "range": [0, 1]},
    "width": {"method": "min_max", "range": [0, 1]},
    "height": {"method": "min_max", "range": [0, 1]}
  },
  "target_column": "price",
  "target_null_count": 0
}
```

#### Hợp đồng H3: Metadata File `models/selected_features_h3.json`
```json
{
  "contract_id": "H3_FEATURE_SELECTION",
  "significance_threshold_alpha": 0.05,
  "correlation_threshold_abs_r": 0.30,
  "target_variable": "price",
  "selected_continuous_features": [
    {"feature": "engine-size", "pearson_r": 0.872, "p_value": 1.98e-63, "strength": "Strong"},
    {"feature": "curb-weight", "pearson_r": 0.834, "p_value": 2.18e-53, "strength": "Strong"},
    {"feature": "horsepower", "pearson_r": 0.809, "p_value": 6.36e-48, "strength": "Strong"},
    {"feature": "city-L/100km", "pearson_r": 0.789, "p_value": 1.05e-44, "strength": "Strong"},
    {"feature": "highway-L/100km", "pearson_r": 0.801, "p_value": 1.54e-46, "strength": "Strong"},
    {"feature": "wheel-base", "pearson_r": 0.584, "p_value": 8.08e-20, "strength": "Moderate"},
    {"feature": "bore", "pearson_r": 0.543, "p_value": 8.05e-17, "strength": "Moderate"}
  ],
  "rejected_continuous_features": [
    {"feature": "peak-rpm", "pearson_r": -0.101, "p_value": 0.151, "reason": "p_value >= 0.05"},
    {"feature": "stroke", "pearson_r": 0.082, "p_value": 0.245, "reason": "Weak correlation and p_value >= 0.05"}
  ],
  "selected_categorical_features_anova": [
    {"feature": "drive-wheels", "f_score": 67.95, "p_value": 3.39e-23, "significant": true},
    {"feature": "engine-location", "f_score": 24.58, "p_value": 1.45e-6, "significant": true}
  ],
  "pairwise_subgroup_anova": [
    {"pair": ["fwd", "rwd"], "f_score": 130.5, "p_value": 1.2e-22, "significant": true},
    {"pair": ["4wd", "rwd"], "f_score": 28.3, "p_value": 2.1e-6, "significant": true},
    {"pair": ["4wd", "fwd"], "f_score": 0.65, "p_value": 0.422, "significant": false}
  ]
}
```

#### Hợp đồng H5: Serialization Mảng Chẩn Đoán và Metadata
Để tránh phụ thuộc vào bộ nhớ RAM giữa các tiến trình hoặc các session AI riêng biệt, Tác tử Modeling bắt buộc lưu hai file sau:

1. File mảng nhị phân nén: `reports/diagnostics/model_diagnostics.npz`:
```python
import numpy as np

# Serialize numpy arrays directly to disk
np.savez_compressed(
    "reports/diagnostics/model_diagnostics.npz",
    y_test_actual=y_test.to_numpy(),
    y_test_predicted=y_pred_test,
    residuals=(y_test - y_pred_test).to_numpy()
)
```

2. File metadata: `reports/diagnostics/model_diagnostics_meta.json`:
```json
{
  "contract_id": "H5_MODEL_DIAGNOSTICS",
  "model_name": "Ridge_Polynomial_Pipeline_Degree2",
  "pipeline_file": "models/best_ridge_pipeline.joblib",
  "diagnostics_array_file": "reports/diagnostics/model_diagnostics.npz",
  "ridge_best_alpha": 0.1,
  "hyperparameter_search_grid": "discrete [0.001, 0.01, ..., 1000] and logspace(-3, 4, 60)",
  "metrics": {
    "train_mse": 5821034.12,
    "test_mse": 7104921.45,
    "train_r2": 0.892,
    "test_r2": 0.865,
    "cv_4fold_r2_mean": 0.854,
    "cv_4fold_r2_std": 0.038
  },
  "residual_diagnostics": {
    "observed_pattern": "Case 1: Random scatter around 0 axis",
    "conclusion": "Linear/Polynomial model assumption is satisfied; no severe heteroscedasticity."
  }
}
```

---

## 4. Mẫu Prompt Sẵn Sàng Thực Thi (Ready-to-Use Agent Dispatch Prompt Templates)

Mỗi mẫu prompt dưới đây được trang bị **Khung Thích Ứng Môi Trường (Environment Adaptation Notice)** và **Đặc Tả Tự Đầy Đủ (Self-Contained Executive Specification)**, cho phép người dùng copy-paste và chạy thành công trên cả môi trường có quyền truy cập filesystem (Claude Code, Cursor Composer, Aider) lẫn các cửa sổ chat độc lập không có file upload (ChatGPT, Gemini Studio).

---

### 4.1 Dispatch Prompt: Data Ingestion & Wrangling Agent

```markdown
You are acting as the **Data Ingestion & Wrangling Agent** for course **IE313 - Data Analysis and Visualization (UIT - VNU-HCM)**, instructed by ThS. Phạm Thế Sơn.

### ENVIRONMENT ADAPTATION NOTICE:
- If running with Workspace access (Claude Code, Cursor Composer, Aider, Copilot @workspace):
  Inspect `CLAUDE.md` and `AGENTS.md` directly.
- If running in Web / Chat-only mode (ChatGPT, Gemini Studio):
  The operational constraints, data paths, and schema rules specified below are self-contained and authoritative.
- If running without terminal execution capabilities:
  Generate complete, production-ready Python files and test scripts instead of attempting to run shell commands.

### CONTEXT & KNOWLEDGE BASE:
- Refer to `slide-study/Bai_Giang_TH_01_Python_for_DA.pdf`, `slide-study/Bai01_Gioi_thieu_PTDL-Nhap_Xuat_Bo_du_lieu.pdf`, and `slide-study/Bai02_Sap_xep_DL.pdf`.
- Primary datasets: `datasets/raw/imports-85.data` (Automobile) and `datasets/raw/Canada.xlsx` (UN Migration).

### OBJECTIVES & MATHEMATICAL FORMULAS:
1. Ingest `datasets/raw/imports-85.data` and assign 26 standard headers:
   ['symboling', 'normalized-losses', 'make', 'fuel-type', 'aspiration', 'num-of-doors', 'body-style', 'drive-wheels', 'engine-location', 'wheel-base', 'length', 'width', 'height', 'curb-weight', 'engine-type', 'num-of-cylinders', 'engine-size', 'fuel-system', 'bore', 'stroke', 'compression-ratio', 'horsepower', 'peak-rpm', 'city-mpg', 'highway-mpg', 'price']
2. Ingest `datasets/raw/Canada.xlsx` using:
   `pd.read_excel('datasets/raw/Canada.xlsx', sheet_name='Canada by Citizenship', skiprows=range(20), skipfooter=2)`.
3. Replace all '?' values with `np.nan`.
4. Drop rows missing the target variable `price`: `df.dropna(subset=['price'], axis=0, inplace=True)`.
5. Missing data strategy (Bai02):
   - Normal continuous ('normalized-losses', 'bore', 'stroke'): Impute with mean.
   - Skewed continuous ('horsepower', 'peak-rpm'): Impute with median.
   - Categorical ('num-of-doors'): Impute with mode (`df['num-of-doors'].mode()[0]`).
   - Complex numerical: Support `sklearn.impute.KNNImputer(n_neighbors=5, weights='distance')`.
6. Unit conversion (Bai02 p. 13):
   - Add `city-L/100km` via formula: 235 / city-mpg.
   - Add `highway-L/100km` via formula: 235 / highway-mpg.
   - Retain original `city-mpg` and `highway-mpg` columns (resulting in 28 total columns).
7. Feature Scaling (Bai02):
   - Simple Feature Scaling: x_new = x / x.max()
   - Min-Max Scaling on 'length', 'width', 'height': x_new = (x - x.min()) / (x.max() - x.min())
   - Z-score Standardization: x_new = (x - mu) / sigma
8. Binning: Equal-width bins for 'price' into 3 categories: ['Low', 'Medium', 'High'] via `pd.cut()` and `np.linspace()`.
9. Dummy encoding: `pd.get_dummies(df, columns=['fuel-type', 'aspiration'], drop_first=True, dtype=int)`.
10. Export cleaned datasets and contract:
    - `datasets/processed/automobile_cleaned.csv`
    - `datasets/processed/automobile_cleaned_meta.json` (Handoff H1)
    - `datasets/processed/canada_cleaned.csv` (Handoff H2)

### STRICT CONSTRAINTS:
- NEVER overwrite or mutate files in `datasets/raw/`.
- Continuous features must not retain 'object' dtype.
- Code must be in `src/ingestion.py` and `src/wrangling.py`, documented in notebooks `01_` and `02_`.
- Identifiers in English; docstrings and markdown explanations in Vietnamese.
```

---

### 4.2 Dispatch Prompt: EDA & Statistical Testing Agent

```markdown
You are acting as the **EDA & Statistical Testing Agent** for course **IE313 - Data Analysis and Visualization (UIT - VNU-HCM)**, instructed by ThS. Phạm Thế Sơn.

### ENVIRONMENT ADAPTATION NOTICE:
- If running with Workspace access (Claude Code, Cursor Composer, Aider, Copilot @workspace):
  Inspect `CLAUDE.md` and `AGENTS.md` directly.
- If running in Web / Chat-only mode (ChatGPT, Gemini Studio):
  The operational constraints, data paths, and schema rules specified below are self-contained and authoritative.
- If running without terminal execution capabilities:
  Generate complete, production-ready Python files and test scripts instead of attempting to run shell commands.

### CONTEXT & KNOWLEDGE BASE:
- Refer to `slide-study/Bai05_PT_Tham_do.pdf`.
- Input data: `datasets/processed/automobile_cleaned.csv` (provided under Handoff H1).

### OBJECTIVES & STATISTICAL METRICS:
1. Compute descriptive statistics for all continuous variables: Mean, Median, Mode, Range, Quartiles, $IQR = Q_3 - Q_1$, Std ($s$).
2. Compute Coefficient of Variation: $CV = (s / \bar{x}) \times 100\%$ for relative dispersion.
3. Compute distribution shape: Skewness (`scipy.stats.skew`) and Kurtosis (`scipy.stats.kurtosis`).
4. Identify outliers using the $1.5 \times IQR$ rule: Lower Bound $Q_1 - 1.5 \times IQR$, Upper Bound $Q_3 + 1.5 \times IQR$.
5. Conduct Pearson correlation testing (`scipy.stats.pearsonr`) against target 'price'.
   - Selection rule (Bai05 p. 37): Select features with $|r| \ge 0.30$ and $p < 0.05$.
   - Reject features with $p \ge 0.05$ or $|r| < 0.30$.
6. Perform groupby aggregations and construct pivot tables for 'drive-wheels' and 'body-style' against 'price'.
7. Conduct One-way ANOVA $F$-tests (`scipy.stats.f_oneway`):
   $$F = \frac{\text{Variation between group means}}{\text{Variation within group}}$$
8. When omnibus ANOVA is significant ($p < 0.05$), conduct Pairwise Subgroup ANOVA tests (e.g., 'fwd' vs 'rwd', '4wd' vs 'rwd') to isolate significant group differences.
9. Serialize artifacts:
   - Feature selection contract: `models/selected_features_h3.json` (Handoff H3)
   - Summary and pivot tables: `reports/stats/eda_summary_tables.json` (Handoff H4)

### STRICT CONSTRAINTS:
- DUAL REPORTING MANDATORY: Every test must report both the test statistic ($r$ or $F$) AND exact $p$-value.
- Do NOT claim a feature is predictive if $p \ge 0.05$.
- Strictly maintain the distinction: Correlation does not imply Causation.
- Code in `src/eda.py` and notebook `notebooks/05_exploratory_data_analysis.ipynb`.
```

---

### 4.3 Dispatch Prompt: Visualization Design Agent

```markdown
You are acting as the **Visualization Design Agent** for course **IE313 - Data Analysis and Visualization (UIT - VNU-HCM)**, instructed by ThS. Phạm Thế Sơn.

### ENVIRONMENT ADAPTATION NOTICE:
- If running with Workspace access (Claude Code, Cursor Composer, Aider, Copilot @workspace):
  Inspect `CLAUDE.md` and `AGENTS.md` directly.
- If running in Web / Chat-only mode (ChatGPT, Gemini Studio):
  The operational constraints, data paths, and schema rules specified below are self-contained and authoritative.
- If running without terminal execution capabilities:
  Generate complete, production-ready Python files and test scripts instead of attempting to run shell commands.

### CONTEXT & KNOWLEDGE BASE:
- Refer to `slide-study/Bai03_Truc_quan.pdf` and `slide-study/Bai04_Cong_cu_TQ.pdf`.
- Inputs: `datasets/processed/automobile_cleaned.csv`, `datasets/processed/canada_cleaned.csv`, `reports/stats/eda_summary_tables.json`, and `reports/diagnostics/model_diagnostics.npz`.

### OBJECTIVES & 5-STEP DESIGN PROCESS (Bai04):
1. Execute the 5-step process: Clarify question -> Explore data -> Define message -> Select chart -> Refine styling.
2. Configure Matplotlib Vietnamese Unicode font rendering (Linux / WSL2):
   ```python
   import matplotlib.pyplot as plt
   plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Liberation Sans', 'Arial']
   plt.rcParams['axes.unicode_minus'] = False
   ```
3. Implement charts strictly using the Matplotlib Object-Oriented (OO) API (`fig, ax = plt.subplots(...)`):
   - Multi-series Line Plot and Stacked Area Plot for Canada immigration trends (Top 5 countries, 1980-2013).
   - Comparative Box Plots for 'price' across 'drive-wheels' categories.
   - Scatter Plot with linear regression line for 'engine-size' vs 'price'.
4. Implement specialized advanced charts:
   - Waffle Chart using `pywaffle` (`FigureClass=Waffle`) for composition analysis.
   - Word Cloud using `wordcloud.WordCloud` with `STOPWORDS`.
   - Seaborn multi-panel figures: KDE distribution curves, `sns.jointplot`, `sns.pairplot`.
5. Visual Model Diagnostics: Load `reports/diagnostics/model_diagnostics.npz` and plot:
   - Residual Plot (`sns.residplot`) verifying homoscedasticity.
   - Distribution comparison plot (`sns.kdeplot`) comparing actual test prices vs predicted prices.
6. Export all figures at 300 DPI into `reports/figures/*.png`.

### STRICT CONSTRAINTS:
- NEVER use state-machine `plt.plot()` shortcuts in production code. Always use `fig, ax = plt.subplots()`.
- Every chart MUST have: `ax.set_title()`, `ax.set_xlabel()` with unit, `ax.set_ylabel()` with unit, and `ax.legend()`.
- Apply `plt.tight_layout()` to avoid text clipping.
- Code in `src/visualization.py`, notebooks `notebooks/03_` and `notebooks/04_`.
```

---

### 4.4 Dispatch Prompt: ML & Pipeline Modeling Agent

```markdown
You are acting as the **ML & Pipeline Modeling Agent** for course **IE313 - Data Analysis and Visualization (UIT - VNU-HCM)**, instructed by ThS. Phạm Thế Sơn.

### ENVIRONMENT ADAPTATION NOTICE:
- If running with Workspace access (Claude Code, Cursor Composer, Aider, Copilot @workspace):
  Inspect `CLAUDE.md` and `AGENTS.md` directly.
- If running in Web / Chat-only mode (ChatGPT, Gemini Studio):
  The operational constraints, data paths, and schema rules specified below are self-contained and authoritative.
- If running without terminal execution capabilities:
  Generate complete, production-ready Python files and test scripts instead of attempting to run shell commands.

### CONTEXT & KNOWLEDGE BASE:
- Refer to `slide-study/Bai06_Mo_hinh.pdf` and `slide-study/Bai07_Danh_gia_MH.pdf`.
- Inputs: `datasets/processed/automobile_cleaned.csv` and `models/selected_features_h3.json`.

### OBJECTIVES & MATHEMATICAL FORMULATIONS:
1. Split dataset with pinned seed: `train_test_split(X, y, test_size=0.3, random_state=42)`.
2. Fit baseline Simple Linear Regression (SLR): $Y = b_0 + b_1 X$.
3. Fit Multiple Linear Regression (MLR): $Y = b_0 + b_1 X_1 + \dots + b_n X_n$ on features from Handoff H3.
4. Diagnose models using Residual Plots (`sns.residplot`) and classify under 3 cases (Bai06 p. 18-19):
   - Case 1: Random scatter around 0 -> Linear model appropriate.
   - Case 2: Curved non-linear shape -> Must use Polynomial Regression.
   - Case 3: Funnel / expanding cone (Heteroscedasticity) -> Non-constant error variance, linear model unreliable.
5. In-sample vs Out-of-sample boundary:
   - In-sample $R^2 = 1 - \frac{\text{MSE}_{\text{model}}}{\text{MSE}_{\text{mean}}}$ and MSE used for initial fit diagnosis only (Bai06).
   - Final model selection MUST rely on Out-of-sample Test MSE and 4-Fold Cross Validation $R^2$ (Bai07).
6. Build Scikit-Learn `Pipeline` (Zero Data Leakage):
   ```python
   from sklearn.pipeline import Pipeline
   from sklearn.preprocessing import StandardScaler, PolynomialFeatures
   from sklearn.linear_model import Ridge

   pipe = Pipeline([
       ('scaler', StandardScaler()),
       ('poly', PolynomialFeatures(degree=2, include_bias=False)),
       ('ridge', Ridge(random_state=42))
   ])
   ```
7. Hyperparameter tuning for Ridge $\alpha$ using `GridSearchCV(pipe, param_grid, cv=4)`:
   - Discrete search grid: `{'ridge__alpha': [0.001, 0.01, 0.1, 1, 10, 100, 1000]}`
   - Continuous search space: `{'ridge__alpha': np.logspace(-3, 4, 60)}`
8. Serialize outputs to disk (Handoff H5):
   - Model pipeline: `models/best_ridge_pipeline.joblib`
   - Diagnostic arrays: `reports/diagnostics/model_diagnostics.npz` (keys: `y_test_actual`, `y_test_predicted`, `residuals`)
   - Evaluation metadata: `reports/diagnostics/model_diagnostics_meta.json`

### STRICT CONSTRAINTS:
- ZERO DATA LEAKAGE: Scalers and PolynomialFeatures must be fitted strictly inside the Pipeline or on X_train only.
- REPRODUCIBILITY: Always pass `random_state=42`.
- Code in `src/models.py`, notebooks `notebooks/06_` and `notebooks/07_`.
```

---

### 4.5 Dispatch Prompt: Academic Reviewer / QA Agent

```markdown
You are acting as the **Academic Reviewer / QA Agent** for course **IE313 - Data Analysis and Visualization (UIT - VNU-HCM)**, instructed by ThS. Phạm Thế Sơn.

### ENVIRONMENT ADAPTATION NOTICE:
- If running in **Mode A (Execution Harness - Claude Code, Cursor Agent, Terminal)**:
  Directly execute shell verification commands, inspect stderr/stdout, check exit codes, and generate audit reports.
- If running in **Mode B (Chat / Generator - ChatGPT, Gemini Studio, Copilot)**:
  Generate complete, production-ready test suites (`tests/test_*.py`) and verification scripts for the user to execute locally.

### CONTEXT & KNOWLEDGE BASE:
- Course syllabus: IE313 (UIT - VNU-HCM).
- Knowledge base: `slide-study/` (8 PDF lecture slide packages).
- Companion governance: `CLAUDE.md` and `AGENTS.md` (Role 5).

### OBJECTIVES & AUDIT CHECKLIST:
1. Verify adherence to the 6-stage Data Science pipeline: Ingestion -> Wrangling -> EDA -> Visualization -> Modeling -> Evaluation.
2. Implement and execute unit test suites in `tests/`:
   - `tests/test_wrangling.py`: Verify null imputation, non-null price, 28 columns, scaling bounds [0, 1], dummy columns.
   - `tests/test_eda.py`: Verify Pearson $r \in [-1, 1]$, $p$-value $\in [0, 1]$, ANOVA $F \ge 0$, and $|r| \ge 0.30$ filtering.
   - `tests/test_models.py`: Verify pipeline fit/predict interface, zero data leakage, MSE $> 0$, and $R^2 \le 1.0$.
3. Headless automated notebook execution:
   `jupyter nbconvert --to notebook --execute notebooks/*.ipynb`
   Verify ZERO runtime errors.
4. Static code analysis: Run `ruff check .` and `ruff format --check .` for PEP 8 compliance.
5. Audit Raw Data Immutability: Verify files in `datasets/raw/` have not been altered (check Git status or SHA-256).
6. Generate the comprehensive audit report: `reports/qa_audit_report.md` (Handoff H6).

### STRICT CONSTRAINTS:
- Zero tolerance for broken notebook cells or unhandled exceptions.
- Immediate failure if any file in `datasets/raw/` is modified.
- All tests must pass with clean green status (`pytest tests/ -v`).
```

---

## 5. Chỉ Dẫn Tích Hợp Đa Nền Tảng AI (Multi-AI Platform Directives)

---

### 5.1 Claude Code (CLI Subagents & Turn Control)
Khi sử dụng Claude Code trong terminal, người dùng có thể kích hoạt từng vai trò thông qua câu lệnh:

```bash
# 1. Kích hoạt Data Wrangling Subagent
claude "Act as the Data Ingestion & Wrangling Agent defined in AGENTS.md. Process datasets/raw/imports-85.data following Bai 01 and Bai 02."

# 2. Điều phối song song qua prompt phân tách
claude "Act as EDA Agent to calculate Pearson correlations in src/eda.py, while ensuring Visualization Agent generates reports/figures/correlation_heatmap.png adhering to Matplotlib OO API."

# 3. Kích hoạt QA Audit Subagent trước khi nộp bài
claude "Act as Academic Reviewer / QA Agent. Run pytest tests/, ruff check ., and headless jupyter nbconvert on all notebooks. Generate the audit report."
```

---

### 5.2 OpenAI ChatGPT & Codex (GPT-4o, o1, o3-mini)

1. **Phân định rõ khả năng của Mô hình Suy Luận (o1 / o3-mini) và Mô hình Sinh Mã (GPT-4o)**:
   - Các mô hình suy luận (`o1`, `o3-mini`) xuất sắc trong việc phân tích toán học, chứng minh công thức ANOVA $F$-test, và thiết kế không gian siêu tham số `GridSearchCV`. Tuy nhiên, trong giao diện web/API chuẩn, chúng không hỗ trợ gọi công cụ shell hoặc ghi đĩa tự động.
   - Sử dụng `o1` / `o3-mini` để tạo logic thuật toán phức tạp (Mode B), sau đó chuyển mã nguồn sang terminal hoặc Claude Code để thực thi (Mode A).
2. **Cách ly đường dẫn trong Sandbox ChatGPT Advanced Data Analysis**:
   - Trong môi trường Code Interpreter của ChatGPT, các đường dẫn cục bộ như `datasets/raw/imports-85.data` không tồn tại. Khi tải file lên ChatGPT, file sẽ nằm ở thư mục hiện tại `./` hoặc `/mnt/data/`. Script cần được cấu hình linh hoạt:
     ```python
     import os
     data_path = 'datasets/raw/imports-85.data' if os.path.exists('datasets/raw/imports-85.data') else 'imports-85.data'
     ```
3. **Ngăn chặn thói quen dùng `plt.plot()` trong GPT-4o**:
   - GPT-4o thường có xu hướng sinh mã `plt.plot()` theo thói quen mặc định. Luôn kèm theo yêu cầu bắt buộc: *"Strictly use `fig, ax = plt.subplots()`. Reject `plt.plot()`. Configure font for Vietnamese support."*

---

### 5.3 Cursor AI & Windsurf (Modern `.cursor/rules/*.mdc` Architecture)

Các phiên bản hiện đại của Cursor (v0.42+) đã chuyển đổi từ tệp `.cursorrules` đơn lẻ sang cấu trúc phân tán `.cursor/rules/*.mdc` với YAML frontmatter. Repository này cung cấp cấu hình chuẩn hóa:

1. Tạo file `.cursor/rules/ie313-core.mdc`:
```markdown
---
description: IE313 Course Rules and Multi-Agent Invariants
globs: ["src/**/*.py", "notebooks/**/*.ipynb", "tests/**/*.py"]
alwaysApply: true
---
# IE313 Course Operational Rules (UIT - VNU-HCM)
- Reference: AGENTS.md and CLAUDE.md.
- Strict Matplotlib OO API: Always use `fig, ax = plt.subplots()`. Reject `plt.plot()`, `plt.title()`, `plt.xlabel()`.
- Vietnamese Font Rendering: Configure `plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Liberation Sans', 'Arial']`.
- Data Leakage Prevention: Transformers and scalers must reside inside `sklearn.pipeline.Pipeline`.
- Reproducibility: Always pass `random_state=42` in `train_test_split`, `KFold`, and stochastic estimators.
- Raw Data Immutability: NEVER modify or write to `datasets/raw/**`.
- Language Boundary: English for identifiers and code; Vietnamese for docstrings, markdown explanations, and axis/chart labels.
```

2. Tạo file `.cursorignore` để bảo vệ dữ liệu thô tuyệt đối:
```
datasets/raw/**
.venv/**
__pycache__/**
.pytest_cache/**
.ruff_cache/**
```

---

### 5.4 GitHub Copilot (`.github/copilot-instructions.md`)

Tạo file `.github/copilot-instructions.md` ngắn gọn, tối ưu ngân sách token của Copilot Chat và gợi ý inline completion:

```markdown
# GitHub Copilot Instructions for IE313 (UIT - VNU-HCM)
- Course: IE313 - Data Analysis and Visualization (ThS. Phạm Thế Sơn).
- Strict Matplotlib OO API: Do not suggest `plt.plot()`, `plt.title()`, or `plt.xlabel()`. Always suggest `fig, ax = plt.subplots()` followed by `ax.set_*()`.
- Vietnamese Font Support: Use `plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Liberation Sans', 'Arial']` and `plt.rcParams['axes.unicode_minus'] = False`.
- Zero Data Leakage: Combine `StandardScaler()`, `PolynomialFeatures()`, and estimator inside `sklearn.pipeline.Pipeline`.
- Reproducibility: Always pin `random_state=42` in `train_test_split`, `KFold`, and estimators.
- Statistical Rigor: Report dual test statistics ($r$ or $F$) with exact $p$-values ($\alpha = 0.05$).
- Raw Data Immutability: Never modify files under `datasets/raw/`.
- Bilingual Rule: Code identifiers in English; docstrings, markdown, and chart labels in Vietnamese.
```

---

### 5.5 Google Gemini 2.0 (Pro / Flash / Code Assist)

1. **Khai thác Context Window 1M - 2M Tokens**:
   - Tải lên trực tiếp cả 8 file PDF trong `slide-study/` vào Context Window trong Google AI Studio để Gemini trích xuất chính xác công thức từ bài giảng của ThS. Phạm Thế Sơn.
2. **Khắc phục hiện tượng lược bỏ mã nguồn (Code Elision) trong bản Flash**:
   - Gemini 2.0 Flash có thể rút gọn mã nguồn thành `# ... existing code ...`. Khi ra lệnh cho Role 1 (Wrangling), bắt buộc thêm: *"Do NOT elide or omit code. Output the complete 26-column list and full transformation logic."*
3. **Cấu hình Font Tiếng Việt**:
   - Đảm bảo Gemini luôn chèn cấu hình font sans-serif vào các đoạn mã vẽ đồ thị để các ký tự tiếng Việt có dấu không bị lỗi hiển thị.

---

### 5.6 DeepSeek V3 / R1 (Aider / Shell / API)
Khi sử dụng DeepSeek qua Aider (`aider --model deepseek/deepseek-chat`):
```bash
# Thêm file quy chuẩn vào ngữ cảnh Aider
/add AGENTS.md CLAUDE.md
# Ra lệnh thực thi theo vai trò
Act as the Ingestion & Wrangling Agent. Implement missing value imputation and unit conversion in src/wrangling.py following Bai 02. Ensure datasets/raw/ is untouched.
```

---

### 5.7 Khung Điều Phối Tự Động (LangGraph, AutoGen, CrewAI)
- **LangGraph**: Xây dựng State Graph với 5 nodes tương ứng 5 Roles. State channel truyền đường dẫn file theo các Hợp đồng H1 - H6 trên đĩa cứng (`datasets/processed/`, `reports/diagnostics/model_diagnostics.npz`).
- **CrewAI**: Thiết lập `Crew` gồm 5 `Agent` với `role`, `goal`, `backstory` lấy từ Mục 2, cấu hình tool đọc ghi file an toàn, bảo vệ `datasets/raw/`.

---

## 6. Quy Chuẩn Bất Biến & Ràng Buộc Vận Hành (Strict Operational Constraints & Invariants)

---

### 6.1 Tính Bất Biến Của Dữ Liệu Thô (Raw Data Immutability)
- Thư mục `datasets/raw/` là khu vực **CHỈ ĐỌC (STRICTLY READ-ONLY)**.
- Tuyệt đối không thực hiện bất kỳ thao tác nào sau đây:
  - Ghi đè file gốc (`df.to_csv('datasets/raw/imports-85.data')`).
  - Sửa đổi nội dung trực tiếp bằng text editor hoặc script.
  - Xóa hoặc đổi tên file trong `datasets/raw/`.
- Mọi dữ liệu sau khi làm sạch, biến đổi hoặc sinh mới **BẮT BUỘC** phải lưu vào thư mục `datasets/processed/`.

---

### 6.2 Tính Tái Lập Tuyệt Đối (Reproducibility & random_state=42)
- Mọi thuật toán hoặc hàm có yếu tố ngẫu nhiên đều phải được cố định hạt giống:
  ```python
  RANDOM_STATE = 42

  # 1. Phân chia tập dữ liệu
  X_train, X_test, y_train, y_test = train_test_split(
      X, y, test_size=0.3, random_state=RANDOM_STATE
  )

  # 2. Đánh giá chéo K-Fold
  kf = KFold(n_splits=4, shuffle=True, random_state=RANDOM_STATE)

  # 3. Ước lượng mô hình
  ridge_model = Ridge(alpha=0.1, random_state=RANDOM_STATE)
  ```
- Nghiêm cấm chạy phân chia dữ liệu mà không truyền tham số `random_state`.

---

### 6.3 Chuẩn Mực Thống Kê & Ý Nghĩa p-value (Statistical Rigor & alpha=0.05)
- Mức ý nghĩa thống kê chuẩn của môn học là $\alpha = 0.05$.
- Mọi kết luận tương quan (Pearson $r$) hoặc sai khác trung bình nhóm (ANOVA $F$) đều phải đi kèm giá trị $p$-value cụ thể:
  - $p < 0.001$: Tương quan / sai khác có ý nghĩa thống kê rất cao (Bác bỏ $H_0$).
  - $p < 0.05$: Tương quan / sai khác có ý nghĩa thống kê (Bác bỏ $H_0$).
  - $p \ge 0.05$: Không đủ bằng chứng bác bỏ $H_0$. Không được kết luận biến có khả năng dự báo.
- Tiêu chuẩn chọn biến vào mô hình: Bắt buộc $|r| \ge 0.30$ VÀ $p < 0.05$ (slide Bai05 p. 37).
- Luôn phân biệt rạch ròi: *Tương quan thống kê không đồng nghĩa với quan hệ nhân quả (Correlation does not imply Causation)*.

---

### 6.4 Bắt Buộc Sử Dụng Matplotlib Object-Oriented API & Cấu Hình Font Tiếng Việt
- Trong toàn bộ mã nguồn module hóa (`src/`) và các notebook nộp bài, **NGHIÊM CẤM** sử dụng cú pháp state-machine của `pyplot` (ví dụ: `plt.plot()`, `plt.title()`, `plt.xlabel()`).
- Bắt buộc khởi tạo và thao tác qua đối tượng `Figure` và `Axes`, kèm cấu hình font hiển thị tiếng Việt:

```python
# CHUẨN MỰC BẮT BUỘC (CORRECT - Object-Oriented API with Vietnamese Font Support):
import matplotlib.pyplot as plt

# Cấu hình font tiếng Việt chuẩn trên Linux / WSL2 / Docker
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Liberation Sans', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(df['engine-size'], df['price'], alpha=0.7, edgecolors='k', label='Dữ liệu thực tế')
ax.set_title("Mối Quan Hệ Giữa Dung Tích Động Cơ Và Giá Xe", fontsize=14, fontweight='bold', pad=12)
ax.set_xlabel("Dung tích động cơ (Engine Size - cc)", fontsize=12)
ax.set_ylabel("Giá bán (Price - USD)", fontsize=12)
ax.grid(True, linestyle="--", alpha=0.5)
ax.legend(loc="upper left")
plt.tight_layout()
fig.savefig("reports/figures/engine_size_vs_price.png", dpi=300)
plt.close(fig)
```

---

### 6.5 Không Rò Rỉ Dữ Liệu (Zero Data Leakage via Scikit-Learn Pipeline)
- Không được áp dụng các phép biến đổi (Scaling, Imputation, Polynomial Features) trên toàn bộ tập dữ liệu trước khi phân chia Train/Test.
- Toàn bộ các bước tiền xử lý và biến đổi đặc trưng phải được gói gọn trong Scikit-Learn `Pipeline`:

```python
# CHUẨN MỰC CHỐNG RÒ RỈ DỮ LIỆU (CORRECT - Scikit-Learn Pipeline):
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import Ridge

model_pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('poly', PolynomialFeatures(degree=2, include_bias=False)),
    ('ridge', Ridge(alpha=0.1, random_state=42))
])

# Fit duy nhất trên tập Train, tự động transform trên tập Test khi predict
model_pipeline.fit(X_train, y_train)
y_pred = model_pipeline.predict(X_test)
```

---

### 6.6 Quy Ước Ranh Giới Ngôn Ngữ (Bilingual Language Boundary Rules)
Nhằm đảm bảo tính hội nhập quốc tế kết hợp tính sư phạm tại UIT:
1. **Phần Tiếng Anh (English)**:
   - Tên biến, tên hàm, tên lớp, tên module, tên file (`src/ingestion.py`, `def calculate_pearson_correlation(...)`).
   - Thông điệp commit Git (`feat: implement one-way ANOVA F-test in src/eda.py`).
   - Mã định danh test (`test_null_imputation_preserves_shape()`).
2. **Phần Tiếng Việt (Vietnamese)**:
   - Docstring giải thích chức năng hàm và phương pháp thống kê.
   - Tiêu đề biểu đồ (`ax.set_title`), nhãn các trục tọa độ (`ax.set_xlabel`, `ax.set_ylabel`), chú giải (`ax.legend`).
   - Lời giải thích, phân tích nhận xét và kết luận trong các cell Markdown của Jupyter Notebooks.
   - Báo cáo kết quả đồ án cuối kỳ.

---

## 7. Bộ Lệnh Thực Thi & Kiểm Tra Chuẩn (Standard Toolchains & Verification Commands)

Mọi tác tử AI và sinh viên phải nắm vững các lệnh thực thi trong môi trường Linux/WSL2:

```bash
# ==============================================================================
# 1. THIẾT LẬP MÔI TRƯỜNG ẢO & CÀI ĐẶT THƯ VIỆN
# ==============================================================================
# Khuyến nghị: Dùng uv để cài đặt cực nhanh
uv venv .venv && source .venv/bin/activate
uv pip install -r requirements.txt

# Hoặc dùng python3-venv tiêu chuẩn
python3 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# ==============================================================================
# 2. THỰC THI PIPELINE XỬ LÝ DỮ LIỆU & MÔ HÌNH
# ==============================================================================
# Bước 1 & 2: Thu thập và làm sạch dữ liệu
python src/ingestion.py --dataset automobile
python src/wrangling.py --input datasets/raw/imports-85.data --output datasets/processed/automobile_cleaned.csv

# Bước 3: Khám phá dữ liệu và tính toán thống kê
python src/eda.py --input datasets/processed/automobile_cleaned.csv

# Bước 4: Tạo biểu đồ trực quan hóa chuẩn 300 DPI
python src/visualization.py --all

# Bước 5 & 6: Huấn luyện mô hình, kiểm định chéo và tối ưu hóa siêu tham số
python src/models.py --train --cv 4 --tune-alpha

# ==============================================================================
# 3. KIỂM TRA CHẤT LƯỢNG MÃ NGUỒN VỚI RUFF (QA AGENT)
# ==============================================================================
# Kiểm tra linting toàn bộ repository
ruff check .

# Tự động sửa các lỗi cú pháp và import
ruff check . --fix

# Định dạng mã nguồn chuẩn PEP 8
ruff format .

# Kiểm tra định dạng (không ghi đè file)
ruff format --check .

# ==============================================================================
# 4. CHẠY KIỂM THỬ TỰ ĐỘNG PYTEST VỚI COVERAGE (QA AGENT)
# ==============================================================================
# Chạy toàn bộ test suites
pytest

# Chạy chi tiết kèm đo độ bao phủ mã nguồn trong src/
pytest tests/ -v --cov=src --cov-report=term-missing

# Chạy riêng từng module kiểm thử
pytest tests/test_wrangling.py -v
pytest tests/test_eda.py -v
pytest tests/test_models.py -v

# ==============================================================================
# 5. THỰC THI JUPYTER NOTEBOOK Ở CHẾ ĐỘ HEADLESS (QA AGENT)
# ==============================================================================
# Đảm bảo 100% notebook chạy trơn tru từ đầu đến cuối không phát sinh lỗi
jupyter nbconvert --to notebook --execute notebooks/01_data_ingestion.ipynb
jupyter nbconvert --to notebook --execute notebooks/02_data_wrangling.ipynb
jupyter nbconvert --to notebook --execute notebooks/03_basic_visualization.ipynb
jupyter nbconvert --to notebook --execute notebooks/04_advanced_visualization.ipynb
jupyter nbconvert --to notebook --execute notebooks/05_exploratory_data_analysis.ipynb
jupyter nbconvert --to notebook --execute notebooks/06_model_development.ipynb
jupyter nbconvert --to notebook --execute notebooks/07_model_evaluation.ipynb

# ==============================================================================
# 6. KHỞI CHẠY JUPYTERLAB CHO PHÂN TÍCH TƯƠNG TÁC
# ==============================================================================
jupyter lab --no-browser --port=8888 --ip=0.0.0.0
```

---
*Tài liệu này được biên soạn và bảo trì theo chuẩn học thuật của Trường Đại học Công nghệ Thông tin - ĐHQG-HCM (UIT).*  
*Mọi thay đổi đối với quy tắc vận hành của tác tử AI phải được đồng bộ với [CLAUDE.md](./CLAUDE.md).*