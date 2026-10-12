"""Bộ kiểm thử đơn vị (Unit Tests) cho module eda_stats.

Kiểm tra tính đúng đắn của các hàm thống kê mô tả, kiểm định tương quan Pearson,
đánh giá điều kiện ANOVA, bảng chéo 2D và minh họa kỹ thuật Bài 02.
Bao gồm các trường hợp biên: mẫu rỗng, mẫu hằng số (zero variance), mẫu thiếu dữ liệu.
Đồ án môn học IE313 (UIT - VNU-HCM) - Nhóm 10.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from src.data_loader import compute_sha256
from src.eda_stats import (
    compute_anova_test,
    compute_neighbourhood_pivot,
    compute_pairwise_correlations,
    compute_price_distribution_stats,
    compute_room_type_stats,
    demonstrate_lesson02_wrangling,
    evaluate_anova_conditions,
    run_full_eda,
)


class TestPriceDistributionStats:
    """Kiểm thử hàm compute_price_distribution_stats với dữ liệu chuẩn và ca biên."""

    def test_standard_price_series(self) -> None:
        """Kiểm tra tính toán đầy đủ trên chuỗi giá tiêu chuẩn."""
        # Chuỗi 9 số: 10, 20, 30, 40, 50, 60, 70, 80, 1000 (1000 là outlier)
        s = pd.Series([10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 1000.0])
        res = compute_price_distribution_stats(s)

        assert res["n"] == 9
        assert res["min"] == 10.0
        assert res["max"] == 1000.0
        assert res["median"] == 50.0
        assert res["mean"] == pytest.approx(151.11, abs=0.01)
        assert res["q1"] == 30.0
        assert res["q3"] == 70.0
        assert res["iqr"] == 40.0
        assert res["outliers_count"] == 1
        assert res["outliers_pct"] == pytest.approx(11.11, abs=0.01)
        assert res["skewness"] is not None and res["skewness"] > 0
        assert res["kurtosis"] is not None

    def test_empty_and_all_null_series(self) -> None:
        """Kiểm tra xử lý chuỗi rỗng hoặc toàn giá trị null."""
        s_empty = pd.Series([], dtype=float)
        res_empty = compute_price_distribution_stats(s_empty)
        assert res_empty["n"] == 0
        assert res_empty["median"] is None
        assert res_empty["status"] == "EMPTY_SERIES"

        s_null = pd.Series([np.nan, None, "invalid"])
        res_null = compute_price_distribution_stats(s_null)
        assert res_null["n"] == 0
        assert res_null["status"] == "EMPTY_SERIES"

    def test_constant_series_zero_variance(self) -> None:
        """Kiểm tra xử lý chuỗi hằng số (phương sai bằng 0)."""
        s_const = pd.Series([100.0, 100.0, 100.0, 100.0])
        res = compute_price_distribution_stats(s_const)
        assert res["n"] == 4
        assert res["min"] == 100.0
        assert res["max"] == 100.0
        assert res["std"] == 0.0
        assert res["variance"] == 0.0
        assert res["cv_pct"] == 0.0
        assert res["iqr"] == 0.0
        assert res["skewness"] is None  # std = 0 thì không tính skewness
        assert res["kurtosis"] is None

    def test_small_sample_size_edge_cases(self) -> None:
        """Kiểm tra xử lý khi mẫu chỉ có 1 hoặc 2 phần tử."""
        # 1 phần tử
        s1 = pd.Series([50.0])
        res1 = compute_price_distribution_stats(s1)
        assert res1["n"] == 1
        assert res1["mean"] == 50.0
        assert res1["std"] is None
        assert res1["skewness"] is None

        # 2 phần tử
        s2 = pd.Series([40.0, 60.0])
        res2 = compute_price_distribution_stats(s2)
        assert res2["n"] == 2
        assert res2["mean"] == 50.0
        assert res2["std"] > 0
        assert res2["skewness"] is None  # n < 3


class TestRoomTypeStatsAndANOVA:
    """Kiểm thử thống kê nhóm loại phòng và kiểm định ANOVA."""

    @pytest.fixture
    def room_df(self) -> pd.DataFrame:
        """Tạo DataFrame mẫu với 3 loại phòng."""
        return pd.DataFrame(
            {
                "room_type": [
                    "Entire home/apt",
                    "Entire home/apt",
                    "Entire home/apt",
                    "Private room",
                    "Private room",
                    "Private room",
                    "Shared room",
                    "Shared room",
                    "Shared room",
                ],
                "price": [
                    2000.0,
                    2500.0,
                    3000.0,
                    1000.0,
                    1200.0,
                    1500.0,
                    300.0,
                    400.0,
                    500.0,
                ],
                "host_id": [1, 2, 3, 4, 1, 5, 6, 7, 8],
            }
        )

    def test_compute_room_type_stats(self, room_df: pd.DataFrame) -> None:
        """Kiểm tra tính toán thống kê theo từng nhóm loại phòng."""
        res = compute_room_type_stats(room_df)
        assert res["room_types_count"] == 3
        assert res["total_valid_observations"] == 9
        assert "Entire home/apt" in res["by_room_type"]
        assert res["by_room_type"]["Entire home/apt"]["median"] == 2500.0
        assert res["by_room_type"]["Shared room"]["median"] == 400.0

    def test_evaluate_anova_conditions(self, room_df: pd.DataFrame) -> None:
        """Kiểm tra hàm đánh giá điều kiện ANOVA phát hiện chính xác các tiêu chí."""
        cond = evaluate_anova_conditions(room_df)
        assert cond["status"] == "EVALUATED"
        assert "normality_evaluation" in cond
        assert "homoscedasticity_evaluation" in cond
        assert "sample_size_balance" in cond
        assert "independence_evaluation" in cond
        assert "scientific_recommendation" in cond

    def test_compute_anova_test_omnibus_and_pairwise(self, room_df: pd.DataFrame) -> None:
        """Kiểm tra tính toán ANOVA F-test tổng thể và cặp nhóm con."""
        res = compute_anova_test(room_df)
        assert res["status"] == "COMPUTED"
        assert "omnibus_test" in res
        assert res["omnibus_test"]["f_statistic"] > 0
        assert res["omnibus_test"]["p_value"] < 0.05
        assert res["pairwise_subgroup_tests"] == []  # Điều kiện chưa xác nhận, không tự so sánh cặp

    def test_anova_insufficient_groups(self) -> None:
        """Kiểm tra khi chỉ có 1 nhóm duy nhất."""
        single_df = pd.DataFrame({"room_type": ["Private room"] * 5, "price": [100.0] * 5})
        res = compute_anova_test(single_df)
        assert res["status"] == "INSUFFICIENT_GROUPS"


class TestPairwiseCorrelations:
    """Kiểm thử tính tương quan Pearson và xử lý ca biên (RQ3)."""

    def test_standard_pairwise_correlation(self) -> None:
        """Kiểm tra tương quan chuẩn giữa accommodates và price."""
        df = pd.DataFrame(
            {
                "accommodates": [1.0, 2.0, 3.0, 4.0, 5.0],
                "price": [500.0, 1000.0, 1500.0, 2000.0, 2500.0],
            }
        )
        res = compute_pairwise_correlations(df, feature_cols=["accommodates"], target_col="price")
        assert len(res) == 1
        row = res.iloc[0]
        assert row["n_valid"] == 5
        assert row["n_missing"] == 0
        assert row["pearson_r"] == pytest.approx(1.0, abs=1e-4)
        assert row["p_value"] < 0.001
        assert row["strength"] == "Mạnh (Strong)"
        assert row["status"] == "COMPUTED"

    def test_correlation_with_missing_values(self) -> None:
        """Kiểm tra xử lý khuyết từng cặp (pairwise complete cases)."""
        df = pd.DataFrame(
            {
                "bedrooms": [1.0, 2.0, np.nan, 4.0, 5.0],
                "price": [500.0, 1000.0, 1500.0, 2000.0, np.nan],
            }
        )
        res = compute_pairwise_correlations(df, feature_cols=["bedrooms"], target_col="price")
        row = res.iloc[0]
        assert row["n_total"] == 5
        assert row["n_valid"] == 3  # Chỉ có 3 cặp cùng không null
        assert row["n_missing"] == 2
        assert row["status"] == "COMPUTED"

    def test_correlation_constant_feature(self) -> None:
        """Kiểm tra khi biến độc lập là hằng số (phương sai bằng 0)."""
        df = pd.DataFrame(
            {
                "accommodates": [2.0, 2.0, 2.0, 2.0],
                "price": [100.0, 200.0, 300.0, 400.0],
            }
        )
        res = compute_pairwise_correlations(df, feature_cols=["accommodates"], target_col="price")
        row = res.iloc[0]
        assert row["status"] == "CONSTANT_FEATURE"
        assert row["pearson_r"] is None
        assert row["p_value"] is None


class TestNeighbourhoodPivot:
    """Kiểm thử bảng chéo 2D theo quận và loại phòng (RQ4)."""

    def test_compute_neighbourhood_pivot(self) -> None:
        """Kiểm tra tạo bảng pivot median, count, iqr và cảnh báo ô ít mẫu."""
        df = pd.DataFrame(
            {
                "neighbourhood_cleansed": ["Watthana", "Watthana", "Sathon", "Sathon", "Sathon"],
                "room_type": [
                    "Entire home/apt",
                    "Entire home/apt",
                    "Entire home/apt",
                    "Private room",
                    "Private room",
                ],
                "price": [2000.0, 2500.0, 1800.0, 800.0, 1000.0],
            }
        )
        p_med, p_cnt, p_iqr, meta = compute_neighbourhood_pivot(df, min_cell_sample_warning=2)

        assert p_med.shape == (2, 2)
        assert p_cnt.loc["Watthana", "Entire home/apt"] == 2
        assert p_cnt.loc["Watthana", "Private room"] == 0  # ô rỗng
        assert p_med.loc["Watthana", "Entire home/apt"] == 2250.0
        assert meta["districts_count"] == 2
        assert meta["empty_cells_count"] == 1


class TestLesson02Demonstration:
    """Kiểm thử minh họa kỹ thuật Bài 02 (Scaling, Binning, Dummy)."""

    def test_demonstrate_lesson02_wrangling(self) -> None:
        """Kiểm tra 3 phương pháp scaling, 2 phương pháp binning và mã hóa dummy."""
        df = pd.DataFrame(
            {
                "accommodates": [1, 2, 4, 8, 16],
                "price": [100.0, 200.0, 500.0, 1000.0, 50000.0],
                "room_type": [
                    "Entire home/apt",
                    "Private room",
                    "Entire home/apt",
                    "Shared room",
                    "Hotel room",
                ],
            }
        )
        res = demonstrate_lesson02_wrangling(df)

        assert res["status"] == "DEMONSTRATION_ONLY_NO_DATA_LEAKAGE"
        assert "scaling_summary" in res
        assert "binning_summary" in res
        assert len(res["dummy_columns_created"]) == 4


class TestFullEDAWorkflow:
    """Kiểm thử luồng thực thi run_full_eda và tính bất biến baseline."""

    def test_run_full_eda_pipeline(self, tmp_path: Path) -> None:
        """Kiểm tra chạy toàn bộ quy trình EDA và xuất 12 file kết quả máy đọc."""
        baseline_csv = tmp_path / "test_baseline.csv"
        df = pd.DataFrame(
            {
                "id": [1, 2, 3, 4],
                "host_id": [10, 20, 30, 40],
                "last_scraped": ["2026-06-29"] * 4,
                "price": [1000.0, 1500.0, 2000.0, 3000.0],
                "room_type": ["Entire home/apt", "Private room", "Entire home/apt", "Shared room"],
                "property_type": ["Condo", "Apartment", "Condo", "Hostel"],
                "neighbourhood_cleansed": ["Watthana", "Watthana", "Sathon", "Sathon"],
                "accommodates": [2.0, 1.0, 4.0, 1.0],
                "bedrooms": [1.0, 1.0, 2.0, np.nan],
                "bathrooms": [1.0, 1.0, 2.0, 1.0],
                "beds": [1.0, 1.0, 2.0, 1.0],
                "minimum_nights": [1.0, 2.0, 3.0, 1.0],
                "number_of_reviews": [10.0, 5.0, 20.0, 2.0],
                "review_scores_rating": [4.8, 4.5, 4.9, np.nan],
                "host_is_superhost": ["t", "f", "t", "f"],
                "price_raw": ["$1,000.00", "$1,500.00", "$2,000.00", "$3,000.00"],
            }
        )
        df.to_csv(baseline_csv, index=False)
        actual_hash = compute_sha256(baseline_csv)

        out_dir = tmp_path / "reports_stats"
        meta = run_full_eda(baseline_csv, out_dir, expected_sha256=actual_hash)

        assert (out_dir / "rq1_price_distribution.json").is_file()
        assert (out_dir / "rq2_room_type_stats.csv").is_file()
        assert (out_dir / "rq3_size_correlation.csv").is_file()
        assert (out_dir / "rq4_neighbourhood_pivot_median.csv").is_file()
        assert (out_dir / "eda_metadata.json").is_file()
        assert len(meta["artifacts_generated"]) == 12

    def test_run_full_eda_hash_mismatch_raises_error(self, tmp_path: Path) -> None:
        """Kiểm tra ném lỗi khi hash của baseline không khớp."""
        baseline_csv = tmp_path / "test_baseline.csv"
        baseline_csv.write_text("id,price\n1,100.0\n", encoding="utf-8")
        out_dir = tmp_path / "reports_stats"

        with pytest.raises(ValueError, match="Mã băm dữ liệu baseline không khớp"):
            run_full_eda(baseline_csv, out_dir, expected_sha256="0" * 64)
