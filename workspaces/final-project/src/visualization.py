"""Biểu đồ EDA theo mẫu tính toán thật; phóng trục không thay đổi mẫu thống kê."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.cbook import boxplot_stats

from src.data_loader import compute_sha256
from src.eda_stats import (
    EXPECTED_BASELINE_SHA256,
    SIZE_FEATURES,
    compute_neighbourhood_pivot,
    compute_pairwise_correlations,
    compute_price_distribution_stats,
    finite_frame,
)

PRICE_ZOOM = 10000.0
ROOM_ZOOM = 8000.0
SCATTER_ZOOM = 20000.0
ROOM_ORDER = ["Entire home/apt", "Hotel room", "Private room", "Shared room"]
SIZE_LABELS = {
    "accommodates": "Sức chứa (người)",
    "bedrooms": "Phòng ngủ (phòng)",
    "bathrooms": "Phòng tắm (phòng)",
    "beds": "Giường (chiếc)",
}


def setup_plot_style() -> None:
    """Cấu hình font tiếng Việt, màu và cỡ chữ chung."""
    sns.set_theme(style="whitegrid", font="DejaVu Sans")
    plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Liberation Sans", "Arial"]
    plt.rcParams["axes.unicode_minus"] = False


def finish(fig: plt.Figure, output_path: str | Path | None) -> None:
    """Xuất ảnh 300 DPI bằng Figure OO API."""
    if output_path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, dpi=300)


def plot_price_distribution(price_series, output_path=None):
    """Toàn miền thang trục log và vùng trung tâm; thống kê luôn trên toàn bộ giá."""
    setup_plot_style()
    p = pd.to_numeric(price_series, errors="coerce")
    p = p[np.isfinite(p) & (p > 0)]
    if p.empty:
        raise ValueError("Không có giá hữu hạn dương để vẽ.")
    st = compute_price_distribution_stats(p)
    fig, axes = plt.subplots(1, 2, figsize=(16, 6), layout="constrained")
    low, high = p.min(), p.max()
    bins = np.geomspace(low, high, 50) if high > low else np.array([low * 0.9, high * 1.1])
    bins[0], bins[-1] = min(bins[0], low), max(bins[-1], high)
    axes[0].hist(p, bins=bins, color="#35658c", edgecolor="white")
    axes[0].set_xscale("log")
    axes[0].set_title(
        f"Toàn miền • n = {len(p):,}\nThang trục log10; giá và thống kê giữ đơn vị gốc"
    )
    zoom = p[p <= PRICE_ZOOM]
    axes[1].hist(zoom, bins=40, color="#399878", edgecolor="white")
    axes[1].set_xlim(0, PRICE_ZOOM)
    axes[1].set_title(f"Vùng ≤ {PRICE_ZOOM:,.0f} THB • n hiển thị = {len(zoom):,}")
    outside = len(p) - len(zoom)
    axes[1].text(
        0.98,
        0.56,
        f"{outside:,}/{len(p):,} ({outside / len(p):.2%}) ngoài khung\nToàn miền ở panel trái\nNgoại lệ IQR: {st['outliers_count']:,} (tiêu chí khác)",
        transform=axes[1].transAxes,
        ha="right",
        fontsize=10,
        bbox={"facecolor": "white", "alpha": 0.9},
    )
    for ax in axes:
        ax.axvline(st["median"], color="#b75921", ls="--", label=f"Trung vị {st['median']:,.0f}")
        ax.axvline(st["mean"], color="#7351a2", ls=":", label=f"Trung bình {st['mean']:,.0f}")
        ax.set_xlabel("Giá thuê (THB/đêm)")
        ax.set_ylabel("Số listing (tần số mỗi khoảng)")
        ax.legend(fontsize=9)
    fig.suptitle("RQ1 • Phân bố giá thuê Airbnb Bangkok", fontsize=16)
    finish(fig, output_path)
    return fig, tuple(axes)


def room_box_statistics(df):
    """Tính hộp trên mẫu đầy đủ, không lọc theo giới hạn hiển thị."""
    valid = finite_frame(df, ["price"]).dropna(subset=["room_type", "price"])
    observed = valid.room_type.unique().tolist()
    order = [name for name in ROOM_ORDER if name in observed] + sorted(
        set(observed) - set(ROOM_ORDER)
    )
    boxes = [
        boxplot_stats(valid.loc[valid.room_type == name, "price"].to_numpy(), labels=[name])[0]
        for name in order
    ]
    return valid, boxes


def plot_room_type_comparison(df, output_path=None):
    """Boxplot tính trên toàn mẫu và bar trung vị với đoạn Q1–Q3; chỉ giới hạn trục."""
    setup_plot_style()
    valid, boxes = room_box_statistics(df)
    if not boxes:
        raise ValueError("Không có nhóm phòng hợp lệ.")
    fig, axes = plt.subplots(1, 2, figsize=(16, 6), layout="constrained")
    colors = sns.color_palette("colorblind", len(boxes))
    artists = axes[0].bxp(boxes, patch_artist=True, flierprops={"markersize": 2, "alpha": 0.3})
    for patch, color in zip(artists["boxes"], colors, strict=True):
        patch.set_facecolor(color)
    axes[0].set_ylim(0, ROOM_ZOOM)
    outside = int((valid.price > ROOM_ZOOM).sum())
    axes[0].set_title(
        f"Hộp tính trên toàn bộ {len(valid):,} listing\n{outside:,} giá > {ROOM_ZOOM:,.0f} THB ngoài khung"
    )
    med = np.array([box["med"] for box in boxes])
    q1 = np.array([box["q1"] for box in boxes])
    q3 = np.array([box["q3"] for box in boxes])
    positions = np.arange(len(boxes))
    axes[1].bar(
        positions,
        med,
        yerr=[med - q1, q3 - med],
        color=colors,
        capsize=5,
        label="Đoạn Q1–Q3; không phải khoảng tin cậy",
    )
    axes[1].set_xticks(positions, [box["label"] for box in boxes])
    for i, box in enumerate(boxes):
        n = int((valid.room_type == box["label"]).sum())
        axes[1].text(
            i,
            med[i] / 2,
            f"{med[i]:,.0f}\nn={n:,}",
            ha="center",
            va="center",
            color="white",
            fontweight="bold",
        )
    axes[1].set_title("Trung vị và khoảng tứ phân vị (toàn mẫu)")
    axes[1].legend(fontsize=8)
    for ax in axes:
        ax.set_xlabel("Loại phòng")
        ax.set_ylabel("Giá thuê (THB/đêm)")
        ax.tick_params(axis="x", labelsize=9)
    fig.suptitle("RQ2 • Giá theo loại phòng — xem toàn miền giá ở hình RQ1", fontsize=15)
    finish(fig, output_path)
    return fig, tuple(axes)


def scatter_data(df, feature, sample_display_n=3000, seed=42):
    """Mẫu tính hồi quy đầy đủ và mẫu điểm hiển thị kèm kế toán giới hạn trục."""
    pair = finite_frame(df[[feature, "price"]], [feature, "price"]).dropna()
    selected = (
        pair.sample(n=min(sample_display_n, len(pair)), random_state=seed) if len(pair) else pair
    )
    shown = selected[selected.price.between(0, SCATTER_ZOOM)]
    line = None
    if len(pair) >= 3 and pair[feature].nunique() > 1:
        slope, intercept = np.polyfit(pair[feature], pair.price, 1)
        line = {"slope": float(slope), "intercept": float(intercept), "fit_n": len(pair)}
    meta = {
        "n_valid": len(pair),
        "sample_selected": len(selected),
        "n_displayed": len(shown),
        "selected_outside_axis": len(selected) - len(shown),
        "full_outside_axis": int((~pair.price.between(0, SCATTER_ZOOM)).sum()),
        "not_sampled": len(pair) - len(selected),
        "seed": seed,
        "trend": line,
    }
    return pair, shown, meta


def plot_size_correlation(df, size_cols=None, output_path=None, seed=42, sample_display_n=3000):
    """Đường xu hướng và Pearson cùng tính trên toàn bộ cặp hữu hạn."""
    setup_plot_style()
    columns = SIZE_FEATURES if size_cols is None else size_cols
    if not 1 <= len(columns) <= 4:
        raise ValueError("Cần 1–4 biến cho lưới biểu đồ.")
    correlations = compute_pairwise_correlations(df, columns).set_index("feature")
    fig, axes = plt.subplots(2, 2, figsize=(15, 11), layout="constrained")
    flat = axes.ravel()
    for ax, col in zip(flat, columns, strict=False):
        pair, shown, meta = scatter_data(df, col, sample_display_n, seed)
        ax.scatter(
            shown[col],
            shown.price,
            s=14,
            alpha=0.25,
            color="#35658c",
            label="Điểm trong khung từ mẫu hiển thị",
        )
        trend = meta["trend"]
        if trend:
            x = np.linspace(pair[col].min(), pair[col].max(), 100)
            ax.plot(
                x,
                trend["slope"] * x + trend["intercept"],
                color="#b75921",
                label=f"OLS toàn mẫu: độ dốc {trend['slope']:.1f}",
            )
        row = correlations.loc[col]
        note = (
            f"r={row.pearson_r:+.4f}, p={row.p_value:.2e}"
            if row.status == "COMPUTED"
            else row.status
        )
        ax.set_title(f"{SIZE_LABELS.get(col, col)}\n{note}; n hợp lệ={len(pair):,}", fontsize=11)
        ax.set_xlabel(SIZE_LABELS.get(col, col))
        ax.set_ylabel("Giá thuê (THB/đêm)")
        ax.set_ylim(0, SCATTER_ZOOM)
        ax.legend(fontsize=8, loc="upper left")
        ax.text(
            0.98,
            0.03,
            f"Chọn {meta['sample_selected']:,} (seed={seed}); vẽ {meta['n_displayed']:,}\n{meta['selected_outside_axis']:,} điểm đã chọn ngoài trục\nToàn mẫu có {meta['full_outside_axis']:,} giá ngoài trục",
            ha="right",
            transform=ax.transAxes,
            fontsize=8,
            bbox={"facecolor": "white", "alpha": 0.9},
        )
    for ax in flat[len(columns) :]:
        ax.set_visible(False)
    fig.suptitle(
        "RQ3 • Pearson và OLS toàn mẫu; điểm hiển thị lấy mẫu, trục Y phóng to\nPhạm vi giá đầy đủ ở hình RQ1; p-value chỉ diễn giải thăm dò",
        fontsize=14,
    )
    finish(fig, output_path)
    return fig, flat


def neighbourhood_views(df, top_n_districts=15):
    """Chọn quận theo số mẫu; bar so sánh trong cùng loại Entire home/apt."""
    valid = finite_frame(df, ["price"]).dropna(
        subset=["price", "room_type", "neighbourhood_cleansed"]
    )
    med, count, _, summary = compute_neighbourhood_pivot(valid)
    districts = valid.neighbourhood_cleansed.value_counts().head(top_n_districts).index
    room = "Entire home/apt"
    if room in med.columns:
        eligible = pd.DataFrame({"median": med[room], "n": count[room]})
        eligible = eligible[eligible.n >= 20].sort_values("median")
        selected = pd.concat([eligible.head(10), eligible.tail(10)]).loc[
            lambda frame: ~frame.index.duplicated()
        ]
    else:
        selected = pd.DataFrame(columns=["median", "n"])
    return med.loc[districts], count.loc[districts], selected, summary


def plot_neighbourhood_analysis(
    df, output_path_heatmap=None, output_path_bars=None, top_n_districts=15
):
    """Heatmap theo loại phòng; bar cùng Entire home/apt, n>=20 chỉ là quy tắc hiển thị."""
    setup_plot_style()
    med, count, selected, _ = neighbourhood_views(df, top_n_districts)
    fig_heat, ax = plt.subplots(figsize=(12, 10), layout="constrained")
    if not med.empty:
        labels = med.astype(object)
        for district in med.index:
            for room in med.columns:
                n = int(count.loc[district, room])
                labels.loc[district, room] = f"{med.loc[district, room]:,.0f}\n(n={n})" + (
                    " *" if 0 < n < 5 else ""
                )
        sns.heatmap(
            med,
            annot=labels,
            fmt="",
            cmap="YlOrRd",
            linewidths=0.5,
            cbar_kws={"label": "Giá trung vị (THB/đêm)"},
            ax=ax,
        )
        for y, district in enumerate(med.index):
            for x, room in enumerate(med.columns):
                if count.loc[district, room] == 0:
                    ax.text(x + 0.5, y + 0.5, "n=0", ha="center", va="center", fontsize=9)
    ax.set_title(
        f"RQ4 • {len(med)} quận nhiều listing nhất × loại phòng\n* n<5: mô tả rất ít mẫu; ô trống n=0",
        fontsize=13,
    )
    ax.set_xlabel("Loại phòng")
    ax.set_ylabel("Quận theo dữ liệu nguồn")
    finish(fig_heat, output_path_heatmap)
    fig_bar, ax_bar = plt.subplots(figsize=(13, 9), layout="constrained")
    bars = ax_bar.barh(selected.index, selected["median"], color="#35658c")
    for bar, (_, row) in zip(bars, selected.iterrows(), strict=True):
        ax_bar.text(
            bar.get_width() + 20,
            bar.get_y() + bar.get_height() / 2,
            f"{row['median']:,.0f} (n={int(row['n']):,})",
            va="center",
            fontsize=9,
        )
    if len(selected):
        ax_bar.set_xlim(0, float(selected["median"].max()) * 1.35)
    ax_bar.set_title(
        "RQ4 • Giá trung vị theo quận trong cùng Entire home/apt\nTối đa 10 mức thấp và 10 mức cao; n≥20 là quy tắc hiển thị, không bảo đảm đại diện",
        fontsize=12,
    )
    ax_bar.set_xlabel("Giá trung vị (THB/đêm)")
    ax_bar.set_ylabel("Quận theo dữ liệu nguồn")
    finish(fig_bar, output_path_bars)
    return fig_heat, fig_bar


def generate_figures_catalog(figures_dir, output_catalog_path=None, df=None):
    """Tính metadata từ chính DataFrame dùng vẽ; không sử dụng số liệu ghi sẵn."""
    if df is None:
        raise ValueError("Cần DataFrame đã dùng để sinh hình cho catalog.")
    valid = finite_frame(df, ["price"]).dropna(subset=["price"])
    med, count, selected, _ = neighbourhood_views(valid)
    n = len(valid)
    entries = [
        {
            "figure_filename": "fig1_price_distribution.png",
            "rq": "RQ1",
            "title_vi": "Phân bố giá",
            "chart_type": "Histogram toàn miền + vùng trung tâm",
            "source_data_table": "reports/stats/rq1_price_distribution.json",
            "sample_size_n": n,
            "axis_ranges": {
                "full": [float(valid.price.min()), float(valid.price.max())],
                "zoom": [0, PRICE_ZOOM],
            },
            "out_of_frame_notes": {
                "zoom_displayed": int((valid.price <= PRICE_ZOOM).sum()),
                "zoom_excluded": int((valid.price > PRICE_ZOOM).sum()),
            },
        },
        {
            "figure_filename": "fig2_price_by_room_type.png",
            "rq": "RQ2",
            "title_vi": "Giá theo loại phòng",
            "chart_type": "Boxplot + trung vị/Q1–Q3 toàn mẫu",
            "source_data_table": "reports/stats/rq2_room_type_stats.json",
            "sample_size_n": int(valid.room_type.notna().sum()),
            "axis_ranges": {"box": [0, ROOM_ZOOM]},
            "out_of_frame_notes": {
                "box_above_limit": int((valid.price > ROOM_ZOOM).sum()),
                "box_statistics_fit": "ALL_VALID_ROWS",
            },
        },
        {
            "figure_filename": "fig3_price_vs_size_scatter.png",
            "rq": "RQ3",
            "title_vi": "Quy mô và giá",
            "chart_type": "Scatter; OLS toàn bộ cặp hợp lệ",
            "source_data_table": "reports/stats/rq3_size_correlation.json",
            "sample_size_n": {col: scatter_data(valid, col)[2]["n_valid"] for col in SIZE_FEATURES},
            "axis_ranges": {"y": [0, SCATTER_ZOOM]},
            "out_of_frame_notes": {col: scatter_data(valid, col)[2] for col in SIZE_FEATURES},
        },
        {
            "figure_filename": "fig4_price_by_neighbourhood_heatmap.png",
            "rq": "RQ4",
            "title_vi": "Quận × loại phòng",
            "chart_type": "Heatmap trung vị, n và cảnh báo n<5",
            "source_data_table": "reports/stats/rq4_neighbourhood_pivot_median.csv",
            "sample_size_n": int(count.sum().sum()),
            "axis_ranges": {"districts": med.index.tolist(), "room_types": med.columns.tolist()},
            "out_of_frame_notes": {
                "listings_not_in_displayed_districts": n - int(count.sum().sum())
            },
        },
        {
            "figure_filename": "fig4_price_top_neighbourhoods_bar.png",
            "rq": "RQ4",
            "title_vi": "Giá theo quận trong Entire home/apt",
            "chart_type": "Bar trung vị cùng loại phòng",
            "source_data_table": "reports/stats/rq4_neighbourhood_pivot_median.csv",
            "sample_size_n": int(selected.n.sum()),
            "axis_ranges": {"room_type": "Entire home/apt", "districts": selected.index.tolist()},
            "out_of_frame_notes": {
                "minimum_n": 20,
                "note": "Tối đa 10 thấp và 10 cao; ngưỡng chỉ để hiển thị",
            },
        },
    ]
    fingerprint = hashlib.sha256(
        pd.util.hash_pandas_object(df, index=True).values.tobytes()
    ).hexdigest()
    for entry in entries:
        entry.update(
            units="THB/đêm",
            dataframe_sha256=fingerprint,
            source_baseline_sha256=df.attrs.get("source_sha256"),
            dpi=300,
            design_steps_summary="Câu hỏi → kiểm tra biến/n → thông điệp theo kết quả → chọn hình → nhãn/giới hạn; chi tiết notebook 03",
        )
    if output_catalog_path:
        path = Path(output_catalog_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.suffix == ".json":
            path.write_text(
                json.dumps(entries, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
                encoding="utf-8",
            )
        else:
            pd.DataFrame(entries).to_csv(path, index=False)
    return pd.DataFrame(entries)


def run_all_visualizations(df, figures_dir):
    """Xuất năm hình và catalog từ cùng DataFrame."""
    folder = Path(figures_dir)
    folder.mkdir(parents=True, exist_ok=True)
    paths = {
        key: folder / name
        for key, name in {
            "fig1": "fig1_price_distribution.png",
            "fig2": "fig2_price_by_room_type.png",
            "fig3": "fig3_price_vs_size_scatter.png",
            "fig4_heat": "fig4_price_by_neighbourhood_heatmap.png",
            "fig4_bar": "fig4_price_top_neighbourhoods_bar.png",
        }.items()
    }
    for routine, key, arg in [
        (plot_price_distribution, "fig1", df.price),
        (plot_room_type_comparison, "fig2", df),
        (plot_size_correlation, "fig3", df),
    ]:
        fig, _ = routine(arg, output_path=paths[key])
        plt.close(fig)
    heat, bars = plot_neighbourhood_analysis(df, paths["fig4_heat"], paths["fig4_bar"])
    plt.close(heat)
    plt.close(bars)
    for ext in ["json", "csv"]:
        path = folder / f"figures_catalog.{ext}"
        generate_figures_catalog(folder, path, df=df)
        paths[f"catalog_{ext}"] = path
    return {key: str(value) for key, value in paths.items()}


def main():
    """CLI có kiểm hash baseline trước khi xuất hình."""
    parser = argparse.ArgumentParser(description="Biểu đồ EDA Airbnb Bangkok")
    parser.add_argument("--input", default="data/processed/bangkok_cleaned.csv")
    parser.add_argument("--output-dir", default="reports/figures")
    args = parser.parse_args()
    actual = compute_sha256(args.input)
    if actual != EXPECTED_BASELINE_SHA256:
        raise ValueError("Checksum baseline không khớp.")
    df = pd.read_csv(args.input)
    df.attrs["source_sha256"] = actual
    run_all_visualizations(df, args.output_dir)


if __name__ == "__main__":
    main()
