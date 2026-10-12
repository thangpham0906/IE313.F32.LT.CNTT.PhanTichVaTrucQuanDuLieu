"""Module thẩm định khả thi, chọn lọc đặc trưng và xây dựng mô hình hồi quy bổ trợ.

Tuân thủ nghiêm ngặt chuẩn mực học thuật:
- Ánh xạ Bài 06 (Phát triển mô hình hồi quy) & Bài 07 (Đánh giá và tinh chỉnh mô hình).
- Scikit-Learn Pipeline chống rò rỉ dữ liệu (Zero Data Leakage).
- Phân chia Train (70%) / Test (30%) với random_state=42 trước khi chọn biến.
- Chọn lọc đặc trưng độc lập trong từng training fold (Pearson |r| >= 0.30 & p < 0.05).
- Đánh giá điều kiện ANOVA cho biến phân loại; loại biến khi vi phạm giả định tham số.
- Xử lý trung thực tính không khả thi: Không hạ ngưỡng, không cắt tỉa dữ liệu để ép mô hình.
- Đánh giá mốc so sánh DummyRegressor (dự đoán trung bình y_train).

Đồ án môn học IE313 (UIT - VNU-HCM) - Nhóm 10.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Đảm bảo thư mục gốc dự án có trong sys.path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import platform  # noqa: E402
from importlib.metadata import version  # noqa: E402

import joblib  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy import stats  # noqa: E402
from sklearn.base import BaseEstimator, RegressorMixin  # noqa: E402
from sklearn.compose import ColumnTransformer  # noqa: E402
from sklearn.dummy import DummyRegressor  # noqa: E402
from sklearn.impute import SimpleImputer  # noqa: E402
from sklearn.linear_model import LinearRegression, Ridge  # noqa: E402
from sklearn.metrics import mean_squared_error, r2_score  # noqa: E402
from sklearn.model_selection import KFold, train_test_split  # noqa: E402
from sklearn.pipeline import Pipeline  # noqa: E402
from sklearn.preprocessing import OneHotEncoder, PolynomialFeatures, StandardScaler  # noqa: E402
from sklearn.utils.validation import check_is_fitted  # noqa: E402

from src.data_audit import json_safe  # noqa: E402
from src.data_loader import compute_sha256  # noqa: E402
from src.eda_stats import compute_anova_test, finite_numeric  # noqa: E402
from src.wrangling import MODEL_FEATURES  # noqa: E402

EXPECTED_BASELINE_SHA256 = "961a01ad225e35f989ec81f124925488e392baca2ef3800ff4028b4423d5f9a7"

NUMERIC_FEATURES = [
    "accommodates",
    "bedrooms",
    "bathrooms",
    "beds",
    "minimum_nights",
    "number_of_reviews",
    "review_scores_rating",
]

CATEGORICAL_FEATURES = [
    "room_type",
    "property_type",
    "neighbourhood_cleansed",
    "host_is_superhost",
]

FORBIDDEN_COLUMNS = [
    "id",
    "host_id",
    "last_scraped",
    "price_raw",
    "price_quote_checkin_date",
    "price_quote_checkout_date",
    "price_quote_total_price",
    "price_quote_price_per_night",
    "price_quote_raw",
    "estimated_occupancy_l365d",
    "estimated_revenue_l365d",
]

RIDGE_ALPHAS = [0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0]
PEARSON_R_THRESHOLD = 0.30
ALPHA_SIGNIFICANCE = 0.05
RANDOM_STATE = 42
TEST_SIZE = 0.30
N_SPLITS = 4


def verify_baseline_data(
    df: pd.DataFrame,
    expected_sha256: str | None = EXPECTED_BASELINE_SHA256,
    filepath: str | Path | None = None,
) -> bool:
    """Xác thực tính toàn vẹn của dữ liệu baseline trước khi xử lý."""
    if filepath is not None:
        p = Path(filepath)
        if not p.is_file():
            raise FileNotFoundError(f"Không tìm thấy tệp baseline: {filepath}")
        actual_hash = compute_sha256(p)
        if expected_sha256 and actual_hash.lower() != expected_sha256.strip().lower():
            raise ValueError(
                f"Mã băm dữ liệu baseline không khớp!\n"
                f"  Kỳ vọng: {expected_sha256}\n"
                f"  Thực tế: {actual_hash}"
            )

    if "price" not in df.columns:
        raise ValueError("Thiếu biến mục tiêu 'price' trong dữ liệu.")
    if "id" not in df.columns:
        raise ValueError("Thiếu cột định danh 'id' trong dữ liệu.")
    if df["id"].isna().any():
        raise ValueError("Cột id có giá trị khuyết.")
    if not df.index.is_unique:
        raise ValueError("Index phải duy nhất trước khi chia tập.")
    if df["id"].duplicated().any():
        raise ValueError("Cột 'id' có giá trị trùng lặp trong dữ liệu baseline.")
    price = pd.to_numeric(df["price"], errors="coerce")
    if (price <= 0).any() or not np.isfinite(price).all():
        raise ValueError("Cột 'price' chứa giá trị không hợp lệ (<= 0 hoặc NaN).")

    return True


def validate_feature_inputs(feature_cols: list[str]) -> None:
    """Kiểm tra danh sách đặc trưng đầu vào, từ chối tuyệt đối các cột rò rỉ hoặc cấm."""
    for col in feature_cols:
        if (
            col in FORBIDDEN_COLUMNS
            or col.startswith("price_quote_")
            or col.startswith("estimated_")
        ):
            raise ValueError(
                f"Phát hiện cột cấm hoặc gây rò rỉ dữ liệu trong tập đặc trưng: '{col}'"
            )
        if col not in MODEL_FEATURES:
            raise ValueError(
                f"Cột '{col}' không nằm trong danh sách MODEL_FEATURES cho phép: {MODEL_FEATURES}"
            )


def split_data(
    df: pd.DataFrame,
    test_size: float = TEST_SIZE,
    random_state: int = RANDOM_STATE,
    n_splits: int = N_SPLITS,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, pd.DataFrame, dict[str, Any]]:
    """Phân chia dữ liệu Train (70%) / Test (30%) theo listing và thiết lập KFold trên tập Train.

    Đồng thời phân tích mức độ giao thoa chủ nhà (host overlap) giữa hai tập.
    """
    verify_baseline_data(df, expected_sha256=None)
    validate_feature_inputs(MODEL_FEATURES)

    X = df[MODEL_FEATURES].copy()
    y = df["price"].astype(float).copy()
    ids = df["id"].copy()
    hosts = (
        df["host_id"].copy() if "host_id" in df.columns else pd.Series(index=df.index, dtype=object)
    )

    train_idx, test_idx = train_test_split(df.index, test_size=test_size, random_state=random_state)

    X_train = X.loc[train_idx].copy()
    X_test = X.loc[test_idx].copy()
    y_train = y.loc[train_idx].copy()
    y_test = y.loc[test_idx].copy()

    # Thiết lập 4-Fold KFold trên tập Train
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=random_state)
    train_fold_assignments = pd.Series(index=train_idx, dtype=int)
    for fold_num, (_, val_pos) in enumerate(kf.split(X_train)):
        val_orig_idx = train_idx[val_pos]
        train_fold_assignments.loc[val_orig_idx] = fold_num

    # Tạo bảng gán tập (split assignments) phục vụ lưu vết
    split_records = []
    for idx_val in df.index:
        row_id = ids.loc[idx_val]
        if idx_val in train_idx:
            split_name = "train"
            fold_val = int(train_fold_assignments.loc[idx_val])
        else:
            split_name = "test"
            fold_val = -1
        split_records.append({"id": row_id, "split": split_name, "fold": fold_val})

    split_df = pd.DataFrame(split_records)

    # Thống kê giao thoa chủ nhà (Host Overlap Analysis)
    train_host_set = set(hosts.loc[train_idx].dropna())
    test_host_set = set(hosts.loc[test_idx].dropna())
    overlap_hosts = train_host_set.intersection(test_host_set)
    test_listings_in_train_hosts = int(hosts.loc[test_idx].isin(train_host_set).sum())

    host_overlap_meta = {
        "total_hosts_train": len(train_host_set),
        "total_hosts_test": len(test_host_set),
        "overlapping_hosts_count": len(overlap_hosts),
        "overlapping_hosts_pct_of_test": (
            round((len(overlap_hosts) / len(test_host_set)) * 100, 2) if test_host_set else 0.0
        ),
        "test_listings_belonging_to_train_hosts": test_listings_in_train_hosts,
        "test_listings_belonging_to_train_hosts_pct": (
            round((test_listings_in_train_hosts / len(test_idx)) * 100, 2)
            if len(test_idx) > 0
            else 0.0
        ),
        "methodological_caveat": (
            f"{100 * test_listings_in_train_hosts / len(test_idx):.2f}% listing trong tập test thuộc về các chủ nhà đã xuất hiện trong tập train. "
            "Phân chia ngẫu nhiên theo listing chỉ đánh giá khả năng dự báo trên các chỗ ở mới "
            "trong cùng tập dữ liệu, KHÔNG đánh giá khả năng tổng quát hóa sang chủ nhà mới."
        ),
    }

    meta = {
        "n_total": len(df),
        "n_train": len(X_train),
        "n_test": len(X_test),
        "test_size_ratio": test_size,
        "random_state": random_state,
        "n_cv_splits": n_splits,
        "host_overlap": host_overlap_meta,
    }

    return X_train, X_test, y_train, y_test, split_df, meta


def select_features_for_fold(
    X_fold: pd.DataFrame,
    y_fold: pd.Series,
    r_threshold: float = PEARSON_R_THRESHOLD,
    alpha: float = ALPHA_SIGNIFICANCE,
    hosts: pd.Series | None = None,
) -> dict[str, Any]:
    """Thực hiện chọn lọc đặc trưng độc lập bên trong một training fold.

    - Biến số: Kiểm định Pearson |r| >= 0.30 VÀ p < 0.05 trên cặp hữu hạn hợp lệ.
    - Biến phân loại: Đánh giá giả định ANOVA; loại biến khi vi phạm phương sai đồng nhất hoặc phân phối.
    """
    validate_feature_inputs(list(X_fold.columns))
    if not X_fold.index.equals(y_fold.index):
        raise ValueError("Index X/y phải khớp để chọn biến.")
    numeric_results = {}
    selected_numeric = []

    for col in NUMERIC_FEATURES:
        if col not in X_fold.columns:
            numeric_results[col] = {
                "n_valid": 0,
                "pearson_r": None,
                "p_value": None,
                "selected": False,
                "reason": "COLUMN_NOT_IN_DATA",
            }
            continue

        pair_data = pd.DataFrame(
            {"x": finite_numeric(X_fold[col]), "y": finite_numeric(y_fold)}
        ).dropna()
        # Chỉ giữ số hữu hạn
        finite_mask = np.isfinite(pair_data["x"]) & np.isfinite(pair_data["y"])
        pair_data = pair_data.loc[finite_mask]
        n_valid = len(pair_data)

        if n_valid < 3:
            numeric_results[col] = {
                "n_valid": n_valid,
                "pearson_r": None,
                "p_value": None,
                "selected": False,
                "reason": "INSUFFICIENT_OBSERVATIONS",
            }
            continue

        x_vals = pair_data["x"].values
        y_vals = pair_data["y"].values

        if np.ptp(x_vals) == 0 or np.ptp(y_vals) == 0:
            numeric_results[col] = {
                "n_valid": n_valid,
                "pearson_r": None,
                "p_value": None,
                "selected": False,
                "reason": "ZERO_VARIANCE_CONSTANT_FEATURE",
            }
            continue

        r, p = stats.pearsonr(x_vals, y_vals)
        r_val = float(r)
        p_val = float(p)
        meets_criteria = bool(abs(r_val) >= r_threshold and p_val < alpha)

        if meets_criteria:
            selected_numeric.append(col)
            decision_reason = "MEETS_PEARSON_CRITERIA"
        else:
            if abs(r_val) < r_threshold:
                decision_reason = f"CORRELATION_TOO_WEAK (|r|={abs(r_val):.4f} < {r_threshold})"
            else:
                decision_reason = f"NOT_STATISTICALLY_SIGNIFICANT (p={p_val:.4f} >= {alpha})"

        numeric_results[col] = {
            "n_valid": n_valid,
            "pearson_r": r_val,
            "p_value": p_val,
            "selected": meets_criteria,
            "reason": decision_reason,
        }

    categorical_results = {}
    selected_categorical = []

    for col in CATEGORICAL_FEATURES:
        if col not in X_fold.columns:
            categorical_results[col] = {
                "groups_count": 0,
                "f_statistic": None,
                "p_value": None,
                "selected": False,
                "reason": "COLUMN_NOT_IN_DATA",
            }
            continue

        valid = pd.DataFrame({col: X_fold[col], "price": finite_numeric(y_fold)})
        if hosts is not None:
            if not hosts.index.equals(X_fold.index):
                raise ValueError("Index host phải khớp với training fold.")
            valid["host_id"] = hosts
        sizes = valid.dropna(subset=[col, "price"]).groupby(col, observed=True).size()
        result = compute_anova_test(valid, group_col=col)
        omnibus = result.get("omnibus_test", {})
        checks = result.get("condition_checks", {})
        levene = checks.get("homoscedasticity_evaluation", {})
        lev_p = levene.get("p_value")
        # Chính sách thận trọng: dữ liệu quan sát chưa xác nhận giả định suy luận.
        # Ghi UNKNOWN thay vì bịa vi phạm khi kiểm tra không phát hiện dấu hiệu.
        categorical_results[col] = {
            "groups_count": len(sizes),
            "group_sizes": {str(key): int(value) for key, value in sizes.items()},
            "n_valid": int(sizes.sum()),
            "f_statistic": omnibus.get("f_statistic"),
            "p_value": omnibus.get("p_value"),
            "anova_status": result["status"],
            "selected": False,
            "reason": "ANOVA_ASSUMPTIONS_NOT_CONFIRMED_FOR_SELECTION",
            "condition_checks": checks,
            "heteroscedasticity_detected": bool(lev_p < alpha) if lev_p is not None else None,
            "policy_note": "Chưa đủ cơ sở dùng ANOVA để chọn biến theo đặc tả; không kết luận biến không dự báo được.",
        }

    all_selected = selected_numeric + selected_categorical
    return {
        "numeric_features": numeric_results,
        "categorical_features": categorical_results,
        "selected_numeric": selected_numeric,
        "selected_categorical": selected_categorical,
        "all_selected_features": all_selected,
        "has_selected_features": len(all_selected) > 0,
    }


def run_cross_fold_feature_selection(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    kf: KFold,
    r_threshold: float = PEARSON_R_THRESHOLD,
    alpha: float = ALPHA_SIGNIFICANCE,
    hosts: pd.Series | None = None,
) -> dict[str, Any]:
    """Thực hiện chọn lọc đặc trưng trên từng fold CV và trên toàn bộ tập Train.

    Đánh giá tính khả thi: Nếu có bất kỳ fold nào không đủ biến, kết luận không khả thi.
    """
    folds_results: dict[str, Any] = {}
    folds_selected_counts = []

    for fold_num, (train_pos, _) in enumerate(kf.split(X_train), start=1):
        fold_key = f"fold_{fold_num}"
        X_fold_tr = X_train.iloc[train_pos]
        y_fold_tr = y_train.iloc[train_pos]

        res = select_features_for_fold(
            X_fold_tr,
            y_fold_tr,
            r_threshold=r_threshold,
            alpha=alpha,
            hosts=hosts.iloc[train_pos] if hosts is not None else None,
        )
        folds_results[fold_key] = res
        folds_selected_counts.append(len(res["all_selected_features"]))

    # Đánh giá trên toàn bộ tập Train
    full_train_res = select_features_for_fold(
        X_train, y_train, r_threshold=r_threshold, alpha=alpha, hosts=hosts
    )

    # Đánh giá tính khả thi tổng thể
    # Khả thi khi và chỉ khi: có ít nhất 1 biến được chọn ở toàn bộ các fold và full train
    all_folds_have_features = all(count > 0 for count in folds_selected_counts)
    full_train_has_features = full_train_res["has_selected_features"]
    is_feasible = bool(all_folds_have_features and full_train_has_features)

    if not is_feasible:
        empty_folds = [
            name for name, value in folds_results.items() if not value["has_selected_features"]
        ]
        infeasibility_reason = (
            f"Theo quy tắc |r|≥{r_threshold} và p<{alpha}, số biến chọn ở các fold là {folds_selected_counts}; "
            f"full train có {len(full_train_res['all_selected_features'])} biến. "
            f"Fold không có biến: {', '.join(empty_folds) or 'không có'}. "
            "Biến phân loại chưa được chọn do giả định dùng ANOVA chưa xác nhận; xem chẩn đoán từng biến/fold. "
            "Chưa triển khai hồi quy theo chính sách hiện tại; đây không phải chứng minh dữ liệu không thể mô hình hóa."
        )
    else:
        infeasibility_reason = None

    return {
        "is_modeling_feasible": is_feasible,
        "infeasibility_reason": infeasibility_reason,
        "r_threshold_used": r_threshold,
        "alpha_significance_used": alpha,
        "folds_selected_counts": folds_selected_counts,
        "full_train_selected_count": len(full_train_res["all_selected_features"]),
        "folds": folds_results,
        "full_train": full_train_res,
    }


def regression_metrics(actual, predicted) -> dict[str, Any]:
    """MSE và R² không làm tròn; R² không xác định được trả null kèm lý do."""
    actual = np.asarray(actual, dtype=float)
    predicted = np.asarray(predicted, dtype=float)
    if len(actual) == 0 or not np.isfinite(actual).all() or not np.isfinite(predicted).all():
        raise ValueError("Đánh giá cần mẫu hữu hạn, khác rỗng.")
    reason = (
        "TOO_FEW_OBSERVATIONS"
        if len(actual) < 2
        else "CONSTANT_TARGET"
        if np.ptp(actual) == 0
        else None
    )
    return {
        "mse": float(mean_squared_error(actual, predicted)),
        "r2": None if reason else float(r2_score(actual, predicted, force_finite=False)),
        "r2_reason": reason,
    }


def summarize_cv(scores: list[dict[str, Any]]) -> dict[str, Any]:
    """Không âm thầm bỏ fold có R² chưa xác định; std mô tả dùng ddof=0."""
    mses = [row["mse"] for row in scores]
    r2s = [row["r2"] for row in scores]
    all_defined = all(value is not None for value in r2s)
    return {
        "cv_4fold_mse_mean": float(np.mean(mses)),
        "cv_4fold_mse_std": float(np.std(mses)),
        "cv_4fold_mse_by_fold": mses,
        "cv_4fold_r2_mean": float(np.mean(r2s)) if all_defined else None,
        "cv_4fold_r2_std": float(np.std(r2s)) if all_defined else None,
        "cv_4fold_r2_by_fold": r2s,
        "cv_r2_reasons": [row["r2_reason"] for row in scores],
        "cv_n_splits": len(scores),
        "cv_std_ddof": 0,
    }


def evaluate_mean_dummy_benchmark(
    y_train: pd.Series, y_test: pd.Series, kf: KFold
) -> dict[str, Any]:
    """Dự đoán trung bình train; mỗi fold có trung bình riêng, không làm tròn artifact."""
    dummy = DummyRegressor(strategy="mean").fit(np.zeros((len(y_train), 1)), y_train)
    train = regression_metrics(y_train, dummy.predict(np.zeros((len(y_train), 1))))
    test = regression_metrics(y_test, dummy.predict(np.zeros((len(y_test), 1))))
    scores = []
    for train_pos, val_pos in kf.split(y_train):
        mean = float(y_train.iloc[train_pos].mean())
        scores.append(
            regression_metrics(y_train.iloc[val_pos], np.full(len(val_pos), mean, dtype=float))
        )
    return {
        "model_name": "DummyRegressor (Mean Benchmark - Bổ sung kỹ thuật)",
        "train_mean_prediction_thb": float(y_train.mean()),
        "train_mse": train["mse"],
        "train_r2": train["r2"],
        "train_r2_reason": train["r2_reason"],
        "test_mse": test["mse"],
        "test_r2": test["r2"],
        "test_r2_reason": test["r2_reason"],
        **summarize_cv(scores),
        "status": "COMPLETED_BENCHMARK",
    }


def build_regression_pipeline(
    selected_numeric: list[str],
    selected_categorical: list[str],
    model_type: str = "ridge",
    alpha: float = 1.0,
    degree: int = 1,
) -> Pipeline:
    """Xây dựng Scikit-Learn Pipeline chống rò rỉ dữ liệu (dùng khi có đặc trưng được chọn).

    Numeric: SimpleImputer(median) -> StandardScaler -> [PolynomialFeatures]
    Categorical: SimpleImputer(most_frequent) -> OneHotEncoder(ignore)
    Estimator: LinearRegression hoặc Ridge
    """
    validate_feature_inputs(selected_numeric + selected_categorical)
    transformers = []

    if selected_numeric:
        num_steps: list[tuple[str, Any]] = [
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
        if degree > 1:
            num_steps.append(("poly", PolynomialFeatures(degree=degree, include_bias=False)))
        transformers.append(("num", Pipeline(num_steps), selected_numeric))

    if selected_categorical:
        cat_steps: list[tuple[str, Any]] = [
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("ohe", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
        transformers.append(("cat", Pipeline(cat_steps), selected_categorical))

    if not transformers:
        raise ValueError("Không có đặc trưng nào để xây dựng Pipeline.")

    preprocessor = ColumnTransformer(transformers=transformers, remainder="drop")

    if model_type == "linear":
        estimator = LinearRegression()
    elif model_type == "ridge":
        estimator = Ridge(alpha=alpha, random_state=RANDOM_STATE)
    else:
        raise ValueError(f"Không hỗ trợ model_type: {model_type}")

    return Pipeline([("preprocessor", preprocessor), ("estimator", estimator)])


class FoldSelectedRegressor(RegressorMixin, BaseEstimator):
    """Bổ sung kỹ thuật: estimator chọn lại biến và fit Pipeline trên từng tập train."""

    def __init__(self, model_type="ridge", alpha=1.0, max_numeric=None):
        self.model_type = model_type
        self.alpha = alpha
        self.max_numeric = max_numeric

    def fit(self, X, y, hosts=None):
        """Không nhận validation/holdout vào bước fit chọn biến hoặc tiền xử lý."""
        y = pd.Series(np.asarray(y, dtype=float), index=X.index)
        self.selection_ = select_features_for_fold(X, y, hosts=hosts)
        numeric = self.selection_["selected_numeric"]
        if self.max_numeric is not None:
            numeric = sorted(
                numeric,
                key=lambda name: abs(self.selection_["numeric_features"][name]["pearson_r"]),
                reverse=True,
            )[: self.max_numeric]
        categorical = self.selection_["selected_categorical"]
        self.selected_features_ = numeric + categorical
        if not self.selected_features_:
            raise ValueError("Không có đặc trưng nào đạt tiêu chí trong tập train này.")
        self.pipeline_ = build_regression_pipeline(
            numeric, categorical, self.model_type, self.alpha
        )
        self.pipeline_.fit(self._prepare(X), y)
        self.n_features_in_ = X.shape[1]
        self.feature_names_in_ = np.asarray(X.columns, dtype=object)
        self.training_index_ = list(X.index)
        return self

    def _prepare(self, X):
        """Chuẩn hóa xác định; không học tham số từ dữ liệu đầu vào dự đoán."""
        validate_feature_inputs(list(X.columns))
        result = X.copy()
        for name in result.columns:
            if name in NUMERIC_FEATURES:
                result[name] = finite_numeric(result[name])
            else:
                result[name] = result[name].astype(object).where(result[name].notna(), np.nan)
        return result

    def predict(self, X):
        """Dùng lựa chọn biến và tham số đã fit trên train."""
        check_is_fitted(self, "pipeline_")
        return self.pipeline_.predict(self._prepare(X))


def fit_feasible_models(X_train, y_train, X_test, y_test, kf, hosts=None):
    """So sánh cấu hình trên cùng fold; chỉ đánh giá holdout cho cấu hình chọn qua CV."""
    configs = [("SLR", "linear", 0.0, 1), ("Linear", "linear", 0.0, None)]
    configs += [(f"Ridge alpha={alpha}", "ridge", alpha, None) for alpha in RIDGE_ALPHAS]
    rows = []
    for name, model_type, alpha, limit in configs:
        scores = []
        for train_pos, val_pos in kf.split(X_train):
            model = FoldSelectedRegressor(model_type, alpha, limit)
            model.fit(
                X_train.iloc[train_pos],
                y_train.iloc[train_pos],
                hosts=hosts.iloc[train_pos] if hosts is not None else None,
            )
            scores.append(
                regression_metrics(y_train.iloc[val_pos], model.predict(X_train.iloc[val_pos]))
            )
        rows.append(
            {
                "model_name": name,
                "model_type": model_type,
                "alpha": alpha,
                "max_numeric": limit,
                **summarize_cv(scores),
                "status": "CV_ONLY",
                "train_mse": None,
                "train_r2": None,
                "test_mse": None,
                "test_r2": None,
                "features_used": None,
            }
        )
    winner = min(range(len(rows)), key=lambda i: rows[i]["cv_4fold_mse_mean"])
    chosen = rows[winner]
    best = FoldSelectedRegressor(chosen["model_type"], chosen["alpha"], chosen["max_numeric"]).fit(
        X_train, y_train, hosts=hosts
    )
    prediction = best.predict(X_test)
    train_metrics = regression_metrics(y_train, best.predict(X_train))
    test_metrics = regression_metrics(y_test, prediction)
    chosen.update(
        {
            "status": "SELECTED_BY_CV",
            "features_used": ", ".join(best.selected_features_),
            "train_mse": train_metrics["mse"],
            "train_r2": train_metrics["r2"],
            "test_mse": test_metrics["mse"],
            "test_r2": test_metrics["r2"],
            "test_r2_reason": test_metrics["r2_reason"],
        }
    )
    return rows, best, prediction


def export_regression_artifacts(artifact_root, model, ids, actual, prediction):
    """Lưu estimator hoàn chỉnh và chẩn đoán thật, không ghi đè hình EDA."""
    import matplotlib.pyplot as plt

    model_path = artifact_root / "models/best_pipeline.joblib"
    diag_path = artifact_root / "reports/diagnostics/model_diagnostics.npz"
    figure_path = artifact_root / "reports/figures/model_diagnostics.png"
    for path in [model_path, diag_path, figure_path]:
        path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)
    actual = np.asarray(actual, dtype=float)
    prediction = np.asarray(prediction, dtype=float)
    residuals = actual - prediction
    np.savez(
        diag_path,
        test_ids=np.asarray(ids),
        y_test_actual=actual,
        y_test_predicted=prediction,
        residuals=residuals,
    )
    with plt.rc_context({"font.sans-serif": ["DejaVu Sans"], "axes.unicode_minus": False}):
        fig, axes = plt.subplots(1, 3, figsize=(15, 4), layout="constrained")
        axes[0].scatter(actual, prediction, s=9, alpha=0.45, label="Listing test")
        axes[0].set(
            title="Giá thực và dự đoán", xlabel="Giá thực (THB/đêm)", ylabel="Dự đoán (THB/đêm)"
        )
        axes[1].scatter(prediction, residuals, s=9, alpha=0.45, label="Phần dư test")
        axes[1].axhline(0, color="black", linestyle="--")
        axes[1].set(
            title="Chẩn đoán phần dư", xlabel="Dự đoán (THB/đêm)", ylabel="Phần dư (THB/đêm)"
        )
        bins = np.histogram_bin_edges(np.concatenate([actual, prediction]), bins=30)
        axes[2].hist(actual, bins=bins, alpha=0.5, label="Thực tế")
        axes[2].hist(prediction, bins=bins, alpha=0.5, label="Dự đoán")
        axes[2].set(title="Phân phối trên test", xlabel="Giá (THB/đêm)", ylabel="Số listing")
        for ax in axes:
            ax.legend()
        fig.savefig(figure_path, dpi=300)
        plt.close(fig)
    result = {
        "best_pipeline_joblib": str(model_path),
        "model_diagnostics_npz": str(diag_path),
        "diagnostic_figures": [str(figure_path)],
        "n_test": len(actual),
        "units": "THB/đêm",
        "model": model.model_type,
        "alpha": model.alpha,
        "interpretation": "Chẩn đoán trực quan; không xác nhận mọi giả định từ hình.",
        "dpi": 300,
    }
    (diag_path.parent / "model_diagnostics_meta.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    )
    (figure_path.parent / "model_figures_catalog.json").write_text(
        json.dumps([result], ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    )
    return result


def generate_model_comparison_table(
    benchmark_res: dict[str, Any],
    feasibility_info: dict[str, Any],
    trained_models_res: list[dict[str, Any]] | None = None,
) -> pd.DataFrame:
    """Tạo bảng so sánh mô hình và mốc cơ sở (model_comparison.csv)."""
    rows = []

    # 1. Mốc so sánh cơ sở DummyRegressor
    rows.append(
        {
            "model_name": benchmark_res["model_name"],
            "model_type": "Benchmark",
            "features_used": "None (y_train mean)",
            "train_mse": benchmark_res["train_mse"],
            "train_r2": benchmark_res["train_r2"],
            "cv_4fold_mse_mean": benchmark_res["cv_4fold_mse_mean"],
            "cv_4fold_r2_mean": benchmark_res["cv_4fold_r2_mean"],
            "test_mse": benchmark_res["test_mse"],
            "test_r2": benchmark_res["test_r2"],
            "status": benchmark_res["status"],
            "notes": "Mốc cơ sở tham chiếu (Baseline Comparator); liên hệ công thức R^2 Bài 06",
        }
    )

    # Nếu không khả thi: ghi nhận 4 mô hình học thuật với trạng thái KHÔNG KHẢ THI
    if not feasibility_info["is_modeling_feasible"]:
        reason_msg = feasibility_info["infeasibility_reason"]
        model_templates = [
            (
                "Simple Linear Regression (SLR - Bài 06)",
                "SLR",
                "NOT_FEASIBLE_NO_SELECTED_NUMERIC_FEATURES",
            ),
            (
                "Multiple Linear Regression (MLR - Bài 06)",
                "MLR",
                "NOT_FEASIBLE_NO_SELECTED_FEATURES",
            ),
            (
                "Polynomial Regression (Degree 2 - Bài 06)",
                "Poly-2",
                "NOT_FEASIBLE_NO_SELECTED_NUMERIC_FEATURES",
            ),
            (
                "Ridge Regression (alpha tuning - Bài 07)",
                "Ridge",
                "NOT_FEASIBLE_NO_SELECTED_FEATURES",
            ),
        ]
        for name, m_type, status_code in model_templates:
            rows.append(
                {
                    "model_name": name,
                    "model_type": m_type,
                    "features_used": "None",
                    "train_mse": None,
                    "train_r2": None,
                    "cv_4fold_mse_mean": None,
                    "cv_4fold_r2_mean": None,
                    "test_mse": None,
                    "test_r2": None,
                    "status": status_code,
                    "notes": reason_msg,
                }
            )
    elif trained_models_res:
        for m in trained_models_res:
            rows.append(m)

    return pd.DataFrame(rows)


def generate_modeling_findings_markdown(
    metadata, feasibility, benchmark, comparison_df, output_path=None
) -> str:
    """Sinh nhận xét từ artifact thực tế; không gán số hoặc kết luận cố định."""
    split = metadata["split_info"]
    ho = split["host_overlap"]

    def fmt(value):
        return "Không xác định" if value is None else f"{value:.8g}"

    lines = [
        "# Kết quả Bước 7 sau review",
        "",
        f"Nguồn: {metadata['dataset_baseline_filename']}; SHA-256 `{metadata['dataset_baseline_sha256']}`.",
        f"Train {split['n_train']:,}, test {split['n_test']:,}; seed {split['random_state']}; CV {split['n_cv_splits']} fold.",
        "",
        "## Chọn biến trong train/fold",
        "",
        "Ngưỡng số: |r|≥0,30 và p<0,05 theo repository. Biến phân loại chưa được chọn khi chưa có cơ sở dùng ANOVA làm bộ lọc. Đây là chính sách phân tích, không phải định lý về khả năng dự báo.",
        "",
        "| Biến số | n train | r train | p train | Được chọn |",
        "|---|---:|---:|---:|---|",
    ]
    for name, row in feasibility["full_train"]["numeric_features"].items():
        lines.append(
            f"| {name} | {row['n_valid']} | {fmt(row['pearson_r'])} | {fmt(row['p_value'])} | {row['selected']} |"
        )
    lines += [
        "",
        f"Số biến từng fold: {feasibility['folds_selected_counts']}; full train: {feasibility['full_train_selected_count']}.",
        "",
        "| Biến phân loại | Số nhóm | F thăm dò | p thăm dò | Trạng thái |",
        "|---|---:|---:|---:|---|",
    ]
    for name, row in feasibility["full_train"]["categorical_features"].items():
        lines.append(
            f"| {name} | {row['groups_count']} | {fmt(row['f_statistic'])} | {fmt(row['p_value'])} | {row.get('anova_status', row['reason'])} |"
        )
    lines += [
        "",
        "Các nhóm n=1 không bị âm thầm loại để tính lại ANOVA. N, skew, Levene và host trong từng training fold lưu tại `feature_selection.json`. **[MỞ RỘNG NGOÀI BÀI HỌC]** Levene center=median; nguồn/giới hạn tại `docs/EDA_METHODS.md`. Skew và mất cân đối chỉ là chẩn đoán, không tự chứng minh giả định đúng/sai.",
        "",
        "## Quyết định theo quy tắc hiện tại",
        "",
        feasibility["infeasibility_reason"]
        or "Có biến hợp lệ trên mọi training fold và toàn train; kết quả fit/CV nằm trong metadata.",
        "",
        "## Mốc dự đoán trung bình",
        "",
        f"Giá dự đoán cố định = {fmt(benchmark['train_mean_prediction_thb'])} THB/đêm. DummyRegressor là API bổ sung kỹ thuật; không thay thế hồi quy có predictor.",
        "",
        "| Thước đo | Train | CV mean ± std | Test |",
        "|---|---:|---:|---:|",
        f"| MSE (THB²) | {fmt(benchmark['train_mse'])} | {fmt(benchmark['cv_4fold_mse_mean'])} ± {fmt(benchmark['cv_4fold_mse_std'])} | {fmt(benchmark['test_mse'])} |",
        f"| R² | {fmt(benchmark['train_r2'])} | {fmt(benchmark['cv_4fold_r2_mean'])} ± {fmt(benchmark['cv_4fold_r2_std'])} | {fmt(benchmark['test_r2'])} |",
        "",
        "R² = 1 − SSE/SST với trung bình của chính tập đang đánh giá trong SST; mẫu hằng/ít hơn 2 trả null. CV std dùng ddof=0; không bỏ fold chưa xác định. Số đầy đủ trong JSON/CSV, chỉ làm tròn khi trình bày.",
        "",
        "## Giới hạn và sản phẩm",
        "",
        f"{ho['overlapping_hosts_count']:,} host giao hai tập; {ho['test_listings_belonging_to_train_hosts']:,} listing test thuộc host đã thấy ({ho['test_listings_belonging_to_train_hosts_pct']}%). {ho['methodological_caveat']}",
        "Các p-value mang tính thăm dò. Không suy ra tác động nhân quả, tính độc lập hay khả năng tổng quát sang host mới.",
        f"Sản phẩm hồi quy hiện hành: `{metadata['conditional_artifacts']}`.",
        "Bảng so sánh và trạng thái: `model_comparison.csv`; metadata có phiên bản môi trường. Phương pháp: `docs/MODELING_METHODS.md`.",
    ]
    result = "\n".join(lines) + "\n"
    if output_path:
        Path(output_path).write_text(result, encoding="utf-8")
    return result


def run_full_modeling_workflow(
    baseline_csv_path: str | Path,
    output_dir: str | Path,
    expected_sha256: str | None = EXPECTED_BASELINE_SHA256,
    random_state: int = RANDOM_STATE,
) -> dict[str, Any]:
    """Thực thi toàn bộ quy trình kiểm định khả thi mô hình hóa Bước 7."""
    csv_path = Path(baseline_csv_path)
    if not csv_path.is_file():
        raise FileNotFoundError(f"Không tìm thấy tệp baseline: {baseline_csv_path}")

    # 1. Xác thực baseline
    verify_baseline_data(pd.read_csv(csv_path), expected_sha256=expected_sha256, filepath=csv_path)
    df = pd.read_csv(csv_path)

    out_dir = Path(output_dir)
    if csv_path.parent.name in {"raw", "processed"} and out_dir.resolve().is_relative_to(
        csv_path.parent.resolve()
    ):
        raise ValueError("Không xuất báo cáo vào thư mục dữ liệu đầu vào.")
    out_dir.mkdir(parents=True, exist_ok=True)

    print("[*] 1/4 Đang phân chia dữ liệu Train (70%) / Test (30%) và thiết lập KFold (4 folds)...")
    X_train, X_test, y_train, y_test, split_df, split_meta = split_data(
        df, test_size=TEST_SIZE, random_state=random_state, n_splits=N_SPLITS
    )
    split_csv_path = out_dir / "split_assignments.csv"
    split_df.to_csv(split_csv_path, index=False)
    print(f"[✓] Đã xuất bản bảng gán tập: {split_csv_path}")

    # 2. Chọn lọc đặc trưng trong từng training fold
    print("[*] 2/4 Đang thực hiện chọn lọc đặc trưng độc lập trong từng training fold...")
    kf = KFold(n_splits=N_SPLITS, shuffle=True, random_state=random_state)
    feat_sel_results = run_cross_fold_feature_selection(
        X_train,
        y_train,
        kf=kf,
        r_threshold=PEARSON_R_THRESHOLD,
        alpha=ALPHA_SIGNIFICANCE,
        hosts=df.loc[X_train.index, "host_id"] if "host_id" in df else None,
    )
    feat_sel_json_path = out_dir / "feature_selection.json"
    with feat_sel_json_path.open("w", encoding="utf-8") as f:
        json.dump(json_safe(feat_sel_results), f, ensure_ascii=False, indent=2, allow_nan=False)
    print(f"[✓] Đã xuất bản kết quả chọn đặc trưng: {feat_sel_json_path}")

    # 3. Đánh giá mốc cơ sở DummyRegressor
    print("[*] 3/4 Đang đánh giá mốc cơ sở DummyRegressor (y_train mean benchmark)...")
    benchmark_res = evaluate_mean_dummy_benchmark(y_train, y_test, kf=kf)

    # 4. Xuất bảng so sánh mô hình và metadata
    print("[*] 4/4 Đang tổng hợp bảng so sánh mô hình và siêu dữ liệu...")
    trained_rows = None
    artifact_root = (
        out_dir.parent.parent
        if out_dir.name == "modeling" and out_dir.parent.name == "reports"
        else out_dir
    )
    conditional = {
        "best_pipeline_joblib": None,
        "model_diagnostics_npz": None,
        "diagnostic_figures": None,
        "status_explanation": "Chưa có hồi quy theo quy tắc chọn biến hiện tại; chỉ có mốc trung bình.",
    }
    if feat_sel_results["is_modeling_feasible"]:
        trained_rows, best, prediction = fit_feasible_models(
            X_train,
            y_train,
            X_test,
            y_test,
            kf,
            hosts=df.loc[X_train.index, "host_id"] if "host_id" in df else None,
        )
        conditional = export_regression_artifacts(
            artifact_root, best, df.loc[X_test.index, "id"], y_test, prediction
        )
    else:
        # Lưu trữ sản phẩm của lần chạy cũ thay vì để chúng trông như kết quả hiện hành.
        previous = []
        for name in [
            "models/best_pipeline.joblib",
            "reports/diagnostics/model_diagnostics.npz",
            "reports/diagnostics/model_diagnostics_meta.json",
            "reports/figures/model_diagnostics.png",
            "reports/figures/model_figures_catalog.json",
        ]:
            old = artifact_root / name
            if old.exists():
                archive = (
                    out_dir
                    / "previous_artifacts"
                    / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")
                    / old.name
                )
                archive.parent.mkdir(parents=True, exist_ok=True)
                old.rename(archive)
                previous.append(str(archive))
        conditional["archived_previous_artifacts"] = previous
    comp_df = generate_model_comparison_table(
        benchmark_res=benchmark_res,
        feasibility_info=feat_sel_results,
        trained_models_res=trained_rows,
    )
    comp_csv_path = out_dir / "model_comparison.csv"
    comp_df.to_csv(comp_csv_path, index=False)
    print(f"[✓] Đã xuất bản bảng so sánh mô hình: {comp_csv_path}")

    metadata = {
        "modeling_execution_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "dataset_baseline_filename": csv_path.name,
        "dataset_baseline_sha256": compute_sha256(csv_path),
        "random_state": random_state,
        "versions": {
            "python": platform.python_version(),
            **{
                package: version(package)
                for package in ["numpy", "pandas", "scipy", "scikit-learn"]
            },
        },
        "allowlist_features": MODEL_FEATURES,
        "forbidden_columns_enforced": FORBIDDEN_COLUMNS,
        "split_info": split_meta,
        "feasibility_decision": {
            "is_modeling_feasible": feat_sel_results["is_modeling_feasible"],
            "infeasibility_reason": feat_sel_results["infeasibility_reason"],
        },
        "benchmark_results": benchmark_res,
        "conditional_artifacts": conditional,
        "trained_models": trained_rows,
        "artifacts_generated": [
            "split_assignments.csv",
            "feature_selection.json",
            "model_comparison.csv",
            "modeling_metadata.json",
            "modeling_findings.md",
        ],
    }

    meta_json_path = out_dir / "modeling_metadata.json"
    with meta_json_path.open("w", encoding="utf-8") as f:
        json.dump(json_safe(metadata), f, ensure_ascii=False, indent=2, allow_nan=False)
    print(f"[✓] Đã xuất bản siêu dữ liệu mô hình: {meta_json_path}")

    # Sinh Markdown báo cáo phát hiện
    findings_md_path = out_dir / "modeling_findings.md"
    generate_modeling_findings_markdown(
        metadata=metadata,
        feasibility=feat_sel_results,
        benchmark=benchmark_res,
        comparison_df=comp_df,
        output_path=findings_md_path,
    )
    print(f"[✓] Đã xuất bản báo cáo phát hiện mô hình: {findings_md_path}")

    return metadata


def main() -> None:
    """Điểm vào dòng lệnh (CLI) thực thi module modeling."""
    parser = argparse.ArgumentParser(
        description="Đánh giá khả thi mô hình hồi quy Bước 7 - Đồ án IE313"
    )
    parser.add_argument(
        "--input",
        type=str,
        default="data/processed/bangkok_cleaned.csv",
        help="Đường dẫn đến tệp dữ liệu baseline cleaned",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="reports/modeling",
        help="Thư mục xuất các tệp báo cáo mô hình",
    )
    parser.add_argument(
        "--expected-sha256",
        type=str,
        default=EXPECTED_BASELINE_SHA256,
        help="Mã băm SHA-256 kỳ vọng của baseline",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=RANDOM_STATE,
        help="Hạt giống ngẫu nhiên (mặc định 42)",
    )
    args = parser.parse_args()

    try:
        run_full_modeling_workflow(
            baseline_csv_path=args.input,
            output_dir=args.output_dir,
            expected_sha256=args.expected_sha256,
            random_state=args.seed,
        )
    except Exception as e:
        print(f"[LỖI THỰC THI MODELING] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
