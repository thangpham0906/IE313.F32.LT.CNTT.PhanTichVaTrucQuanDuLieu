"""Làm sạch xác định trước; không fit imputer/scaler hay chọn biến trên toàn bộ dữ liệu."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from src.data_audit import CANDIDATE_FEATURES
from src.data_loader import compute_sha256, load_listings_data, parse_price_value

MODEL_FEATURES = [name for name in CANDIDATE_FEATURES if name != "price"]
CONTEXT_COLUMNS = ["id", "host_id", "last_scraped"]
NUMERIC_MINIMUMS = {
    "accommodates": 1,
    "bedrooms": 0,
    "bathrooms": 0,
    "beds": 0,
    "minimum_nights": 1,
    "number_of_reviews": 0,
    "review_scores_rating": 0,
}
INTEGER_COLUMNS = {"accommodates", "bedrooms", "beds", "minimum_nights", "number_of_reviews"}
CATEGORY_COLUMNS = ["room_type", "property_type", "neighbourhood_cleansed"]


def clean_listings(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any], pd.DataFrame]:
    """Trả dữ liệu chung, nhật ký và dòng bị loại; không biến đổi DataFrame đầu vào.

    Giá phải hữu hạn và dương. Không cắt ngưỡng giá dương, không điền khuyết.
    Chỉ loại dòng trùng toàn bộ; ID trùng nhưng nội dung khác phải dừng để rà soát.
    """
    required = CONTEXT_COLUMNS + CANDIDATE_FEATURES
    missing_columns = sorted(set(required) - set(df.columns))
    if missing_columns:
        raise ValueError(f"Thiếu cột bắt buộc: {missing_columns}")
    frame = df.copy(deep=True)
    before = len(frame)
    exact_duplicates = frame.duplicated()
    excluded = [
        {"id": row_id, "reason": "exact_duplicate"}
        for row_id in frame.loc[exact_duplicates, "id"].tolist()
    ]
    frame = frame.loc[~exact_duplicates].copy()
    if frame["id"].isna().any() or frame["id"].duplicated().any():
        raise ValueError("ID thiếu hoặc trùng khác nội dung; cần rà soát, không tự chọn một dòng.")

    parsed = frame["price"].map(parse_price_value).astype(float)
    raw_missing = frame["price"].isna() | frame["price"].astype("string").str.strip().eq("").fillna(
        False
    )
    reason_masks = {
        "missing_price": raw_missing,
        "invalid_price_format": parsed.isna() & ~raw_missing,
        "nonpositive_price": parsed.notna() & (parsed <= 0),
    }
    for reason, mask in reason_masks.items():
        excluded.extend(
            {"id": row_id, "reason": reason} for row_id in frame.loc[mask, "id"].tolist()
        )
    keep = parsed.notna() & (parsed > 0)
    frame["price_raw"] = frame["price"].astype("string")
    frame["price"] = parsed
    frame = frame.loc[keep, required + ["price_raw"]].copy()
    if frame.empty:
        raise ValueError("Không còn dòng có giá hữu hạn dương; chưa xuất dữ liệu processed.")

    changes: dict[str, Any] = {}
    for name, minimum in NUMERIC_MINIMUMS.items():
        original = frame[name]
        numeric = pd.to_numeric(original, errors="coerce").astype(float)
        invalid = ~np.isfinite(numeric) | (numeric < minimum)
        if name in INTEGER_COLUMNS:
            invalid |= numeric.notna() & (numeric % 1 != 0)
        changes[name] = {
            "invalid_observed_to_missing": int((original.notna() & invalid).sum()),
            "minimum_inclusive": minimum,
            "integer_required": name in INTEGER_COLUMNS,
        }
        frame[name] = numeric.mask(invalid)

    for name in CATEGORY_COLUMNS:
        frame[name] = frame[name].astype("string").str.strip().replace("", pd.NA)
    superhost = frame["host_is_superhost"].astype("string").str.strip().str.lower()
    changes["host_is_superhost"] = {
        "invalid_observed_to_missing": int((superhost.notna() & ~superhost.isin(["t", "f"])).sum())
    }
    frame["host_is_superhost"] = superhost.where(superhost.isin(["t", "f"]))
    frame = frame.reset_index(drop=True)
    exclusions = pd.DataFrame(excluded, columns=["id", "reason"])
    summary = {
        "rows_before": before,
        "exact_duplicates_removed": int(exact_duplicates.sum()),
        "rows_after": len(frame),
        "rows_removed": len(exclusions),
        "excluded_by_reason": {reason: int(mask.sum()) for reason, mask in reason_masks.items()},
        "predictor_changes": changes,
        "missing_after": {name: int(frame[name].isna().sum()) for name in required},
        "model_feature_allowlist": MODEL_FEATURES,
        "context_only_columns": CONTEXT_COLUMNS + ["price_raw"],
        "target": "price",
        "currency": "THB",
        "price_min_retained": float(frame["price"].min()),
        "price_max_retained": float(frame["price"].max()),
        "imputation_applied": False,
        "scaling_applied": False,
        "feature_selection_applied": False,
    }
    assert summary["rows_removed"] + summary["rows_after"] == before
    return frame, summary, exclusions


def price_outlier_report(frame: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Đánh dấu ngoại lệ 1,5 IQR chỉ cho EDA; không lọc dòng hay tạo predictor."""
    q1, q3 = frame["price"].quantile([0.25, 0.75])
    iqr = q3 - q1
    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    mask = (frame["price"] < lower) | (frame["price"] > upper)
    flagged = frame.loc[mask, ["id", "price", "room_type", "neighbourhood_cleansed"]].copy()
    flagged["review_reason"] = "outside_1_5_iqr_not_automatically_invalid"
    return flagged, {
        "q1": float(q1),
        "q3": float(q3),
        "lower_bound": float(lower),
        "upper_bound": float(upper),
        "flagged_count": int(mask.sum()),
        "removed_count": 0,
        "use": "EDA_ONLY",
    }


def run_cleaning(
    input_path: str | Path = "data/raw/bangkok_listings_2026-06-29.csv.gz",
    manifest_path: str | Path = "data/source_manifest.json",
    output_dir: str | Path = "data/processed",
    report_dir: str | Path = "reports/cleaning",
) -> dict[str, Any]:
    """Xác minh snapshot rồi xuất dữ liệu và nhật ký tái lập, giữ nguyên raw."""
    raw_path = Path(input_path)
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    expected = manifest.get("sha256", "")
    if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", expected):
        raise ValueError("Manifest thiếu sha256 hợp lệ.")
    actual = compute_sha256(raw_path)
    if actual.lower() != expected.lower():
        raise ValueError("Checksum dữ liệu thô không khớp manifest.")
    raw_stat = raw_path.stat()
    outputs = [Path(output_dir).resolve(), Path(report_dir).resolve()]
    for target in outputs:
        if target == raw_path.parent.resolve() or raw_path.parent.resolve() in target.parents:
            raise ValueError("Không xuất kết quả vào thư mục raw.")
    frame, summary, exclusions = clean_listings(load_listings_data(raw_path, parse_prices=False))
    outliers, iqr_summary = price_outlier_report(frame)
    summary.update(
        {
            "source_sha256": actual,
            "source_rows": summary["rows_before"],
            "outlier_review": iqr_summary,
        }
    )
    for target in outputs:
        target.mkdir(parents=True, exist_ok=True)
    processed_file = outputs[0] / "bangkok_cleaned.csv"
    frame.to_csv(processed_file, index=False)
    exclusions.to_csv(outputs[1] / "excluded_rows.csv", index=False)
    outliers.to_csv(outputs[1] / "price_outliers.csv", index=False)
    summary["processed_sha256"] = compute_sha256(processed_file)
    summary["processed_columns"] = frame.columns.tolist()
    (outputs[1] / "cleaning_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )
    if compute_sha256(raw_path) != actual or raw_path.stat().st_mtime_ns != raw_stat.st_mtime_ns:
        raise RuntimeError("Dữ liệu thô đã thay đổi trong khi chạy; không nghiệm thu kết quả.")
    return summary


def main() -> None:
    """Chạy bằng python -m src.wrangling từ gốc đồ án."""
    parser = argparse.ArgumentParser(description="Làm sạch Airbnb Bangkok theo CLEANING_PLAN.md")
    parser.add_argument("--input", default="data/raw/bangkok_listings_2026-06-29.csv.gz")
    parser.add_argument("--manifest", default="data/source_manifest.json")
    parser.add_argument("--output-dir", default="data/processed")
    parser.add_argument("--report-dir", default="reports/cleaning")
    args = parser.parse_args()
    summary = run_cleaning(args.input, args.manifest, args.output_dir, args.report_dir)
    print(
        json.dumps(
            {
                key: summary[key]
                for key in ["rows_before", "rows_after", "rows_removed", "outlier_review"]
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
