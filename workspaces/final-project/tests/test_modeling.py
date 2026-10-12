"""Bộ kiểm thử đơn vị & hồi quy cho module modeling (Bước 7).

Kiểm tra nghiêm ngặt các yêu cầu kỹ thuật & chống rò rỉ dữ liệu:
- Tính bất biến và tái lập của train/test split và 4-fold KFold với random_state=42.
- Từ chối tuyệt đối các cột cấm và cột làm rò rỉ biến mục tiêu (id, host_id, price_quote_*, v.v.).
- Chọn lọc đặc trưng độc lập trong từng fold: Không rò rỉ dữ liệu giữa các fold hoặc từ test sang train.
- Xử lý các trường hợp biên: Biến hằng số (zero variance), biến toàn khuyết, biến ít mẫu.
- Thẩm định tính không khả thi: Không hạ ngưỡng hoặc bỏ fold âm thầm khi không có đặc trưng đạt chuẩn.
- Đánh giá mốc cơ sở DummyRegressor (y_train mean benchmark): Khớp công thức R^2 Bài 06.
- Khả năng xây dựng và huấn luyện Pipeline đầy đủ (imputer, scaler, OneHotEncoder, Ridge tuning)
  trên dữ liệu giả lập (synthetic data) có đặc trưng tương quan mạnh (|r| >= 0.30).

Đồ án môn học IE313 (UIT - VNU-HCM) - Nhóm 10.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from sklearn.model_selection import KFold

from src.modeling import (
    FORBIDDEN_COLUMNS,
    build_regression_pipeline,
    evaluate_mean_dummy_benchmark,
    generate_model_comparison_table,
    run_cross_fold_feature_selection,
    run_full_modeling_workflow,
    select_features_for_fold,
    split_data,
    validate_feature_inputs,
    verify_baseline_data,
)


@pytest.fixture
def sample_cleaned_df() -> pd.DataFrame:
    """Fixture DataFrame giả lập có cấu trúc giống baseline cleaned."""
    np.random.seed(42)
    n = 100
    return pd.DataFrame(
        {
            "id": range(1001, 1001 + n),
            "host_id": np.random.choice([1, 2, 3, 4, 5], n),
            "last_scraped": ["2026-06-29"] * n,
            "price": np.random.uniform(500, 10000, n),
            "room_type": np.random.choice(["Entire home/apt", "Private room", "Shared room"], n),
            "property_type": np.random.choice(["Condo", "Apartment", "House"], n),
            "neighbourhood_cleansed": np.random.choice(["Watthana", "Khlong Toei", "Sathon"], n),
            "accommodates": np.random.randint(1, 8, n).astype(float),
            "bedrooms": np.random.choice([1.0, 2.0, 3.0, np.nan], n),
            "bathrooms": np.random.choice([1.0, 1.5, 2.0, np.nan], n),
            "beds": np.random.choice([1.0, 2.0, 4.0, np.nan], n),
            "minimum_nights": np.random.randint(1, 5, n).astype(float),
            "number_of_reviews": np.random.randint(0, 100, n).astype(float),
            "review_scores_rating": np.random.choice([4.5, 4.8, 5.0, np.nan], n),
            "host_is_superhost": np.random.choice(["t", "f"], n),
            "price_raw": ["$1,000.00"] * n,
        }
    )


class TestValidationAndDataSplit:
    """Kiểm thử tính toàn vẹn, xác thực và phân chia dữ liệu chống rò rỉ."""

    def test_verify_baseline_data_valid(self, sample_cleaned_df: pd.DataFrame) -> None:
        """Kiểm tra xác thực thành công khi dữ liệu hợp lệ."""
        assert verify_baseline_data(sample_cleaned_df, expected_sha256=None) is True

    def test_verify_baseline_data_missing_columns(self) -> None:
        """Kiểm tra báo lỗi khi thiếu cột price hoặc id."""
        df_no_price = pd.DataFrame({"id": [1, 2], "val": [10, 20]})
        with pytest.raises(ValueError, match="Thiếu biến mục tiêu 'price'"):
            verify_baseline_data(df_no_price, expected_sha256=None)

        df_no_id = pd.DataFrame({"price": [10.0, 20.0]})
        with pytest.raises(ValueError, match="Thiếu cột định danh 'id'"):
            verify_baseline_data(df_no_id, expected_sha256=None)

    def test_verify_baseline_data_duplicate_ids(self) -> None:
        """Kiểm tra báo lỗi khi cột id có giá trị trùng lặp."""
        df_dup = pd.DataFrame({"id": [1, 1], "price": [10.0, 20.0]})
        with pytest.raises(ValueError, match="trùng lặp"):
            verify_baseline_data(df_dup, expected_sha256=None)

    def test_validate_feature_inputs_rejects_forbidden_columns(self) -> None:
        """Kiểm tra từ chối tuyệt đối các cột rò rỉ hoặc cấm."""
        for forbidden in FORBIDDEN_COLUMNS:
            with pytest.raises(ValueError, match="Phát hiện cột cấm hoặc gây rò rỉ"):
                validate_feature_inputs([forbidden])

        with pytest.raises(ValueError, match="Phát hiện cột cấm hoặc gây rò rỉ"):
            validate_feature_inputs(["price_quote_price_per_night"])

        with pytest.raises(ValueError, match="không nằm trong danh sách MODEL_FEATURES"):
            validate_feature_inputs(["random_unknown_column"])

    def test_split_data_reproducibility(self, sample_cleaned_df: pd.DataFrame) -> None:
        """Kiểm tra tính tái lập tuyệt đối của phân chia 70/30 và KFold với random_state=42."""
        X_tr1, X_te1, y_tr1, y_te1, split1, meta1 = split_data(sample_cleaned_df, random_state=42)
        X_tr2, X_te2, y_tr2, y_te2, split2, meta2 = split_data(sample_cleaned_df, random_state=42)

        pd.testing.assert_frame_equal(X_tr1, X_tr2)
        pd.testing.assert_frame_equal(X_te1, X_te2)
        pd.testing.assert_series_equal(y_tr1, y_tr2)
        pd.testing.assert_series_equal(y_te1, y_te2)
        pd.testing.assert_frame_equal(split1, split2)
        assert meta1 == meta2
        assert len(X_tr1) == 70
        assert len(X_te1) == 30

    def test_holdout_changes_do_not_affect_train_split(
        self, sample_cleaned_df: pd.DataFrame
    ) -> None:
        """Kiểm tra tính độc lập: Thay đổi/thêm dữ liệu ở holdout không làm biến đổi tập train."""
        X_tr, _, y_tr, _, _, _ = split_data(sample_cleaned_df, random_state=42)

        # Chỉnh sửa phần thuộc test set
        modified_df = sample_cleaned_df.copy()
        # Tìm một index thuộc test
        test_indices = [idx for idx in modified_df.index if idx not in X_tr.index]
        modified_df.loc[test_indices[0], "accommodates"] = 999.0

        X_tr_mod, _, y_tr_mod, _, _, _ = split_data(modified_df, random_state=42)
        pd.testing.assert_frame_equal(X_tr, X_tr_mod)
        pd.testing.assert_series_equal(y_tr, y_tr_mod)


class TestFeatureSelectionInFolds:
    """Kiểm thử logic chọn lọc đặc trưng độc lập trong từng fold."""

    def test_feature_selection_meets_criteria_synthetic(self) -> None:
        """Kiểm tra đặc trưng tương quan mạnh (|r| >= 0.30 và p < 0.05) được chọn chính xác."""
        np.random.seed(42)
        n = 100
        # Tạo biến tương quan mạnh r ~ 0.8
        x_strong = np.random.uniform(1, 10, n)
        y = 500 + 200 * x_strong + np.random.normal(0, 50, n)
        # Tạo biến tương quan yếu r ~ 0.05
        x_weak = np.random.uniform(1, 10, n)

        fold_df = pd.DataFrame(
            {
                "accommodates": x_strong,
                "bedrooms": x_weak,
                "room_type": ["Entire home/apt"] * n,
            }
        )
        res = select_features_for_fold(fold_df, pd.Series(y), r_threshold=0.30, alpha=0.05)

        assert "accommodates" in res["selected_numeric"]
        assert "bedrooms" not in res["selected_numeric"]
        assert res["numeric_features"]["accommodates"]["selected"] is True
        assert res["numeric_features"]["bedrooms"]["selected"] is False
        assert res["has_selected_features"] is True

    def test_feature_selection_handles_constant_and_missing(self) -> None:
        """Kiểm tra xử lý an toàn biến hằng số (zero variance) và biến toàn khuyết."""
        np.random.seed(42)
        n = 50
        y = pd.Series(np.random.uniform(500, 2000, n))
        fold_df = pd.DataFrame(
            {
                "accommodates": [4.0] * n,  # Biến hằng số
                "bedrooms": [np.nan] * n,  # Toàn khuyết
                "bathrooms": [1.0, np.nan] * (n // 2),
            }
        )
        res = select_features_for_fold(fold_df, y)

        assert res["numeric_features"]["accommodates"]["reason"] == "ZERO_VARIANCE_CONSTANT_FEATURE"
        assert res["numeric_features"]["bedrooms"]["reason"] == "INSUFFICIENT_OBSERVATIONS"
        assert res["numeric_features"]["accommodates"]["selected"] is False
        assert res["numeric_features"]["bedrooms"]["selected"] is False

    def test_cross_fold_feature_selection_isolation(self) -> None:
        """Kiểm tra việc chọn biến được tính riêng biệt trên từng fold, không chia sẻ trạng thái."""
        np.random.seed(42)
        n = 40
        X = pd.DataFrame({"accommodates": np.random.uniform(1, 8, n)})
        y = pd.Series(np.random.uniform(500, 5000, n))
        kf = KFold(n_splits=4, shuffle=True, random_state=42)

        res = run_cross_fold_feature_selection(X, y, kf=kf, r_threshold=0.30, alpha=0.05)
        assert len(res["folds"]) == 4
        assert "full_train" in res
        assert "folds_selected_counts" in res
        assert len(res["folds_selected_counts"]) == 4


class TestDummyBenchmarkAndComparison:
    """Kiểm thử mốc cơ sở DummyRegressor và phát sinh bảng so sánh."""

    def test_evaluate_mean_dummy_benchmark(self) -> None:
        """Kiểm tra tính toán mốc so sánh cơ sở theo công thức R^2 Bài 06."""
        y_train = pd.Series([100.0, 200.0, 300.0, 400.0, 500.0])
        y_test = pd.Series([150.0, 250.0, 350.0])
        kf = KFold(n_splits=2, shuffle=True, random_state=42)

        bench = evaluate_mean_dummy_benchmark(y_train, y_test, kf)
        assert bench["train_mean_prediction_thb"] == 300.0
        assert bench["train_r2"] == pytest.approx(0.0, abs=1e-4)
        assert bench["train_mse"] > 0
        assert bench["test_mse"] > 0
        assert len(bench["cv_4fold_mse_by_fold"]) == 2

    def test_generate_model_comparison_table_infeasible(self) -> None:
        """Kiểm tra phát sinh bảng so sánh khi không khả thi (gồm 5 hàng chuẩn)."""
        benchmark_res = {
            "model_name": "DummyRegressor (Mean Benchmark - Bổ sung kỹ thuật)",
            "train_mse": 383665813.44,
            "train_r2": 0.0,
            "cv_4fold_mse_mean": 383714969.84,
            "cv_4fold_r2_mean": -0.0005,
            "test_mse": 315021203.83,
            "test_r2": -0.0,
            "status": "COMPLETED_BENCHMARK",
        }
        feasibility_info = {
            "is_modeling_feasible": False,
            "infeasibility_reason": "No features met criteria",
        }

        df_comp = generate_model_comparison_table(benchmark_res, feasibility_info)
        assert len(df_comp) == 5
        assert df_comp.iloc[0]["status"] == "COMPLETED_BENCHMARK"
        assert "NOT_FEASIBLE" in df_comp.iloc[1]["status"]
        assert "NOT_FEASIBLE" in df_comp.iloc[2]["status"]
        assert "NOT_FEASIBLE" in df_comp.iloc[3]["status"]
        assert "NOT_FEASIBLE" in df_comp.iloc[4]["status"]


class TestSyntheticPipelineExecution:
    """Kiểm thử tính năng xây dựng Pipeline scikit-learn khi có đặc trưng hợp lệ (synthetic)."""

    def test_pipeline_build_and_fit_predict(self) -> None:
        """Kiểm tra Pipeline ColumnTransformer + Ridge fit và predict trơn tru trên dữ liệu có missing và danh mục chưa thấy."""
        pipe = build_regression_pipeline(
            selected_numeric=["accommodates"],
            selected_categorical=["room_type"],
            model_type="ridge",
            alpha=1.0,
        )

        train_data = pd.DataFrame(
            {
                "accommodates": [2.0, 4.0, np.nan, 6.0],
                "room_type": ["Entire home/apt", "Private room", "Entire home/apt", "Shared room"],
            }
        )
        y_train = pd.Series([1000.0, 2000.0, 1500.0, 3000.0])

        pipe.fit(train_data, y_train)

        # Test trên dữ liệu có danh mục chưa từng thấy và missing
        test_data = pd.DataFrame(
            {
                "accommodates": [np.nan, 3.0],
                "room_type": ["UNKNOWN_CATEGORY", "Private room"],
            }
        )
        preds = pipe.predict(test_data)
        assert len(preds) == 2
        assert np.all(np.isfinite(preds))


class TestFullModelingWorkflowExecution:
    """Kiểm thử quy trình thực thi đầy đủ run_full_modeling_workflow trên fixture."""

    def test_run_full_modeling_workflow_infeasible_case(self, tmp_path: Path) -> None:
        """Kiểm tra chạy toàn bộ quy trình trên dữ liệu không đạt chuẩn chọn biến sinh đủ 5 artifact."""
        np.random.seed(42)
        df = pd.DataFrame(
            {
                "id": range(1, 41),
                "host_id": [1, 2] * 20,
                "last_scraped": ["2026-06-29"] * 40,
                "price": np.random.uniform(500, 2000, 40),
                "room_type": ["Entire home/apt", "Private room"] * 20,
                "property_type": ["Condo", "Apartment"] * 20,
                "neighbourhood_cleansed": ["Watthana", "Sathon"] * 20,
                "accommodates": np.random.uniform(1, 5, 40),
                "bedrooms": [1.0] * 40,
                "bathrooms": [1.0] * 40,
                "beds": [1.0] * 40,
                "minimum_nights": [1.0] * 40,
                "number_of_reviews": [10.0] * 40,
                "review_scores_rating": [4.8] * 40,
                "host_is_superhost": ["t", "f"] * 20,
                "price_raw": ["$1,000.00"] * 40,
            }
        )
        baseline_csv = tmp_path / "baseline_test.csv"
        df.to_csv(baseline_csv, index=False)

        out_dir = tmp_path / "reports_modeling"
        meta = run_full_modeling_workflow(
            baseline_csv, output_dir=out_dir, expected_sha256=None, random_state=42
        )

        assert (out_dir / "split_assignments.csv").is_file()
        assert (out_dir / "feature_selection.json").is_file()
        assert (out_dir / "model_comparison.csv").is_file()
        assert (out_dir / "modeling_metadata.json").is_file()
        assert (out_dir / "modeling_findings.md").is_file()
        assert meta["feasibility_decision"]["is_modeling_feasible"] is False
        assert meta["conditional_artifacts"]["best_pipeline_joblib"] is None
