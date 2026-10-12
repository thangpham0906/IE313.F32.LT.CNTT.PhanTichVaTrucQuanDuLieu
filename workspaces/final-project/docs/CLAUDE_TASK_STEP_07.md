# Giao việc Claude Code — Bước 7: Hồi quy bổ trợ sau review EDA

Ngày giao: **11/10/2026**. Hạn nộp đồ án **18/10/2026**; mốc nội bộ Bước 7 **15/10**. Người phụ trách học thuật: **Lê Minh Thiện**; kiểm tra chéo: **Phạm Quốc Thắng**. Người dùng đã yêu cầu review và tiếp tục các bước; thực thi nhiệm vụ này, không chỉ trả kế hoạch.

## 1. Đọc trước và giữ phạm vi

Làm việc tại `workspaces/final-project/`, dùng `.venv/bin/python`. Đọc `AGENTS.md`, `CLAUDE.md` ở root và:

- `docs/SPECIFICATION.md`, nhất là mục 1.4 và 4.2; đối chiếu Bài 06–07 trong `slide-study/`.
- `reports/qa_review_step_05_06.md`, `reports/qa_step_05_06_verification.json`: review hiện hành của Codex. `qa_response_step_05_06.md` là bản bàn giao cũ, có số liệu đã được đính chính.
- `docs/CLEANING_PLAN.md`, `docs/EDA_METHODS.md`, `reports/eda_findings.md`, `README.md`, `docs/RUNBOOK.md`.

Bước 1–6 đã review/sửa: không khôi phục boxplot/OLS trên dữ liệu cắt theo trục, số mẫu catalog nhập tay hay kết luận ANOVA đủ giả định từ skew nhỏ/Levene không có ý nghĩa. Nhận xét EDA được sinh bởi `src/eda_report.py`. Notebook 02–03 có bản mẫu sạch tại `scripts/notebook_templates/`; tránh ghi đè bằng generator cũ.

Đầu vào `data/processed/bangkok_cleaned.csv`: **28.987 × 16**, SHA-256 `961a01ad225e35f989ec81f124925488e392baca2ef3800ff4028b4423d5f9a7`. Giữ nguyên mọi giá dương, missing predictor và các giá cực trị. Raw SHA-256 `b17b99f9c421c566cc26a1c89a0b3d16b4c7f3dc74e659141900ccbac316b20e`, mtime_ns `1791612578936933598`.

## 2. Đánh giá khả thi trước khi fit

1. Xác minh hash, ID duy nhất và schema. `price` là y, đơn vị THB/đêm. Chỉ dùng 11 predictor trong `src.wrangling.MODEL_FEATURES`; không dùng `id`, `host_id`, `last_scraped`, `price_raw`, biến tạo từ price hay các cột price_quote/revenue. ID chỉ phục vụ lưu vết chia tập.
2. Chia **70/30, random_state=42** theo listing trước khi học/chọn biến. Lưu ID train/test, số dòng, checksum nguồn và số host giao nhau. Giải thích đây là listing chưa thấy trong cùng snapshot, có thể cùng host; không đánh giá chủ nhà mới hay giá tương lai. Không đổi sang split khác chỉ vì R² thấp.
3. Trong **mỗi training fold**, kiểm tra Pearson biến số với y trên cặp hữu hạn hợp lệ, dùng trị chưa làm tròn: **|r|≥0,30 VÀ p<0,05**. Biến hằng/toàn thiếu/ít mẫu phải có lý do loại. Ghi n, r, p và quyết định. Không nạp danh sách biến đã chọn từ EDA toàn dữ liệu.
4. Biến phân loại: đánh giá số nhóm, cỡ nhóm, phân phối, độ phân tán, giới hạn độc lập trước khi dùng ANOVA p<0,05 theo đặc tả. Không tự xác nhận đủ giả định, không lấy p nhỏ làm căn cứ duy nhất khi điều kiện không bảo đảm. Nếu chưa có cơ sở sử dụng ANOVA để chọn biến, báo cáo F/p thăm dò khi tính được, loại biến khỏi mô hình chính và nêu lý do. Không tự chuyển sang kiểm định khác.
5. **Không còn biến phù hợp là một kết quả hợp lệ.** Nếu training fold nào không đủ biến, ghi rõ tính không khả thi; không hạ ngưỡng, ép giữ biến, bỏ fold lỗi rồi lấy trung bình những fold còn lại, hoặc tạo R² giả. Không bắt buộc có SLR/đa thức nếu không còn biến số hợp lệ. Phân biệt “không phù hợp với quy tắc hiện tại” với “không có quan hệ nào trong thực tế”.

EDA toàn mẫu hiện cho r thấp ở 4 biến quy mô; đó là thông tin cảnh báo, không thay thế kiểm tra trên train/fold. Phương pháp và quyết định khả thi phải được lưu thành artifact dù cuối cùng không fit được hồi quy.

## 3. Pipeline và đánh giá nếu khả thi

- Thiết kế chọn biến như bước fit trong Pipeline hoặc estimator tương thích scikit-learn, để clone/fit lại trong từng fold. Sau chọn biến, numeric dùng imputer rồi scaler; categorical dùng imputer rồi OneHotEncoder xử lý danh mục chưa thấy. `ColumnTransformer`, `SimpleImputer`, `GridSearchCV` và bộ chọn biến tùy chỉnh ghi “Bổ sung kỹ thuật theo repository”, không gán tên API cho bài giảng chưa đối chiếu.
- **KFold(n_splits=4, shuffle=True, random_state=42)** trên train; dùng cùng fold khi so sánh Linear Regression và Ridge. Lưới alpha giới hạn `[0.001, 0.01, 0.1, 1, 10, 100, 1000]`. Chọn bằng CV MSE, công bố fold score và trung bình/std; ghi rõ kết quả CV dùng để chọn cấu hình, holdout dùng đánh giá cuối.
- Đa thức bậc thấp chỉ khi có biến số hợp lệ và bằng chứng train/CV phù hợp; không tạo đa thức trên toàn bộ dummy. Nếu bỏ SLR/đa thức, nêu lý do gắn với dữ liệu/quy tắc.
- Fit mô hình chọn cuối trên toàn train, rồi đánh giá holdout; không dùng test để chọn biến/alpha/biến đổi/cắt giá. Không điều chỉnh ngưỡng sau khi xem test.
- MSE (THB²), R² (không đơn vị) trên train, từng fold CV và test. Nếu tính R² không được do y hằng/ít mẫu, trả null cùng lý do; không biến null/NaN thành 0. R² âm phải giữ nguyên.
- Có thể dùng dự đoán trung bình y_train làm mốc so sánh cơ bản liên hệ công thức R² Bài 06; nếu triển khai DummyRegressor ghi rõ API bổ sung kỹ thuật. Mốc trung bình không được ghi là đã hoàn tất hồi quy Linear/Ridge khi không có predictor hợp lệ.
- Chẩn đoán trên dự đoán thật: thực–dự đoán, phần dư theo dự đoán, phân phối thực–dự đoán; mô tả ngẫu nhiên/dạng cong/độ phân tán tăng nếu quan sát được, không ép đủ ba tình huống hay tạo dữ liệu giả. OO API, font tiếng Việt, nhãn đơn vị và 300 DPI. Nếu không có hồi quy khả thi, ghi lý do không sinh chẩn đoán hồi quy.
- Không mở rộng Random Forest, Spearman, SHAP, log(price), winsorization, NLP, bản đồ hay dashboard. Không âm thầm loại giá cao để tăng điểm số.

## 4. Sản phẩm phải tạo

| Sản phẩm | Nội dung tối thiểu |
|---|---|
| `src/modeling.py` (và module nhỏ nếu cần) | Hàm dùng lại, CLI, chọn biến trong fold, Pipeline và đánh giá; xử lý không khả thi có cấu trúc |
| `notebooks/04_regression_modeling.ipynb` | Chạy từ đầu đến cuối; mục tiêu, nguồn bài học, split, chọn biến, CV, kết quả/giải trình, giới hạn |
| `reports/modeling/modeling_metadata.json` | Hash dữ liệu, allowlist, seed, split/folds, phiên bản, giao host, quyết định khả thi và lý do |
| `reports/modeling/split_assignments.csv` | ID và train/test; fold trên phần train; không dùng ID làm predictor |
| `reports/modeling/feature_selection.json` | Kết quả từng biến ở từng training fold và khi fit toàn train; n, r/F, p, quyết định/lý do |
| `reports/modeling/model_comparison.csv` | MSE/R², cấu hình và tập đánh giá; trạng thái/giải trình nếu không có mô hình hợp lệ |
| `reports/modeling/modeling_findings.md` | Kết quả thật và liên hệ Bài 06–07; giới hạn, kết luận phù hợp mức bằng chứng |
| `models/best_pipeline.joblib` | Chỉ khi có hồi quy khả thi; lưu pipeline đầy đủ, dự đoán được trên X thô trong allowlist |
| `reports/diagnostics/model_diagnostics.npz` + metadata | Chỉ khi có hồi quy: ID test, y_test_actual, y_test_predicted, residuals; ghi đơn vị/mô hình/phạm vi |
| `reports/figures/model_*.png` + catalog riêng | Hình chẩn đoán khi có; không ghi đè catalog 5 hình EDA |
| `tests/test_modeling.py` | Kiểm tra chống rò rỉ và trường hợp biên có ý nghĩa |
| `reports/qa_response_step_07.md` | Những gì đã chạy, exit code, số test thật, file đầu ra, hạn chế và việc còn lại |

JSON phải chuẩn (null thay cho số không hữu hạn). Không để artifact cũ của một mô hình thành công gây hiểu lầm khi lần chạy hiện tại không khả thi; output manifest phải chỉ rõ kết quả hiện hành. Mọi số liệu nhận xét/bảng/hình phải sinh từ cùng kết quả chạy, không nhập tay.

## 5. Kiểm tra và bàn giao

- Tests có ý nghĩa: holdout thay đổi không làm thay lựa chọn/fit trên train; selector/imputer/encoder fit riêng từng fold; cột cấm bị từ chối; danh mục chưa thấy và missing predictor; biến hằng/toàn thiếu; không còn biến; không bỏ fold lỗi âm thầm; split/folds seed42 lặp lại được; khớp residual = y_actual − y_pred và ID/dòng dự đoán.
- Chạy `.venv/bin/python -m pytest tests --cov=src --cov-report=term-missing`, `.venv/bin/ruff check .`, `.venv/bin/ruff format --check .`; chạy notebook 04 bằng kernel mới/headless. Nếu sửa module chung, chạy lại notebook bị ảnh hưởng. Ghi kết quả thật, không dùng số test/coverage cũ.
- Đối chiếu raw hash/mtime và baseline hash trước/sau; template GV và Word/PDF bản khung nguyên vẹn. Không thay raw hoặc thay baseline để phù hợp mô hình. Không sửa logic/số liệu EDA đã review trừ khi phát hiện lỗi có minh chứng và ghi rõ bản sửa.
- Cập nhật trạng thái README và runbook đúng sản phẩm đã có. Hai đặc tả `docs/SPECIFICATION.md` và `../../docs/superpowers/specs/2026-10-07-airbnb-bangkok-analysis-design.md` phải byte-identical. README có một hàng cho mỗi Bước 1–10; không lặp hàng khi cập nhật. Không đánh dấu nhóm đã kiểm tra chéo nếu chưa có xác nhận.
- Hoàn thành phạm vi Bước 7 rồi báo kết quả để Codex review. Chưa chỉnh Word/slide cuối kỳ hoặc triển khai Bước 8–10 trong lượt này. Không commit/push. Không yêu cầu người dùng xác nhận lại những việc đã được giao ở trên.
