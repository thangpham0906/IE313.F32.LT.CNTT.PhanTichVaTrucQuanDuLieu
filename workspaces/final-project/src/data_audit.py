"""Module thực hiện kiểm toán toàn diện bộ dữ liệu Inside Airbnb Bangkok.

Thực hiện kiểm tra kích thước, toàn vẹn mã băm, trùng lặp định danh,
phân tích giá trị khuyết, xác minh tiền tệ và phân bố giá mục tiêu phục vụ đồ án IE313 (UIT - VNU-HCM).
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Đảm bảo thư mục gốc dự án có trong sys.path để hỗ trợ chạy trực tiếp
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import pandas as pd  # noqa: E402
from scipy import stats  # noqa: E402

from src.audit_markdown import generate_data_audit_markdown  # noqa: E402
from src.data_loader import compute_sha256, load_listings_data, parse_price_value  # noqa: E402

# 12 biến ứng viên được đề xuất trong đặc tả đồ án
CANDIDATE_FEATURES: list[str] = [
    "price",
    "room_type",
    "property_type",
    "neighbourhood_cleansed",
    "accommodates",
    "bedrooms",
    "bathrooms",
    "beds",
    "minimum_nights",
    "number_of_reviews",
    "review_scores_rating",
    "host_is_superhost",
]


def audit_dataset_structure(df: pd.DataFrame) -> dict[str, Any]:
    """Kiểm toán cấu trúc tổng thể, ô khuyết toàn bảng và tính đơn nhất của quan trắc."""
    total_rows, total_cols = df.shape
    total_cells = total_rows * total_cols
    total_missing_cells = int(df.isna().sum().sum())
    total_missing_cells_pct = (
        round((total_missing_cells / total_cells) * 100, 2) if total_cells > 0 else 0.0
    )

    complete_duplicates = int(df.duplicated().sum())

    id_exists = "id" in df.columns
    unique_ids = int(df["id"].nunique(dropna=True)) if id_exists else 0
    duplicate_ids = int(df.duplicated(subset=["id"]).sum()) if id_exists else 0

    dtype_counts = df.dtypes.astype(str).value_counts().to_dict()

    return {
        "total_rows": total_rows,
        "total_columns": total_cols,
        "total_cells": total_cells,
        "total_missing_cells": total_missing_cells,
        "total_missing_cells_pct": total_missing_cells_pct,
        "complete_duplicate_rows": complete_duplicates,
        "has_id_column": id_exists,
        "unique_ids_count": unique_ids,
        "duplicate_id_rows": duplicate_ids,
        "is_one_row_per_listing": bool(id_exists and unique_ids == total_rows),
        "dtype_counts": {str(k): int(v) for k, v in dtype_counts.items()},
    }


def audit_column_groups(df: pd.DataFrame) -> dict[str, Any]:
    """Phân loại 90 cột vào 8 nhóm nghiệp vụ chuẩn đảm bảo tổng bằng 90."""
    cols = df.columns.tolist()
    groups: dict[str, list[str]] = {
        "id_source": [],
        "host": [],
        "location": [],
        "property_room": [],
        "price_quotes": [],
        "availability_policy": [],
        "reviews": [],
        "estimates": [],
    }

    for c in cols:
        if c in [
            "id",
            "listing_url",
            "scrape_id",
            "last_scraped",
            "source",
            "picture_url",
            "license",
        ]:
            groups["id_source"].append(c)
        elif c.startswith("host") or c.startswith("calculated_host"):
            groups["host"].append(c)
        elif c in [
            "neighbourhood",
            "neighbourhood_cleansed",
            "neighbourhood_group_cleansed",
            "latitude",
            "longitude",
        ]:
            groups["location"].append(c)
        elif c in [
            "name",
            "description",
            "neighborhood_overview",
            "property_type",
            "room_type",
            "accommodates",
            "bathrooms",
            "bathrooms_text",
            "bedrooms",
            "beds",
            "amenities",
        ]:
            groups["property_room"].append(c)
        elif c == "price" or c.startswith("price_quote"):
            groups["price_quotes"].append(c)
        elif c in [
            "minimum_nights",
            "maximum_nights",
            "minimum_minimum_nights",
            "maximum_minimum_nights",
            "minimum_maximum_nights",
            "maximum_maximum_nights",
            "minimum_nights_avg_ntm",
            "maximum_nights_avg_ntm",
            "calendar_updated",
            "has_availability",
            "availability_30",
            "availability_60",
            "availability_90",
            "availability_365",
            "calendar_last_scraped",
            "availability_eoy",
            "instant_bookable",
        ]:
            groups["availability_policy"].append(c)
        elif (
            c.startswith("number_of_reviews")
            or c.startswith("review_scores")
            or c in ["first_review", "last_review", "reviews_per_month"]
        ):
            groups["reviews"].append(c)
        elif c.startswith("estimated_"):
            groups["estimates"].append(c)
        else:
            groups["property_room"].append(c)

    group_counts = {k: len(v) for k, v in groups.items()}
    return {
        "group_counts": group_counts,
        "total_columns_categorized": sum(group_counts.values()),
        "groups": groups,
    }


def audit_temporal_coverage(df: pd.DataFrame) -> dict[str, Any]:
    """Kiểm toán phạm vi thời gian thu thập dữ liệu qua cột last_scraped."""
    if "last_scraped" not in df.columns:
        return {"status": "COLUMN_NOT_FOUND"}

    dates_series = df["last_scraped"].dropna().astype(str)
    date_counts = dates_series.value_counts().to_dict()
    sorted_dates = sorted(date_counts.keys())

    return {
        "column": "last_scraped",
        "distinct_dates_count": len(sorted_dates),
        "earliest_date": sorted_dates[0] if sorted_dates else None,
        "latest_date": sorted_dates[-1] if sorted_dates else None,
        "date_distribution": {k: int(v) for k, v in date_counts.items()},
    }


def audit_price_field(df: pd.DataFrame, price_col: str = "price") -> dict[str, Any]:
    """Kiểm toán chi tiết biến giá mục tiêu: định dạng, khuyết, ngoại lai và thống kê."""
    if price_col not in df.columns:
        return {"status": "PRICE_COLUMN_NOT_FOUND"}

    total_rows = len(df)
    raw_series = df[price_col]
    raw_null_count = int(raw_series.isna().sum())

    parsed_series = raw_series.apply(parse_price_value)
    valid_count = int(parsed_series.notna().sum())
    invalid_or_missing_count = total_rows - valid_count

    valid_prices = parsed_series.dropna()
    if len(valid_prices) == 0:
        return {
            "total_rows": total_rows,
            "raw_null_count": raw_null_count,
            "raw_null_pct": round(raw_null_count / total_rows * 100, 2) if total_rows else 0.0,
            "valid_count": 0,
            "valid_pct": 0.0,
            "invalid_or_missing_count": invalid_or_missing_count,
            "zero_price_count": 0,
            "negative_price_count": 0,
            "error": "NO_VALID_PRICES_FOUND",
        }

    zero_count = int((valid_prices == 0).sum())
    negative_count = int((valid_prices < 0).sum())

    p_min = float(valid_prices.min())
    p_max = float(valid_prices.max())
    p_mean = float(valid_prices.mean())
    p_std = float(valid_prices.std())
    p_median = float(valid_prices.median())
    p_q1 = float(valid_prices.quantile(0.25))
    p_q3 = float(valid_prices.quantile(0.75))
    iqr = p_q3 - p_q1
    lower_bound = p_q1 - 1.5 * iqr
    upper_bound = p_q3 + 1.5 * iqr
    outliers_count = int(((valid_prices < lower_bound) | (valid_prices > upper_bound)).sum())

    skewness = (
        float(stats.skew(valid_prices))
        if valid_prices.nunique() > 1 and len(valid_prices) >= 3
        else float("nan")
    )
    kurtosis_val = (
        float(stats.kurtosis(valid_prices))
        if valid_prices.nunique() > 1 and len(valid_prices) >= 4
        else float("nan")
    )

    return {
        "total_rows": total_rows,
        "raw_null_count": raw_null_count,
        "raw_null_pct": round((raw_null_count / total_rows) * 100, 2),
        "valid_count": valid_count,
        "valid_pct": round((valid_count / total_rows) * 100, 2),
        "invalid_or_missing_count": invalid_or_missing_count,
        "zero_price_count": zero_count,
        "negative_price_count": negative_count,
        "descriptive_statistics": {
            "min": p_min,
            "q1": p_q1,
            "median": p_median,
            "mean": round(p_mean, 2),
            "std": round(p_std, 2),
            "q3": p_q3,
            "max": p_max,
            "iqr": round(iqr, 2),
            "outlier_bounds": {
                "lower_bound": round(lower_bound, 2),
                "upper_bound": round(upper_bound, 2),
            },
            "outliers_count_1_5_iqr": outliers_count,
            "outliers_pct": round((outliers_count / valid_count) * 100, 2)
            if valid_count > 0
            else 0.0,
            "skewness": round(skewness, 4),
            "kurtosis": round(kurtosis_val, 4),
        },
    }


def audit_currency_and_pricing_granularity(df: pd.DataFrame) -> dict[str, Any]:
    """Kiểm tra bằng chứng tiền tệ và kỳ lưu trú từ các trường quote phụ trợ."""
    evidence: dict[str, Any] = {
        "status": "ANALYZED",
        "has_price_quote_raw": "price_quote_raw" in df.columns,
        "has_price_quote_price_per_night": "price_quote_price_per_night" in df.columns,
        "has_price_quote_total_price": "price_quote_total_price" in df.columns,
        "findings": [],
    }

    # Đánh giá mẫu chuỗi quote thực tế
    if "price_quote_raw" in df.columns:
        raw_quotes = df["price_quote_raw"].dropna()
        evaluated_sample_size = min(100, len(raw_quotes))
        sample_quotes = raw_quotes.head(evaluated_sample_size)
        baht_symbol_count = 0
        json_error_count = 0

        for q_str in sample_quotes:
            try:
                q_obj = json.loads(q_str)
                # Kiểm tra ký hiệu Baht trong toàn bộ chuỗi quote
                if "฿" in q_str:
                    baht_symbol_count += 1
                elif isinstance(q_obj, dict):
                    # fallback kiểm tra trong line items
                    quote_dict = q_obj.get("quote", {})
                    items = quote_dict.get("raw_price_line_items", [])
                    if any("฿" in str(it.get("price_string", "")) for it in items):
                        baht_symbol_count += 1
            except (json.JSONDecodeError, TypeError):
                json_error_count += 1

        evidence["quote_sample_evaluated_count"] = evaluated_sample_size
        evidence["quote_sample_with_baht_symbol"] = baht_symbol_count
        evidence["quote_sample_json_errors"] = json_error_count
        if evaluated_sample_size > 0:
            evidence["findings"].append(
                f"Phát hiện ký hiệu '฿' (Thai Baht) trong {baht_symbol_count}/{evaluated_sample_size} mẫu chuỗi quote được đánh giá."
            )

    # Đối chiếu giá parse được với price_quote_price_per_night
    if "price_quote_price_per_night" in df.columns and "price" in df.columns:
        parsed_p = df["price"].apply(parse_price_value)
        quote_p = pd.to_numeric(df["price_quote_price_per_night"], errors="coerce")
        both_valid = parsed_p.notna() & quote_p.notna() & quote_p.map(math.isfinite)
        diff = (parsed_p[both_valid] - quote_p[both_valid]).abs()

        total_compared = int(both_valid.sum())
        exact_matches = int((diff == 0.0).sum())
        tolerance = 0.05
        tolerance_matches = int((diff <= tolerance).sum())
        max_diff = float(diff.max()) if total_compared > 0 else 0.0
        mean_diff = float(diff.mean()) if total_compared > 0 else 0.0

        evidence["price_vs_quote_per_night_comparison"] = {
            "total_compared": total_compared,
            "exact_matches": exact_matches,
            "exact_match_rate_pct": round((exact_matches / total_compared) * 100, 2)
            if total_compared > 0
            else 0.0,
            "tolerance_threshold": tolerance,
            "tolerance_matches": tolerance_matches,
            "tolerance_match_rate_pct": round((tolerance_matches / total_compared) * 100, 2)
            if total_compared > 0
            else 0.0,
            "max_difference": round(max_diff, 4),
            "mean_difference": round(mean_diff, 4),
        }
        if total_compared > 0 and exact_matches == total_compared:
            evidence["findings"].append(
                "Cột 'price' khớp chính xác 100% với 'price_quote_price_per_night' (đơn giá theo đêm)."
            )

    return evidence


def audit_candidate_variables(df: pd.DataFrame) -> dict[str, Any]:
    """Kiểm toán sự hiện diện, kiểu dữ liệu và tỷ lệ khuyết của 12 biến ứng viên."""
    total_rows = len(df)
    results: dict[str, Any] = {}

    for var in CANDIDATE_FEATURES:
        if var in df.columns:
            s = df[var]
            nulls = int(s.isna().sum())
            null_pct = round((nulls / total_rows) * 100, 2) if total_rows > 0 else 0.0
            results[var] = {
                "present": True,
                "dtype": str(s.dtype),
                "null_count": nulls,
                "null_pct": null_pct,
                "unique_count": int(s.nunique(dropna=True)),
                "sample_values": s.dropna().head(3).tolist(),
            }
        else:
            results[var] = {
                "present": False,
                "dtype": None,
                "null_count": None,
                "null_pct": None,
                "unique_count": None,
                "sample_values": [],
            }

    return results


def audit_host_clustering(df: pd.DataFrame) -> dict[str, Any]:
    """Kiểm toán hiện tượng tập trung chỗ ở theo chủ nhà (host clustering)."""
    if "host_id" not in df.columns:
        return {"status": "HOST_ID_NOT_FOUND"}

    host_series = df["host_id"].dropna()
    total_listings = len(host_series)
    unique_hosts = int(host_series.nunique(dropna=True))

    if unique_hosts == 0:
        return {
            "status": "NO_HOST_DATA",
            "total_listings_with_host": 0,
            "unique_hosts_count": 0,
            "multi_listing_hosts_count": 0,
            "multi_listing_hosts_pct": 0.0,
            "single_listing_hosts_count": 0,
            "single_listing_hosts_pct": 0.0,
            "max_listings_single_host": 0,
            "mean_listings_per_host": None,
            "median_listings_per_host": None,
            "top_5_hosts": {},
        }

    counts_per_host = host_series.value_counts()
    top_hosts = counts_per_host.head(5).to_dict()
    multi_listing_hosts = int((counts_per_host > 1).sum())
    single_listing_hosts = unique_hosts - multi_listing_hosts

    return {
        "total_listings_with_host": total_listings,
        "unique_hosts_count": unique_hosts,
        "multi_listing_hosts_count": multi_listing_hosts,
        "multi_listing_hosts_pct": round((multi_listing_hosts / unique_hosts) * 100, 2),
        "single_listing_hosts_count": single_listing_hosts,
        "single_listing_hosts_pct": round((single_listing_hosts / unique_hosts) * 100, 2),
        "max_listings_single_host": int(counts_per_host.max()),
        "mean_listings_per_host": round(float(counts_per_host.mean()), 2),
        "median_listings_per_host": float(counts_per_host.median()),
        "top_5_hosts": {str(k): int(v) for k, v in top_hosts.items()},
    }


def load_data_dictionary(
    dictionary_csv_path: str | Path | None = None,
) -> tuple[set[str], dict[str, str]]:
    """Đọc từ điển dữ liệu Inside Airbnb v4.3 (nếu có) để lấy mô tả chính thức của các trường."""
    if dictionary_csv_path is None:
        default_path = project_root / "docs" / "sources" / "inside_airbnb_data_dictionary_v4.3.csv"
        if default_path.is_file():
            dictionary_csv_path = default_path
        else:
            return set(), {}

    dict_path = Path(dictionary_csv_path)
    if not dict_path.is_file():
        return set(), {}

    try:
        df_dict = pd.read_csv(dict_path, header=7)
        if "Field" in df_dict.columns:
            valid_fields = df_dict.dropna(subset=["Field"]).copy()
            valid_fields["Field"] = valid_fields["Field"].astype(str).str.strip()
            dict_fields = set(valid_fields["Field"].tolist())

            descriptions: dict[str, str] = {}
            for _, row in valid_fields.iterrows():
                f = row["Field"]
                desc = row.get("Description", "")
                f_type = row.get("Type", "")
                if pd.notna(desc) and str(desc).strip():
                    descriptions[f] = str(desc).strip().replace("\n", " ")
                elif pd.notna(f_type) and str(f_type).strip():
                    descriptions[f] = (
                        f"Trường có trong từ điển v4.3 (kiểu dữ liệu: {str(f_type).strip()})"
                    )
                else:
                    descriptions[f] = "Trường có trong từ điển v4.3 (chưa có mô tả chi tiết)"
            return dict_fields, descriptions
    except Exception:
        return set(), {}
    return set(), {}


def generate_columns_catalog(
    df: pd.DataFrame, dictionary_csv_path: str | Path | None = None
) -> pd.DataFrame:
    """Tạo bảng danh mục thuộc tính 90 cột đối chiếu từ điển Inside Airbnb v4.3."""
    total_rows = len(df)
    dict_fields, data_dict = load_data_dictionary(dictionary_csv_path)
    records: list[dict[str, Any]] = []

    for idx, col in enumerate(df.columns, start=1):
        s = df[col]
        null_count = int(s.isna().sum())
        null_pct = round((null_count / total_rows) * 100, 2) if total_rows > 0 else 0.0
        unique_cnt = int(s.nunique(dropna=True))
        sample_val = str(s.dropna().iloc[0]) if not s.dropna().empty else ""
        if len(sample_val) > 40:
            sample_val = sample_val[:37] + "..."

        # Phân loại vai trò phân tích
        if col == "id":
            role = "Định danh quan trắc (ID)"
        elif col == "price":
            role = "Biến mục tiêu trung tâm (Target price)"
        elif col in CANDIDATE_FEATURES:
            role = "Biến ứng viên cốt lõi (Candidate feature)"
        elif col.startswith("price_quote_"):
            role = "Cột báo giá phụ trợ (Price quote auxiliary)"
        elif "url" in col:
            role = "Đường dẫn liên kết / hình ảnh (URL)"
        elif col.startswith("host") or col.startswith("calculated_host"):
            role = "Đặc trưng chủ nhà (Host metadata)"
        elif "review" in col:
            role = "Đánh giá & uy tín (Review metric)"
        elif "availability_" in col or "calendar_" in col or "nights" in col:
            role = "Lịch biểu & chính sách lưu trú (Policy/Availability)"
        elif col in ["latitude", "longitude", "neighbourhood", "neighbourhood_cleansed"]:
            role = "Địa lý & khu vực (Geographical)"
        else:
            role = "Đặc tính chỗ ở khác (Property metadata)"

        # Mô tả từ điển chính thức
        if col in dict_fields:
            dict_desc = data_dict.get(col, "Có trong từ điển v4.3")
            source_status = "Đã xác minh (Inside Airbnb Dictionary v4.3)"
        else:
            dict_desc = "Chưa có trong từ điển v4.3 (cột mới hoặc tính toán bổ sung)"
            source_status = "Chưa xác minh trong từ điển v4.3"

        records.append(
            {
                "stt": idx,
                "column_name": col,
                "data_type": str(s.dtype),
                "null_count": null_count,
                "null_pct": null_pct,
                "unique_values_count": unique_cnt,
                "sample_value": sample_val,
                "analytical_role": role,
                "dictionary_description": dict_desc,
                "source_status": source_status,
            }
        )

    return pd.DataFrame(records)


def json_safe(value: Any) -> Any:
    """Chuyển đại lượng không xác định thành null đúng chuẩn JSON."""
    if isinstance(value, dict):
        return {key: json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_safe(item) for item in value]
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def run_full_audit(
    raw_filepath: str | Path,
    output_dir: str | Path,
    expected_sha256: str | None = None,
    data_dictionary_path: str | Path | None = None,
    markdown_output_path: str | Path | None = None,
) -> dict[str, Any]:
    """Thực thi quy trình kiểm toán toàn diện, kiểm tra mã băm nghiêm ngặt và lưu kết quả."""
    path = Path(raw_filepath)
    if not path.is_file():
        raise FileNotFoundError(f"Không tìm thấy tệp dữ liệu thô: {raw_filepath}")

    print(f"[*] Đang tính toán mã băm SHA-256 cho: {path.name}...")
    actual_sha256 = compute_sha256(path)

    # Kiểm tra mã băm nghiêm ngặt trước khi tạo thư mục hoặc ghi file
    if expected_sha256 is not None and expected_sha256.strip():
        if actual_sha256.lower() != expected_sha256.strip().lower():
            raise ValueError(
                f"Mã băm SHA-256 không khớp!\n"
                f"  Kỳ vọng: {expected_sha256.strip().lower()}\n"
                f"  Thực tế: {actual_sha256.lower()}"
            )
        checksum_status = "MATCH"
        checksum_verified = True
    else:
        checksum_status = "NOT_CHECKED"
        checksum_verified = None

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("[*] Đang nạp dữ liệu thô vào bộ nhớ...")
    df = load_listings_data(path, parse_prices=False)

    print("[*] Đang kiểm toán cấu trúc dữ liệu và tính đơn nhất...")
    structure_info = audit_dataset_structure(df)
    column_groups_info = audit_column_groups(df)

    print("[*] Đang kiểm toán phạm vi thời gian cào dữ liệu...")
    temporal_info = audit_temporal_coverage(df)

    print("[*] Đang kiểm toán biến giá mục tiêu (price)...")
    price_info = audit_price_field(df, price_col="price")

    print("[*] Đang kiểm toán bằng chứng tiền tệ và kỳ lưu trú...")
    currency_info = audit_currency_and_pricing_granularity(df)

    print("[*] Đang kiểm toán 12 biến ứng viên...")
    candidates_info = audit_candidate_variables(df)

    print("[*] Đang kiểm toán phân bố chủ nhà (host clustering)...")
    host_info = audit_host_clustering(df)

    audit_summary: dict[str, Any] = {
        "audit_metadata": {
            "dataset_filename": path.name,
            "sha256": actual_sha256,
            "expected_sha256": expected_sha256,
            "checksum_status": checksum_status,
            "checksum_verified": checksum_verified,
            "file_size_bytes": path.stat().st_size,
            "audit_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        },
        "structure": structure_info,
        "column_groups": column_groups_info,
        "temporal_coverage": temporal_info,
        "price_audit": price_info,
        "currency_and_granularity": currency_info,
        "candidate_variables": candidates_info,
        "host_clustering": host_info,
    }

    audit_summary = json_safe(audit_summary)

    # Xuất JSON tổng hợp
    summary_path = out_dir / "bangkok_audit_summary.json"
    with summary_path.open("w", encoding="utf-8") as f:
        json.dump(audit_summary, f, ensure_ascii=False, indent=2, allow_nan=False)
    print(f"[✓] Đã xuất file JSON kiểm toán tổng hợp: {summary_path}")

    # Xuất CSV danh mục cột
    catalog_df = generate_columns_catalog(df, dictionary_csv_path=data_dictionary_path)
    catalog_path = out_dir / "bangkok_columns.csv"
    catalog_df.to_csv(catalog_path, index=False, encoding="utf-8")
    print(f"[✓] Đã xuất file CSV danh mục 90 cột: {catalog_path}")

    # Đồng bộ hoặc sinh Markdown phiếu kiểm toán nếu có yêu cầu
    if markdown_output_path:
        generate_data_audit_markdown(audit_summary, catalog_df, markdown_output_path)
        print(f"[✓] Đã đồng bộ tài liệu Markdown kiểm toán: {markdown_output_path}")

    return audit_summary


def main() -> None:
    """Điểm vào dòng lệnh (CLI) thực thi module kiểm toán dữ liệu."""
    parser = argparse.ArgumentParser(
        description="Kiểm toán dữ liệu Inside Airbnb Bangkok - Đồ án IE313"
    )
    parser.add_argument(
        "--input",
        type=str,
        default="data/raw/bangkok_listings_2026-06-29.csv.gz",
        help="Đường dẫn đến tệp dữ liệu thô (.csv.gz)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="reports/audit",
        help="Thư mục xuất báo cáo kiểm toán",
    )
    parser.add_argument(
        "--expected-sha256",
        type=str,
        default=None,
        help="Mã băm SHA-256 kỳ vọng (tùy chọn)",
    )
    parser.add_argument(
        "--manifest",
        type=str,
        default=None,
        help="Đường dẫn tệp source_manifest.json để nạp expected-sha256 tự động",
    )
    parser.add_argument(
        "--data-dictionary",
        type=str,
        default=None,
        help="Đường dẫn tệp CSV từ điển Inside Airbnb v4.3",
    )
    parser.add_argument(
        "--generate-markdown",
        type=str,
        default=None,
        help="Đường dẫn tệp Markdown để tự động sinh phiếu kiểm toán (ví dụ: docs/DATA_AUDIT.md)",
    )
    args = parser.parse_args()

    try:
        expected_sha = args.expected_sha256
        if args.manifest:
            manifest_data = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
            manifest_sha = manifest_data.get("sha256")
            if not isinstance(manifest_sha, str) or not re.fullmatch(
                r"[0-9a-fA-F]{64}", manifest_sha
            ):
                raise ValueError("Manifest phải chứa sha256 hợp lệ gồm 64 ký tự hex.")
            if expected_sha and expected_sha.lower() != manifest_sha.lower():
                raise ValueError("Checksum trên CLI mâu thuẫn với manifest.")
            expected_sha = manifest_sha
        run_full_audit(
            raw_filepath=args.input,
            output_dir=args.output_dir,
            expected_sha256=expected_sha,
            data_dictionary_path=args.data_dictionary,
            markdown_output_path=args.generate_markdown,
        )
    except ValueError as e:
        print(f"[LỖI KIỂM TOÁN] {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[LỖI HỆ THỐNG] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
