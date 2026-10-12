"""Sinh phiếu kiểm toán từ số liệu đã tính; không gán kết luận thiếu bằng chứng."""

from pathlib import Path
from typing import Any

import pandas as pd


def generate_data_audit_markdown(
    audit_summary: dict[str, Any],
    catalog_df: pd.DataFrame,
    output_markdown_path: str | Path | None = None,
) -> str:
    """Xuất 11 mục kiểm toán; giá trị không xác định hiển thị N/A."""
    meta = audit_summary["audit_metadata"]
    st = audit_summary["structure"]
    tc = audit_summary["temporal_coverage"]
    pa = audit_summary["price_audit"]
    cg = audit_summary["currency_and_granularity"]
    cv = audit_summary["candidate_variables"]
    hc = audit_summary["host_clustering"]
    ds = pa.get("descriptive_statistics", {})
    comp = cg.get("price_vs_quote_per_night_comparison", {})

    def fmt(value: Any) -> str:
        if value is None or (isinstance(value, float) and pd.isna(value)):
            return "N/A"
        if isinstance(value, int):
            return f"{value:,}"
        if isinstance(value, float):
            return f"{value:,.4f}".rstrip("0").rstrip(".")
        return str(value)

    def table(headers: list[str], rows: list[list[Any]]) -> str:
        return "\n".join(
            [
                "| " + " | ".join(headers) + " |",
                "| " + " | ".join(["---"] * len(headers)) + " |",
                *("| " + " | ".join(fmt(v) for v in row) + " |" for row in rows),
            ]
        )

    dictionary_count = int(
        catalog_df.get("source_status", pd.Series(dtype=str)).str.startswith("Đã xác minh").sum()
    )
    column_groups = audit_summary.get("column_groups", {}).get("group_counts", {})
    candidates = table(
        ["Biến", "Có mặt", "Kiểu", "Khuyết", "Khuyết (%)", "Giá trị duy nhất"],
        [
            [
                name,
                info.get("present"),
                info.get("dtype"),
                info.get("null_count"),
                info.get("null_pct"),
                info.get("unique_count"),
            ]
            for name, info in cv.items()
        ],
    )
    missing = catalog_df[catalog_df["null_count"] > 0]
    missing_table = table(
        ["Cột", "Số ô khuyết", "%"],
        missing[["column_name", "null_count", "null_pct"]].values.tolist(),
    )
    stat_names = {
        "min": "Min",
        "q1": "Q1",
        "median": "Trung vị",
        "mean": "Trung bình",
        "std": "Độ lệch chuẩn mẫu",
        "q3": "Q3",
        "max": "Max",
        "iqr": "IQR",
        "skewness": "Skewness",
        "kurtosis": "Kurtosis (excess)",
    }
    stat_table = table(
        ["Chỉ số", "Giá trị"], [[name, ds.get(key)] for key, name in stat_names.items()]
    )
    baht_count = cg.get("quote_sample_with_baht_symbol", 0)
    total_compared = comp.get("total_compared", 0)
    currency_text = (
        "Có bằng chứng ký hiệu ฿ phù hợp Thái Baht (THB) trong snapshot Bangkok; đối chiếu định nghĩa giá bằng tiền địa phương của từ điển."
        if baht_count
        else "Chưa đủ bằng chứng quote để xác minh Thái Baht (THB) từ dữ liệu này."
    )
    granularity_text = (
        "Toàn bộ cặp giá hữu hạn so sánh được khớp chính xác với báo giá theo đêm."
        if total_compared > 0 and comp.get("exact_matches") == total_compared
        else "Chưa xác nhận khớp hoàn toàn với báo giá theo đêm; xem số cặp và sai khác bên dưới."
    )
    observation_text = (
        "ID đầy đủ và duy nhất, phù hợp cấu trúc Listing Snapshot. Tính duy nhất không chứng minh độc lập thống kê."
        if st["total_rows"] > 0 and st.get("is_one_row_per_listing")
        else "Chưa xác nhận cấu trúc Listing Snapshot duy nhất; cần xử lý ID thiếu/trùng trước phân tích."
    )
    text = f"""# PHIẾU KIỂM TOÁN DỮ LIỆU THỰC TẾ

Nhóm 10 — IE313.F32.LT.CNTT — Phạm Quốc Thắng, Lê Minh Thiện.
Sinh tự động bởi `src/data_audit.py`; thời điểm UTC: {meta["audit_timestamp_utc"]}.
Nguồn số liệu: `reports/audit/bangkok_audit_summary.json` và `bangkok_columns.csv`.

## 1. Kích thước và toàn vẹn

- **Tổng số dòng (quan trắc)**: `{st["total_rows"]:,}` dòng.
- Số cột: {st["total_columns"]}; tổng số ô: {fmt(st["total_cells"])}.
- Tệp: `{meta["dataset_filename"]}`; dung lượng: {fmt(meta["file_size_bytes"])} bytes.
- SHA-256: `{meta["sha256"]}`; đối chiếu: **{meta["checksum_status"]}**.

## 2. Danh mục và ý nghĩa cột

Danh mục có {len(catalog_df)} cột; {dictionary_count} cột được đối chiếu với bản từ điển v4.3 lưu ở `docs/sources/`. Cột chưa có trong từ điển được ghi rõ trạng thái chưa xác minh.

{table(["Nhóm nghiệp vụ", "Số cột"], [[k, v] for k, v in column_groups.items()])}

## 3. Kiểu dữ liệu thực tế

{table(["Kiểu khi nạp", "Số cột"], [[k, v] for k, v in st["dtype_counts"].items()])}

Không suy diễn đơn vị tiền tệ chỉ từ ký hiệu `$`. Chuyển giá sang số bằng parser có kiểm tra định dạng.

## 4. Giá trị khuyết

Tổng {fmt(st["total_missing_cells"])}/{fmt(st["total_cells"])} ô khuyết ({st["total_missing_cells_pct"]}%). Không mặc định lý do thiếu rating là listing mới.

{missing_table}

## 5. Trùng lặp và đơn vị quan sát

{observation_text}
ID duy nhất: {fmt(st["unique_ids_count"])}; dòng trùng ID: {st["duplicate_id_rows"]}; dòng trùng toàn bộ: {st["complete_duplicate_rows"]}.
Ngày cào: {tc.get("earliest_date", "N/A")} đến {tc.get("latest_date", "N/A")}.

{table(["Ngày", "Số dòng"], [[k, v] for k, v in tc.get("date_distribution", {}).items()])}

## 6. Chất lượng và ngữ nghĩa giá

{currency_text}
Mẫu quote: {cg.get("quote_sample_evaluated_count", 0)} chuỗi đầu tiên không khuyết; có {baht_count} chuỗi mang ký hiệu ฿. Đây là mẫu thuận tiện, không phải mẫu ngẫu nhiên đại diện toàn bộ.

{granularity_text}
Cặp so sánh: {total_compared}; khớp chính xác: {comp.get("exact_matches", 0)} ({fmt(comp.get("exact_match_rate_pct"))}%); khớp trong dung sai {fmt(comp.get("tolerance_threshold"))}: {fmt(comp.get("tolerance_matches"))}; sai khác cực đại: {fmt(comp.get("max_difference"))}.
Chưa xác minh đầy đủ thuế/phí cuối cùng. Giá niêm yết không phải giá giao dịch thực tế hay doanh thu.

Giá parse được: {pa.get("valid_count", 0)}; khuyết hoặc không parse được: {pa.get("invalid_or_missing_count", "N/A")}; giá bằng 0: {pa.get("zero_price_count", "N/A")}; giá âm: {pa.get("negative_price_count", "N/A")}.

## 7. Phân bố giá sơ bộ

Thống kê trên {pa.get("valid_count", 0)} giá trị parse được, chưa cắt tỉa. Các chỉ số giá dùng đơn vị được kiểm chứng ở mục 6; skewness/kurtosis không có đơn vị. N/A là không đủ dữ liệu để tính.

{stat_table}

Ranh giới 1,5 IQR: {fmt(ds.get("outlier_bounds", {}).get("lower_bound"))} đến {fmt(ds.get("outlier_bounds", {}).get("upper_bound"))}; số ngoại lệ: {fmt(ds.get("outliers_count_1_5_iqr"))} ({fmt(ds.get("outliers_pct"))}%). Đây là dấu hiệu để kiểm tra, không phải tiêu chí tự động xóa.

## 8. Biến ứng viên

{candidates}

## 9. Khả thi và điều kiện kiểm nghiệm

Các RQ chỉ khả thi khi có mẫu hợp lệ ở những biến tương ứng. Pearson phải báo cáo n, r, p và xem tính tuyến tính; ANOVA cần xem số mẫu, phân bố, phương sai và giới hạn độc lập. Chưa có kết quả kiểm định tại bước kiểm toán này.

## 10. Ma trận RQ — phương pháp — biểu đồ

| RQ | Biến | Phương pháp | Biểu đồ | Giới hạn |
|---|---|---|---|---|
| RQ1: Phân bố giá | price | Thống kê mô tả, IQR (Bài 05) | Histogram, boxplot | Giữ cực trị; ghi rõ phạm vi trục |
| RQ2: Giá theo loại phòng | price, room_type | Groupby; ANOVA khi đủ điều kiện | Boxplot, bar trung vị | Nhóm mất cân đối; host clustering |
| RQ3: Quy mô và giá | price, accommodates, bedrooms, bathrooms, beds | Pearson r–p, mẫu cặp hợp lệ | Scatter, heatmap | Khuyết, phi tuyến, cực trị |
| RQ4: Giá theo khu vực | price, neighbourhood_cleansed, room_type | Groupby, pivot | Bar, heatmap | So sánh trong loại phòng; ghi n |

Nguồn phương pháp/trang PDF theo `SPECIFICATION.md` mục 1.3–1.4. Chưa chọn feature mô hình từ EDA toàn bộ dữ liệu.

## 11. Giới hạn và bàn giao

Số host: {fmt(hc.get("unique_hosts_count"))}; host có nhiều listing: {fmt(hc.get("multi_listing_hosts_count"))} ({fmt(hc.get("multi_listing_hosts_pct"))}%); nhiều nhất {fmt(hc.get("max_listings_single_host"))} listing/host. Không coi ID duy nhất là bằng chứng độc lập; các kiểm định thường chỉ dùng thăm dò, không kết luận nhân quả.

Giữ snapshot, không suy rộng thành xu hướng thời gian. Không dùng `price_quote_*`, doanh thu ước tính, ID/URL hoặc biến tạo từ giá làm predictor. Phần imputer/scaler/chọn biến phải fit trong training fold, sau chia tập. Phương án làm sạch tại `CLEANING_PLAN.md`; notebook 01 là bước tiếp theo sau kiểm toán kỹ thuật.

Nguồn: [Inside Airbnb](https://insideairbnb.com/get-the-data/), [Data Dictionary v4.3](https://docs.google.com/spreadsheets/d/1iWCNJcSutYqpULSQHlNyGInUvHg2BoUGoNRIGa6Szc4/edit), [Data Assumptions](https://insideairbnb.com/data-assumptions/). Tọa độ nguồn được làm nhiễu, không dùng phân tích khoảng cách trong phạm vi đồ án.
"""
    if output_markdown_path:
        path = Path(output_markdown_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return text
