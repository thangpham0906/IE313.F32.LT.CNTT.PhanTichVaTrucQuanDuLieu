"""Hồi quy cho các lỗi phát hiện khi review Bước 7, gồm cả nhánh khả thi."""

import json

import joblib
import numpy as np
import pandas as pd
import pytest
from sklearn.base import clone
from sklearn.model_selection import KFold

from src.modeling import (
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
    FoldSelectedRegressor,
    build_regression_pipeline,
    evaluate_mean_dummy_benchmark,
    run_cross_fold_feature_selection,
    run_full_modeling_workflow,
    select_features_for_fold,
    verify_baseline_data,
)


def test_validation_rejects_nonfinite_target_and_missing_id():
    """Không cho giá vô cực hoặc định danh khuyết qua cửa kiểm tra."""
    for target in [np.inf, -np.inf, np.nan, -1.0]:
        with pytest.raises(ValueError):
            verify_baseline_data(pd.DataFrame({"id": [1, 2], "price": [5, target]}), None)
    with pytest.raises(ValueError, match="khuyết"):
        verify_baseline_data(pd.DataFrame({"id": [1, None], "price": [5, 6]}), None)


def test_integer_benchmark_preserves_fractional_mean_and_undefined_r2():
    """np.full_like kiểu int từng làm mất phần lẻ của trung bình fold."""
    y = pd.Series([1, 2, 4, 8, 16, 32, 64, 128])
    kf = KFold(4, shuffle=True, random_state=42)
    result = evaluate_mean_dummy_benchmark(y, pd.Series([5, 5]), kf)
    expected = [np.mean((y.iloc[va] - y.iloc[tr].mean()) ** 2) for tr, va in kf.split(y)]
    assert result["cv_4fold_mse_by_fold"] == pytest.approx(expected)
    assert result["test_r2"] is None
    assert result["test_r2_reason"] == "CONSTANT_TARGET"
    constant = evaluate_mean_dummy_benchmark(pd.Series([3.0] * 8), pd.Series([3.0]), kf)
    assert constant["train_r2"] is None
    assert constant["cv_4fold_r2_mean"] is None
    json.dumps(constant, allow_nan=False)


def test_categorical_evidence_does_not_drop_singletons_or_invent_violations():
    """Ghi đúng nhóm ít mẫu, host của fold và mức chưa xác nhận."""
    X = pd.DataFrame({"room_type": ["a", "a", "b", "b", "c"]})
    y = pd.Series([1.0, 3.0, 1.0, 3.0, 20.0])
    hosts = pd.Series([1, 1, 2, 3, 4])
    row = select_features_for_fold(X, y, hosts=hosts)["categorical_features"]["room_type"]
    assert row["group_sizes"] == {"a": 2, "b": 2, "c": 1}
    assert row["groups_count"] == 3
    assert row["anova_status"] == "NOT_COMPUTABLE"
    assert row["f_statistic"] is None
    assert row["heteroscedasticity_detected"] is None
    assert row["condition_checks"]["independence_evaluation"]["multi_listing_hosts"] == 1
    assert row["reason"] == "ANOVA_ASSUMPTIONS_NOT_CONFIRMED_FOR_SELECTION"


def test_fold_estimator_refits_selection_and_imputation_on_training_rows():
    """Đối chiếu tham số imputer/scaler trực tiếp với các dòng train của mỗi fold."""
    rng = np.random.default_rng(42)
    X = pd.DataFrame({"accommodates": np.linspace(1.0, 50.0, 80), "bedrooms": np.nan})
    y = pd.Series(100.0 + 100.0 * X.accommodates + rng.normal(0, 0.1, len(X)))
    X.loc[4, "accommodates"] = np.nan
    kf = KFold(4, shuffle=True, random_state=42)
    prototype = FoldSelectedRegressor("ridge", 1.0)
    for tr, va in kf.split(X):
        model = clone(prototype).fit(X.iloc[tr], y.iloc[tr])
        num = model.pipeline_.named_steps["preprocessor"].named_transformers_["num"]
        median = X.iloc[tr].accommodates.median()
        assert num.named_steps["imputer"].statistics_[0] == pytest.approx(median)
        assert num.named_steps["scaler"].mean_[0] == pytest.approx(
            X.iloc[tr].accommodates.fillna(median).mean()
        )
        assert set(model.training_index_).isdisjoint(set(X.iloc[va].index))
        assert model.selected_features_ == ["accommodates"]
        assert np.isfinite(model.predict(X.iloc[va])).all()
        altered = X.iloc[va].copy()
        altered["accommodates"] = 100000
        model.predict(altered)
        assert num.named_steps["imputer"].statistics_[0] == pytest.approx(median)
    with pytest.raises(ValueError, match="cột cấm"):
        build_regression_pipeline(["price_raw"], [])


def test_feasible_workflow_trains_and_archives_old_artifacts_when_infeasible(tmp_path):
    """Nhánh khả thi phải fit thật; lần chạy sau không để mô hình cũ trông còn hiệu lực."""
    n = 80
    x = np.linspace(1.0, 20.0, n)
    df = pd.DataFrame({"id": np.arange(n), "host_id": np.arange(n), "price": 100.0 + 150.0 * x})
    for col in NUMERIC_FEATURES:
        df[col] = x if col == "accommodates" else 1.0
    for col in CATEGORICAL_FEATURES:
        df[col] = "one"
    source = tmp_path / "fixture.csv"
    df.to_csv(source, index=False)
    out = tmp_path / "output"
    meta = run_full_modeling_workflow(source, out, expected_sha256=None)
    assert meta["feasibility_decision"]["is_modeling_feasible"]
    assert len(meta["trained_models"]) == 9
    assert sum(row["test_mse"] is not None for row in meta["trained_models"]) == 1
    conditional = meta["conditional_artifacts"]
    model = joblib.load(conditional["best_pipeline_joblib"])
    diagnostic = np.load(conditional["model_diagnostics_npz"])
    test_frame = df.set_index("id").loc[diagnostic["test_ids"]]
    preds = model.predict(test_frame[NUMERIC_FEATURES + CATEGORICAL_FEATURES])
    np.testing.assert_allclose(preds, diagnostic["y_test_predicted"])
    np.testing.assert_array_equal(
        diagnostic["residuals"], diagnostic["y_test_actual"] - diagnostic["y_test_predicted"]
    )
    findings = (out / "modeling_findings.md").read_text()
    assert "28.987" not in findings
    assert "82.81%" not in findings
    assert "KHÔNG KHẢ THI" not in findings
    df["price"] = 500.0
    df.to_csv(source, index=False)
    second = run_full_modeling_workflow(source, out, expected_sha256=None)
    assert not second["feasibility_decision"]["is_modeling_feasible"]
    assert second["conditional_artifacts"]["best_pipeline_joblib"] is None
    assert len(second["conditional_artifacts"]["archived_previous_artifacts"]) == 5
    for path in out.glob("*.json"):
        json.loads(path.read_text(), parse_constant=lambda value: pytest.fail(value))


def test_validation_fold_targets_cannot_change_that_folds_selection():
    """Nhiễu mạnh ở validation không được lọt vào phép chọn biến của training fold đó."""
    rng = np.random.default_rng(42)
    X = pd.DataFrame({"accommodates": rng.uniform(1, 10, 120)})
    y = pd.Series(100 * X.accommodates + rng.normal(0, 1, len(X)))
    kf = KFold(4, shuffle=True, random_state=42)
    before = run_cross_fold_feature_selection(X, y, kf)
    _, val = next(kf.split(X))
    modified = y.copy()
    modified.iloc[val] = rng.uniform(1e6, 1e8, len(val))
    after = run_cross_fold_feature_selection(X, modified, kf)
    assert before["folds"]["fold_1"] == after["folds"]["fold_1"]
    assert before["full_train"] != after["full_train"]
