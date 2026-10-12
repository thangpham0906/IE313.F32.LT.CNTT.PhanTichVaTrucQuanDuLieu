"""Module tính toán thống kê mô tả, kiểm định và phân tích thăm dò dữ liệu (EDA).

Vận dụng kiến thức Bài 05 (EDA & Kiểm định thống kê), Bài 02 (Scaling, Binning, Dummy)
cho đồ án môn học IE313 (UIT - VNU-HCM) - Nhóm 10.
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

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy import stats  # noqa: E402

from src.data_audit import json_safe  # noqa: E402
from src.data_loader import compute_sha256  # noqa: E402

EXPECTED_BASELINE_SHA256 = "961a01ad225e35f989ec81f124925488e392baca2ef3800ff4028b4423d5f9a7"
SIZE_FEATURES = ["accommodates", "bedrooms", "bathrooms", "beds"]


def compute_price_distribution_stats(series: pd.Series) -> dict[str, Any]:
    """Tính toán toàn diện thống kê mô tả phân phối giá (RQ1).

    Xử lý an toàn mẫu nhỏ, mẫu hằng số và chuỗi rỗng/khuyết.
    """
    clean_s = finite_numeric(series).dropna()
    n = len(clean_s)

    if n == 0:
        return {
            "n": 0,
            "min": None,
            "max": None,
            "mean": None,
            "std": None,
            "variance": None,
            "cv_pct": None,
            "median": None,
            "mode": None,
            "q1": None,
            "q3": None,
            "iqr": None,
            "lower_bound": None,
            "upper_bound": None,
            "outliers_count": 0,
            "outliers_pct": 0.0,
            "skewness": None,
            "kurtosis": None,
            "status": "EMPTY_SERIES",
        }

    val_min = float(clean_s.min())
    val_max = float(clean_s.max())
    val_mean = float(clean_s.mean())
    val_median = float(clean_s.median())

    # Mode
    modes = clean_s.mode()
    val_mode = float(modes.iloc[0]) if not modes.empty else None

    # Phân vị & IQR
    val_q1 = float(clean_s.quantile(0.25))
    val_q3 = float(clean_s.quantile(0.75))
    val_iqr = val_q3 - val_q1
    lower_bound = val_q1 - 1.5 * val_iqr
    upper_bound = val_q3 + 1.5 * val_iqr
    outliers_count = int(((clean_s < lower_bound) | (clean_s > upper_bound)).sum())
    outliers_pct = round((outliers_count / n) * 100, 2)

    # Phương sai và độ lệch chuẩn
    if n >= 2:
        val_var = float(clean_s.var(ddof=1))
        val_std = float(clean_s.std(ddof=1))
        cv_pct = round((val_std / val_mean) * 100, 2) if val_mean != 0 else None
    else:
        val_var = None
        val_std = None
        cv_pct = None

    # Skewness và Kurtosis (yêu cầu n >= 3 cho skew, n >= 4 cho kurt)
    if n >= 3 and val_std > 0:
        val_skew = round(float(stats.skew(clean_s, bias=False)), 4)
    else:
        val_skew = None

    if n >= 4 and val_std > 0:
        val_kurt = round(float(stats.kurtosis(clean_s, bias=False)), 4)
    else:
        val_kurt = None

    return {
        "n": n,
        "min": val_min,
        "max": val_max,
        "mean": round(val_mean, 2),
        "std": round(val_std, 2) if val_std is not None else None,
        "variance": round(val_var, 2) if val_var is not None else None,
        "cv_pct": cv_pct,
        "median": round(val_median, 2),
        "mode": round(val_mode, 2) if val_mode is not None else None,
        "q1": round(val_q1, 2),
        "q3": round(val_q3, 2),
        "iqr": round(val_iqr, 2),
        "lower_bound": round(lower_bound, 2),
        "upper_bound": round(upper_bound, 2),
        "outliers_count": outliers_count,
        "outliers_pct": outliers_pct,
        "skewness": val_skew,
        "kurtosis": val_kurt,
        "status": "COMPUTED",
        "moment_estimator": "skew/kurtosis bias=False; Fisher excess kurtosis; variance/std ddof=1",
    }


def compute_room_type_stats(
    df: pd.DataFrame, room_type_col: str = "room_type", price_col: str = "price"
) -> dict[str, Any]:
    """Tính toán thống kê tóm tắt theo từng loại phòng (RQ2)."""
    if room_type_col not in df.columns or price_col not in df.columns:
        raise ValueError(f"Thiếu cột {room_type_col} hoặc {price_col} trong dữ liệu.")

    results: dict[str, Any] = {}
    df = finite_frame(df, [price_col])
    total_valid = len(df.dropna(subset=[room_type_col, price_col]))

    for r_type, grp in df.groupby(room_type_col):
        s = grp[price_col].dropna()
        st = compute_price_distribution_stats(s)
        st["group_n_pct"] = round((st["n"] / total_valid) * 100, 2) if total_valid > 0 else 0.0
        results[str(r_type)] = st

    return {
        "room_types_count": len(results),
        "total_valid_observations": total_valid,
        "by_room_type": results,
    }


def finite_numeric(series: pd.Series) -> pd.Series:
    """Chỉ giữ số hữu hạn; giá trị sai định dạng/vô cực chuyển về khuyết."""
    numeric = pd.to_numeric(series, errors="coerce")
    return numeric.where(np.isfinite(numeric))


def finite_frame(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Chuẩn hóa bản sao theo các cột cần cho phép tính, giữ nguyên đầu vào."""
    result = df.copy()
    for column in columns:
        result[column] = finite_numeric(result[column])
    return result


def evaluate_anova_conditions(
    df: pd.DataFrame, group_col: str = "room_type", val_col: str = "price"
) -> dict[str, Any]:
    """Chẩn đoán thăm dò; không chứng minh tính chuẩn/độc lập bằng skew hoặc p >= 0.05.

    [MỞ RỘNG NGOÀI BÀI HỌC] Levene center=median: chẩn đoán phương sai,
    không thay thế ANOVA hay tự xác nhận giả định. Nguồn và giới hạn: EDA_METHODS.md.
    """
    valid = finite_frame(df, [val_col]).dropna(subset=[group_col, val_col])
    grouped = list(valid.groupby(group_col, observed=True))
    if len(grouped) < 2:
        return {"status": "INSUFFICIENT_GROUPS", "all_parametric_assumptions_met": None}
    names = [str(name) for name, _ in grouped]
    groups = [group[val_col].to_numpy() for _, group in grouped]
    sizes = [len(group) for group in groups]
    shapes = {}
    for name, group in zip(names, groups, strict=True):
        sk = float(stats.skew(group, bias=False)) if len(group) >= 3 and np.std(group) > 0 else None
        shapes[name] = {
            "n": len(group),
            "skewness": sk,
            "severe_skew_warning": abs(sk) > 2 if sk is not None else None,
        }
    severe = any(info["severe_skew_warning"] for info in shapes.values())
    levene_stat = levene_p = None
    if min(sizes) >= 2 and any(np.ptp(group) > 0 for group in groups):
        stat, p_value = stats.levene(*groups, center="median")
        if np.isfinite(stat) and np.isfinite(p_value):
            levene_stat, levene_p = float(stat), float(p_value)
    variance_rejected = levene_p < 0.05 if levene_p is not None else None
    host_counts = (
        valid["host_id"].dropna().value_counts() if "host_id" in valid else pd.Series(dtype=int)
    )
    host_info = {
        "unique_hosts": len(host_counts),
        "multi_listing_hosts": int((host_counts > 1).sum()),
        "host_id_missing": int(valid["host_id"].isna().sum()) if "host_id" in valid else len(valid),
        "independence_confirmed": False,
        "note": "ID duy nhất không chứng minh độc lập; host clustering giới hạn diễn giải p-value.",
    }
    known_concerns = severe or variance_rejected is True or host_info["multi_listing_hosts"] > 0
    return {
        "status": "EVALUATED",
        "all_parametric_assumptions_met": False if known_concerns else None,
        "normality_evaluation": {
            "assumption_satisfied": False if severe else None,
            "by_group": shapes,
            "note": "|skew| > 2 chỉ là cảnh báo mô tả; skew nhỏ không xác nhận tính chuẩn.",
        },
        "homoscedasticity_evaluation": {
            "test": "[MỞ RỘNG NGOÀI BÀI HỌC] Levene (center=median)",
            "statistic": levene_stat,
            "p_value": levene_p,
            "equal_variance_assumption_satisfied": False if variance_rejected else None,
            "conclusion": "Có bằng chứng chống giả thuyết phương sai bằng nhau, với giới hạn độc lập."
            if variance_rejected
            else "Chưa đủ bằng chứng bác bỏ hoặc chưa tính được; không xác nhận phương sai bằng nhau.",
        },
        "sample_size_balance": {
            "group_sizes": dict(zip(names, sizes, strict=True)),
            "max_to_min_ratio": max(sizes) / min(sizes),
        },
        "independence_evaluation": host_info,
        "scientific_recommendation": "Chưa xác nhận mọi giả định; F/p chỉ minh họa thăm dò. Ưu tiên mô tả median/IQR; không suy rộng kiểm định hoặc kết luận nhân quả.",
    }


def compute_anova_test(
    df: pd.DataFrame, group_col: str = "room_type", val_col: str = "price"
) -> dict[str, Any]:
    """F/p tổng thể chỉ thăm dò; không tự chạy cặp khi giả định chưa xác nhận."""
    valid = finite_frame(df, [val_col]).dropna(subset=[group_col, val_col])
    groups = [group[val_col].to_numpy() for _, group in valid.groupby(group_col, observed=True)]
    if len(groups) < 2:
        return {"status": "INSUFFICIENT_GROUPS", "pairwise_subgroup_tests": []}
    conditions = evaluate_anova_conditions(df, group_col, val_col)
    result = {
        "status": "NOT_COMPUTABLE",
        "condition_checks": conditions,
        "pairwise_subgroup_tests": [],
        "pairwise_status": "SKIPPED_ASSUMPTIONS_NOT_CONFIRMED",
        "omnibus_test": {
            "f_statistic": None,
            "p_value": None,
            "significant_at_alpha": None,
            "alpha": 0.05,
            "caveat": "Chỉ thăm dò; chưa xác nhận đủ điều kiện suy luận.",
        },
    }
    if min(map(len, groups)) < 2 or not any(np.ptp(group) > 0 for group in groups):
        result["reason"] = "Mẫu nhóm dưới 2 hoặc toàn bộ phương sai nội nhóm bằng 0."
        return result
    stat, p_value = stats.f_oneway(*groups)
    if np.isfinite(stat) and np.isfinite(p_value):
        result["status"] = "COMPUTED"
        result["omnibus_test"].update(
            f_statistic=float(stat),
            p_value=float(p_value),
            significant_at_alpha=bool(p_value < 0.05),
        )
    return result


def compute_pairwise_correlations(
    df: pd.DataFrame,
    feature_cols: list[str] | None = None,
    target_col: str = "price",
) -> pd.DataFrame:
    """Tính toán hệ số tương quan tuyến tính Pearson r và p-value cho từng cặp đặc trưng quy mô (RQ3).

    Báo cáo rõ:
    - n_valid: Số lượng cặp mẫu hợp lệ (loại trừ khuyết theo cặp pairwise complete cases).
    - n_missing: Số lượng dòng bị khuyết ở biến độc lập tương ứng.
    - r: Hệ số tương quan Pearson r.
    - p_value: Giá trị p-value chính xác.
    - status: 'COMPUTED' hoặc 'CONSTANT_FEATURE' hoặc 'INSUFFICIENT_DATA'.
    """
    if feature_cols is None:
        feature_cols = SIZE_FEATURES

    records = []
    total_rows = len(df)

    for col in feature_cols:
        if col not in df.columns or target_col not in df.columns:
            records.append(
                {
                    "feature": col,
                    "target": target_col,
                    "n_total": total_rows,
                    "n_valid": 0,
                    "n_missing": total_rows,
                    "missing_pct": 100.0,
                    "pearson_r": None,
                    "p_value": None,
                    "strength": "NOT_AVAILABLE",
                    "status": "COLUMN_NOT_FOUND",
                }
            )
            continue

        pair_df = finite_frame(df[[col, target_col]], [col, target_col]).dropna()
        n_valid = len(pair_df)
        n_missing = total_rows - n_valid
        missing_pct = round((n_missing / total_rows) * 100, 2) if total_rows > 0 else 0.0

        if n_valid < 3:
            records.append(
                {
                    "feature": col,
                    "target": target_col,
                    "n_total": total_rows,
                    "n_valid": n_valid,
                    "n_missing": n_missing,
                    "missing_pct": missing_pct,
                    "pearson_r": None,
                    "p_value": None,
                    "strength": "INSUFFICIENT_DATA",
                    "status": "INSUFFICIENT_DATA",
                }
            )
            continue

        x_vals = pair_df[col].values
        y_vals = pair_df[target_col].values

        if np.std(x_vals) == 0 or np.std(y_vals) == 0:
            records.append(
                {
                    "feature": col,
                    "target": target_col,
                    "n_total": total_rows,
                    "n_valid": n_valid,
                    "n_missing": n_missing,
                    "missing_pct": missing_pct,
                    "pearson_r": None,
                    "p_value": None,
                    "strength": "NO_VARIANCE",
                    "status": "CONSTANT_FEATURE",
                }
            )
            continue

        r, pval = stats.pearsonr(x_vals, y_vals)
        r_val = float(r)
        p_val = float(pval)

        # Phân loại độ mạnh theo giáo trình Bài 05 p. 37
        abs_r = abs(r_val)
        if abs_r >= 0.70:
            strength = "Mạnh (Strong)"
        elif abs_r >= 0.30:
            strength = "Trung bình (Moderate)"
        else:
            strength = "Yếu (Weak)"

        records.append(
            {
                "feature": col,
                "target": target_col,
                "n_total": total_rows,
                "n_valid": n_valid,
                "n_missing": n_missing,
                "missing_pct": missing_pct,
                "pearson_r": round(r_val, 4),
                "p_value": p_val,
                "strength": strength,
                "status": "COMPUTED",
            }
        )

    return pd.DataFrame(records)


def compute_neighbourhood_pivot(
    df: pd.DataFrame,
    district_col: str = "neighbourhood_cleansed",
    room_type_col: str = "room_type",
    price_col: str = "price",
    min_cell_sample_warning: int = 5,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    """Xây dựng bảng chéo 2 chiều (2D Pivot Table) theo quận và loại phòng (RQ4).

    Trả về:
    1. pivot_median: Bảng trung vị giá (Median Price).
    2. pivot_count: Bảng số lượng mẫu n (Sample Count per cell).
    3. pivot_iqr: Bảng độ trải giữa (IQR per cell).
    4. summary_meta: Thống kê số lượng ô ít mẫu (low-n cells) để cảnh báo.
    """
    valid = finite_frame(df, [price_col]).dropna(subset=[district_col, room_type_col, price_col])

    def calc_iqr(s: pd.Series) -> float:
        clean = s.dropna()
        if len(clean) >= 2:
            return float(clean.quantile(0.75) - clean.quantile(0.25))
        return 0.0

    pivot_median = valid.pivot_table(
        index=district_col, columns=room_type_col, values=price_col, aggfunc="median"
    ).round(2)
    pivot_count = (
        valid.pivot_table(
            index=district_col, columns=room_type_col, values=price_col, aggfunc="count"
        )
        .fillna(0)
        .astype(int)
    )
    pivot_iqr = valid.pivot_table(
        index=district_col, columns=room_type_col, values=price_col, aggfunc=calc_iqr
    ).round(2)

    # Thống kê cảnh báo các ô ít mẫu
    low_n_cells = int(((pivot_count > 0) & (pivot_count < min_cell_sample_warning)).sum().sum())
    empty_cells = int((pivot_count == 0).sum().sum())
    total_cells = int(pivot_count.size)

    # Thống kê tổng hợp từng quận
    district_overall = (
        valid.groupby(district_col)[price_col]
        .agg(
            n="count",
            median="median",
            q1=lambda s: s.quantile(0.25),
            q3=lambda s: s.quantile(0.75),
            mean="mean",
            std="std",
        )
        .round(2)
    )
    district_overall["iqr"] = (district_overall["q3"] - district_overall["q1"]).round(2)

    summary_meta = {
        "districts_count": int(valid[district_col].nunique()),
        "room_types_count": int(valid[room_type_col].nunique()),
        "total_pivot_cells": total_cells,
        "empty_cells_count": empty_cells,
        "low_n_cells_count": low_n_cells,
        "min_cell_sample_warning_threshold": min_cell_sample_warning,
        "district_overall_summary": district_overall.to_dict(orient="index"),
    }

    return pivot_median, pivot_count, pivot_iqr, summary_meta


def demonstrate_lesson02_wrangling(df: pd.DataFrame) -> dict[str, Any]:
    r"""Minh họa các kỹ thuật tiền xử lý của Bài 02 trên một bản sao EDA cách ly hoàn toàn.

    Tuyệt đối không ghi đè lên baseline `bangkok_cleaned.csv` và không rò rỉ vào mô hình:
    1. 3 phương pháp Feature Scaling trên biến 'accommodates' và 'price':
       - Simple Feature Scaling ($x / x_{max}$)
       - Min-Max Normalization ($(x - x_{min}) / (x_{max} - x_{min})$)
       - Z-score Standardization ($(x - \mu) / \sigma$)
    2. Binning trên biến 'price':
       - Phân khoảng đều (Equal-width via pd.cut)
       - Phân khoảng theo phân vị (Quantile-based via pd.qcut)
    3. Mã hóa biến giả (One-Hot Encoding via pd.get_dummies) trên 'room_type'.
    """
    eda_sample = finite_frame(df, ["accommodates", "price"])

    # 1. Feature Scaling trên accommodates
    acc = eda_sample["accommodates"].dropna()
    acc_sfs = (acc / acc.max()).round(4)
    acc_minmax = ((acc - acc.min()) / (acc.max() - acc.min())).round(4)
    acc_zscore = ((acc - acc.mean()) / acc.std()).round(4)

    scaling_demo = pd.DataFrame(
        {
            "original_accommodates": acc,
            "simple_feature_scaling": acc_sfs,
            "min_max_scaling": acc_minmax,
            "z_score_standardization": acc_zscore,
        }
    )

    # 2. Binning trên price
    p = eda_sample["price"].dropna()
    # Phân khoảng đều 3 nhóm
    bins_eq = np.linspace(p.min(), p.max(), 4)
    binned_equal = (
        pd.cut(p, bins=bins_eq, labels=["Low", "Medium", "High"], include_lowest=True)
        if p.nunique() > 1
        else pd.Series(dtype="string")
    )

    # [MỞ RỘNG NGOÀI BÀI HỌC] qcut chỉ minh họa theo EDA_METHODS.md.
    quantile_counts, quantile_edges = {}, []
    try:
        binned_quantile, q_edges = pd.qcut(p, q=3, labels=["Low", "Medium", "High"], retbins=True)
        quantile_counts = {str(k): int(v) for k, v in binned_quantile.value_counts().items()}
        quantile_edges = [float(value) for value in q_edges]
    except ValueError:
        pass
    binning_demo = {
        "equal_width_bins_edges": [float(b) for b in bins_eq],
        "equal_width_counts": {str(k): int(v) for k, v in binned_equal.value_counts().items()},
        "quantile_bins_edges": quantile_edges,
        "quantile_counts": quantile_counts,
        "quantile_method_scope": "MỞ RỘNG NGOÀI BÀI HỌC; EDA_ONLY",
        "pedagogical_lesson": "Khoảng đều mô tả chiều rộng giá, phân vị hướng tới số quan sát cân bằng; không có cách tốt hơn cho mọi mục tiêu. Xem số đếm thực tế; không dùng price bins làm predictor.",
    }

    # 3. Dummy encoding trên room_type
    dummies = pd.get_dummies(eda_sample["room_type"], prefix="room_type", dtype=int)

    return {
        "status": "DEMONSTRATION_ONLY_NO_DATA_LEAKAGE",
        "scaling_summary": scaling_demo.describe().round(4).to_dict(),
        "binning_summary": binning_demo,
        "dummy_columns_created": dummies.columns.tolist(),
        "dummy_sample": dummies.head(5).to_dict(orient="records"),
    }


def run_full_eda(
    baseline_csv_path: str | Path,
    output_stats_dir: str | Path,
    expected_sha256: str | None = EXPECTED_BASELINE_SHA256,
) -> dict[str, Any]:
    """Thực thi quy trình tính toán thống kê EDA toàn diện và xuất các artifact máy đọc."""
    csv_path = Path(baseline_csv_path)
    if not csv_path.is_file():
        raise FileNotFoundError(f"Không tìm thấy tệp dữ liệu baseline: {baseline_csv_path}")

    actual_hash = compute_sha256(csv_path)
    if expected_sha256 and actual_hash.lower() != expected_sha256.strip().lower():
        raise ValueError(
            f"Mã băm dữ liệu baseline không khớp!\n"
            f"  Kỳ vọng: {expected_sha256}\n"
            f"  Thực tế: {actual_hash}"
        )

    out_dir = Path(output_stats_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(csv_path)

    print("[*] 1/5 Đang tính toán thống kê phân phối giá (RQ1)...")
    rq1_stats = compute_price_distribution_stats(df["price"])
    with (out_dir / "rq1_price_distribution.json").open("w", encoding="utf-8") as f:
        json.dump(json_safe(rq1_stats), f, ensure_ascii=False, indent=2, allow_nan=False)
    pd.DataFrame([rq1_stats]).to_csv(out_dir / "rq1_price_distribution.csv", index=False)

    print("[*] 2/5 Đang tính toán thống kê theo loại phòng & kiểm tra điều kiện ANOVA (RQ2)...")
    rq2_stats = compute_room_type_stats(df)
    with (out_dir / "rq2_room_type_stats.json").open("w", encoding="utf-8") as f:
        json.dump(json_safe(rq2_stats), f, ensure_ascii=False, indent=2, allow_nan=False)
    pd.DataFrame.from_dict(rq2_stats["by_room_type"], orient="index").to_csv(
        out_dir / "rq2_room_type_stats.csv"
    )

    rq2_anova = compute_anova_test(df)
    with (out_dir / "rq2_anova_condition_checks.json").open("w", encoding="utf-8") as f:
        json.dump(json_safe(rq2_anova), f, ensure_ascii=False, indent=2, allow_nan=False)

    print("[*] 3/5 Đang tính toán tương quan Pearson các biến quy mô (RQ3)...")
    rq3_corr = compute_pairwise_correlations(df)
    rq3_corr.to_csv(out_dir / "rq3_size_correlation.csv", index=False)
    with (out_dir / "rq3_size_correlation.json").open("w", encoding="utf-8") as f:
        json.dump(
            json_safe(rq3_corr.to_dict(orient="records")),
            f,
            ensure_ascii=False,
            indent=2,
            allow_nan=False,
        )

    print("[*] 4/5 Đang xây dựng bảng chéo 2D theo quận và loại phòng (RQ4)...")
    p_med, p_cnt, p_iqr, p_meta = compute_neighbourhood_pivot(df)
    p_med.to_csv(out_dir / "rq4_neighbourhood_pivot_median.csv")
    p_cnt.to_csv(out_dir / "rq4_neighbourhood_pivot_count.csv")
    p_iqr.to_csv(out_dir / "rq4_neighbourhood_pivot_iqr.csv")
    with (out_dir / "rq4_neighbourhood_summary.json").open("w", encoding="utf-8") as f:
        json.dump(json_safe(p_meta), f, ensure_ascii=False, indent=2, allow_nan=False)

    print("[*] 5/5 Đang thực hiện minh họa kỹ thuật Bài 02 (Scaling, Binning, Dummy)...")
    l02_demo = demonstrate_lesson02_wrangling(df)
    with (out_dir / "lesson02_wrangling_demo.json").open("w", encoding="utf-8") as f:
        json.dump(json_safe(l02_demo), f, ensure_ascii=False, indent=2, allow_nan=False)

    # Metadata tổng hợp kết quả
    meta_summary = {
        "eda_execution_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "baseline_file": csv_path.name,
        "baseline_sha256": actual_hash,
        "total_baseline_rows": len(df),
        "total_baseline_columns": len(df.columns),
        "methods_reference": "docs/EDA_METHODS.md",
        "moments": "bias=False, excess kurtosis, ddof=1; khác audit sơ bộ bias=True",
        "inference_scope": "EXPLORATORY_ONLY",
        "artifacts_generated": [
            "rq1_price_distribution.json",
            "rq1_price_distribution.csv",
            "rq2_room_type_stats.json",
            "rq2_room_type_stats.csv",
            "rq2_anova_condition_checks.json",
            "rq3_size_correlation.json",
            "rq3_size_correlation.csv",
            "rq4_neighbourhood_pivot_median.csv",
            "rq4_neighbourhood_pivot_count.csv",
            "rq4_neighbourhood_pivot_iqr.csv",
            "rq4_neighbourhood_summary.json",
            "lesson02_wrangling_demo.json",
        ],
    }
    with (out_dir / "eda_metadata.json").open("w", encoding="utf-8") as f:
        json.dump(json_safe(meta_summary), f, ensure_ascii=False, indent=2, allow_nan=False)

    print(
        f"[✓] Đã xuất bản thành công toàn bộ {len(meta_summary['artifacts_generated'])} tệp thống kê tại: {out_dir}"
    )
    return meta_summary


def main() -> None:
    """Điểm vào dòng lệnh (CLI) thực thi module tính toán EDA."""
    parser = argparse.ArgumentParser(
        description="Tính toán thống kê và kiểm định EDA - Đồ án IE313"
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
        default="reports/stats",
        help="Thư mục xuất các tệp thống kê JSON và CSV",
    )
    parser.add_argument(
        "--expected-sha256",
        type=str,
        default=EXPECTED_BASELINE_SHA256,
        help="Mã băm SHA-256 kỳ vọng của baseline",
    )
    args = parser.parse_args()

    try:
        run_full_eda(
            baseline_csv_path=args.input,
            output_stats_dir=args.output_dir,
            expected_sha256=args.expected_sha256,
        )
    except Exception as e:
        print(f"[LỖI THỰC THI EDA] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
