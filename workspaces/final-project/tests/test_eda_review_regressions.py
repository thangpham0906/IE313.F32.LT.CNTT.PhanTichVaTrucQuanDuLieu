"""Hồi quy lỗi khoa học của hình và giới hạn suy luận trong review Bước 5–6."""

import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest

from src.eda_stats import (
    compute_anova_test,
    compute_pairwise_correlations,
    compute_price_distribution_stats,
    evaluate_anova_conditions,
)
from src.visualization import (
    generate_figures_catalog,
    plot_room_type_comparison,
    plot_size_correlation,
    room_box_statistics,
    scatter_data,
)


def test_boxplot_quartiles_use_untrimmed_observations():
    """Giá cao phải góp vào hộp ngay cả khi ngoài giới hạn trục."""
    df = pd.DataFrame({"room_type": ["Private room"] * 5, "price": [100, 200, 300, 10000, 20000]})
    _, boxes = room_box_statistics(df)
    assert boxes[0]["med"] == 300 and boxes[0]["q3"] == 10000
    fig, axes = plot_room_type_comparison(df)
    # Đường trung vị trong kết quả bxp có y=[300,300], không phải median=200 của phần <=8000.
    assert any(
        np.allclose(line.get_ydata(), [300, 300])
        for line in axes[0].lines
        if len(line.get_ydata()) == 2
    )
    plt.close(fig)


def test_scatter_line_uses_same_full_pairs_as_correlation():
    """Giá ngoài khung vẫn tham gia OLS và số điểm thực vẽ được công bố đúng."""
    df = pd.DataFrame({"accommodates": [1, 2, 3, 4], "price": [100, 200, 300, 100000]})
    pair, shown, meta = scatter_data(df, "accommodates", sample_display_n=4)
    slope, intercept = np.polyfit(df.accommodates, df.price, 1)
    assert meta["trend"]["slope"] == pytest.approx(slope)
    assert (
        meta["trend"]["fit_n"] == 4
        and meta["n_displayed"] == 3
        and meta["selected_outside_axis"] == 1
    )
    assert len(pair) == 4 and len(shown) == 3
    fig, axes = plot_size_correlation(df, size_cols=["accommodates"], sample_display_n=4)
    line = axes[0].lines[0]
    np.testing.assert_allclose(line.get_ydata(), slope * line.get_xdata() + intercept)
    plt.close(fig)


def test_skew_and_nonsignificant_levene_do_not_certify_assumptions():
    """Các nhóm đối xứng vẫn không chứng minh chuẩn/độc lập; p>=.05 không chứng minh H0."""
    df = pd.DataFrame(
        {"room_type": ["a"] * 3 + ["b"] * 3, "price": [1, 2, 3, 1, 2, 3], "host_id": [1] * 6}
    )
    result = evaluate_anova_conditions(df)
    assert result["all_parametric_assumptions_met"] is False
    assert result["normality_evaluation"]["assumption_satisfied"] is None
    assert result["homoscedasticity_evaluation"]["equal_variance_assumption_satisfied"] is None
    assert compute_anova_test(df)["pairwise_subgroup_tests"] == []


def test_nonfinite_pairs_and_singleton_variance_are_not_fabricated():
    """Loại vô cực theo cặp, phương sai mẫu đơn là null, không phải 0."""
    df = pd.DataFrame({"x": [1, 2, 3, np.inf], "price": [2, 4, 6, 8]})
    result = compute_pairwise_correlations(df, ["x"]).iloc[0]
    assert result.n_valid == 3 and result.n_missing == 1
    assert result.pearson_r == pytest.approx(1)
    assert compute_price_distribution_stats(pd.Series([2.0, np.inf]))["variance"] is None
    for prices in [[1, 1, 2, 2], [1, 2]]:
        frame = pd.DataFrame(
            {"room_type": ["a"] * (len(prices) // 2) + ["b"] * (len(prices) // 2), "price": prices}
        )
        result = compute_anova_test(frame)
        assert result["status"] == "NOT_COMPUTABLE"
        json.dumps(result, allow_nan=False)


def test_catalog_uses_supplied_dataframe_and_real_axis_counts(tmp_path):
    """Catalog không gán n=28987 hoặc số IQR cho phần nằm ngoài trục."""
    df = pd.DataFrame(
        {
            "price": [100, 200, 300, 50000],
            "room_type": ["Private room"] * 4,
            "neighbourhood_cleansed": ["A"] * 4,
            **{k: [1, 2, 3, 4] for k in ["accommodates", "bedrooms", "bathrooms", "beds"]},
        }
    )
    cat = generate_figures_catalog(tmp_path, df=df).set_index("rq")
    assert cat.loc["RQ1", "sample_size_n"] == 4
    assert cat.loc["RQ1", "out_of_frame_notes"] == {"zoom_displayed": 3, "zoom_excluded": 1}
    assert cat.loc["RQ3", "out_of_frame_notes"]["accommodates"]["n_displayed"] == 3
