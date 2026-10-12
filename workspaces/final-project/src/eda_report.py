"""Sinh nhận xét EDA có số liệu truy về JSON; không nhập tay các số thay đổi."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


def generate_findings(project: str | Path = ".") -> str:
    """Đọc artifact đã chạy, trình bày bốn RQ và giới hạn cùng nguồn phương pháp."""
    root = Path(project)

    def read(name):
        return json.loads((root / "reports/stats" / name).read_text())

    rq1 = read("rq1_price_distribution.json")
    rooms = read("rq2_room_type_stats.json")["by_room_type"]
    anova = read("rq2_anova_condition_checks.json")
    correlations = read("rq3_size_correlation.json")
    district = read("rq4_neighbourhood_summary.json")
    catalog = json.loads((root / "reports/figures/figures_catalog.json").read_text())
    metadata = read("eda_metadata.json")
    hosts = anova["condition_checks"]["independence_evaluation"]
    lev = anova["condition_checks"]["homoscedasticity_evaluation"]
    med = pd.read_csv(root / "reports/stats/rq4_neighbourhood_pivot_median.csv", index_col=0)
    count = pd.read_csv(root / "reports/stats/rq4_neighbourhood_pivot_count.csv", index_col=0)
    room = "Entire home/apt"
    within = pd.DataFrame({"median": med[room], "n": count[room]})
    eligible = within[within.n >= 20].sort_values("median")
    selected = pd.concat([eligible.head(3), eligible.tail(3)])
    selected = selected.loc[~selected.index.duplicated()]
    room_rows = "\n".join(
        f"| {name} | {item['n']:,} | {item['median']:,.2f} | {item['q1']:,.2f}–{item['q3']:,.2f} |"
        for name, item in rooms.items()
    )
    corr_rows = "\n".join(
        f"| {row['feature']} | {row['n_valid']:,} | {row['pearson_r']:+.4f} | {row['p_value']:.3e} |"
        for row in correlations
    )
    district_rows = "\n".join(
        f"| {name} | {int(row.n):,} | {row['median']:,.2f} |" for name, row in selected.iterrows()
    )
    catalog_rows = "\n".join(
        f"| {row['figure_filename']} | {row['rq']} | {row['chart_type']} |" for row in catalog
    )
    zoom = catalog[0]["out_of_frame_notes"]
    text = f"""# Phát hiện EDA — Nhóm 10

Bản cập nhật sau review ngày 11/10/2026. Sinh từ artifact máy đọc bằng `src/eda_report.py`.
Baseline: {metadata["total_baseline_rows"]:,} × {metadata["total_baseline_columns"]}; SHA-256 `{metadata["baseline_sha256"]}`.
Phương pháp, tham số, nguồn và phần mở rộng: [EDA_METHODS.md](../docs/EDA_METHODS.md).

## 1. RQ1 — Giá phân bố lệch phải

Trên n={rq1["n"]:,}, giá trung vị **{rq1["median"]:,.2f} THB/đêm**, trung bình {rq1["mean"]:,.2f}; Q1–Q3 là {rq1["q1"]:,.2f}–{rq1["q3"]:,.2f}; min–max {rq1["min"]:,.2f}–{rq1["max"]:,.2f}. Std mẫu {rq1["std"]:,.2f}, CV {rq1["cv_pct"]}%; skewness {rq1["skewness"]} và excess kurtosis {rq1["kurtosis"]} dùng bias=False. Các moment này khác audit sơ bộ bias=True, không trộn số liệu.

Có {rq1["outliers_count"]:,} ngoại lệ 1,5 IQR ({rq1["outliers_pct"]}%); giữ nguyên để rà soát. Trung vị/IQR ít nhạy với cực trị hơn mean/std; chưa xác minh các mức giá cực đoan là lỗi hay loại listing cụ thể. Giá niêm yết không đồng nghĩa giá giao dịch.

Hình RQ1 có toàn miền và panel ≤10.000 THB: **{zoom["zoom_displayed"]:,}** quan sát trong vùng, **{zoom["zoom_excluded"]:,}** ngoài vùng. Số này khác số ngoại lệ IQR. Nguồn: `rq1_price_distribution.json`, `fig1_price_distribution.png`.

## 2. RQ2 — Giá theo loại phòng

| Loại phòng | n | Trung vị THB/đêm | Q1–Q3 THB/đêm |
|---|---|---|---|
{room_rows}

ANOVA tổng thể thăm dò: F={anova["omnibus_test"]["f_statistic"]:.4f}, p={anova["omnibus_test"]["p_value"]:.6g}. **Chưa xác nhận các điều kiện suy luận**: phân bố lệch, cỡ nhóm mất cân đối và {hosts["multi_listing_hosts"]:,}/{hosts["unique_hosts"]:,} host trong baseline có nhiều listing. Không diễn giải p như bằng chứng nhân quả; không chạy so sánh cặp khi điều kiện chưa được xác nhận.

**[MỞ RỘNG NGOÀI BÀI HỌC]** Levene center=median: W={lev["statistic"]:.4f}, p={lev["p_value"]:.6g}; chỉ chẩn đoán thăm dò phương sai với giới hạn độc lập, không tự chứng minh đủ giả định. Nguồn/tham số tại EDA_METHODS. Boxplot tính phân vị trên toàn mẫu nhóm rồi mới giới hạn trục; bar kèm Q1–Q3, không phải khoảng tin cậy.

Nguồn: `rq2_room_type_stats.json`, `rq2_anova_condition_checks.json`, `fig2_price_by_room_type.png`.

## 3. RQ3 — Liên hệ tuyến tính quy mô–giá có độ lớn nhỏ

| Biến | n cặp hợp lệ | Pearson r | p thăm dò |
|---|---|---|---|
{corr_rows}

Các r dương nhưng độ lớn nhỏ; p nhỏ không đồng nghĩa tương quan mạnh. Chưa đánh giá độ nhạy để quy kết nguyên nhân r thấp cho ngoại lệ. Thiếu dữ liệu theo cặp và host clustering giới hạn việc suy rộng. Các số này chỉ trả lời EDA, **không phải danh sách feature được chọn cho mô hình**.

Scatter và OLS dùng đúng cùng tập cặp hợp lệ như Pearson. Lấy mẫu seed42 chỉ để vẽ điểm; catalog ghi n chọn/n thực vẽ và số ngoài trục 20.000 THB. Nguồn: `rq3_size_correlation.json`, `fig3_price_vs_size_scatter.png`.

## 4. RQ4 — So sánh khu vực trong cùng loại phòng

Pivot có {district["districts_count"]} quận × {district["room_types_count"]} loại phòng, {district["empty_cells_count"]} ô n=0 và {district["low_n_cells_count"]} ô 0<n<5. Heatmap hiển thị {catalog[3]["sample_size_n"]:,} listing thuộc các quận được chọn, ghi rõ n từng ô và dấu * ở ô ít mẫu.

Một số trung vị thấp/cao **trong cùng Entire home/apt**, chỉ hiển thị nhóm n≥20:

| Quận theo dữ liệu nguồn | n Entire home/apt | Trung vị THB/đêm |
|---|---|---|
{district_rows}

Ngưỡng n≥20 là quy tắc hiển thị, không bảo đảm tính đại diện. Không suy ra ảnh hưởng vị trí từ thứ hạng gộp mọi loại phòng; không gán quận thành trung tâm/ngoại ô hay khu du lịch nếu chưa có nguồn xác minh. Nguồn: pivot median/count/IQR và hai hình RQ4.

## Minh họa Bài 02 và bàn giao

Scaling, pd.cut khoảng đều và dummy nằm trên bản EDA riêng. **[MỞ RỘNG NGOÀI BÀI HỌC]** qcut minh họa phân vị, không khẳng định ưu thế chung; số đếm/ranh giới thực tế ở `lesson02_wrangling_demo.json`. Không dùng biến tạo từ price hoặc phép fit toàn bộ dữ liệu làm predictor.

| Hình 300 DPI | RQ | Nội dung |
|---|---|---|
{catalog_rows}

Catalog JSON/CSV tính trực tiếp từ DataFrame dùng vẽ, gồm checksum nguồn, fingerprint, phạm vi trục và số quan sát. Bước tiếp theo: đánh giá khả thi mô hình trên train/CV theo đặc tả; không hạ ngưỡng chọn biến hoặc cắt giá chỉ để đạt R² tốt hơn.
"""
    (root / "reports/eda_findings.md").write_text(text, encoding="utf-8")
    return text


if __name__ == "__main__":
    generate_findings()
