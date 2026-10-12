"""Bộ kiểm thử đơn vị (Unit Tests) cho module visualization.

Kiểm tra tính đúng đắn của các hàm trực quan hóa Matplotlib OO API,
đảm bảo sinh đúng Figure/Axes, xuất ảnh PNG 300 DPI và danh mục catalog.
Đồ án môn học IE313 (UIT - VNU-HCM) - Nhóm 10.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest

from src.visualization import (
    generate_figures_catalog,
    plot_neighbourhood_analysis,
    plot_price_distribution,
    plot_room_type_comparison,
    plot_size_correlation,
    run_all_visualizations,
)


@pytest.fixture
def sample_viz_df() -> pd.DataFrame:
    """Fixture DataFrame nhỏ để kiểm thử đồ họa."""
    rng = np.random.default_rng(42)
    return pd.DataFrame(
        {
            "id": range(1, 101),
            "price": rng.uniform(500, 15000, 100),
            "room_type": rng.choice(
                ["Entire home/apt", "Hotel room", "Private room", "Shared room"], 100
            ),
            "neighbourhood_cleansed": rng.choice(
                ["Watthana", "Khlong Toei", "Huai Khwang", "Sathon"], 100
            ),
            "accommodates": rng.integers(1, 8, 100),
            "bedrooms": rng.integers(1, 4, 100),
            "bathrooms": rng.uniform(1, 3, 100),
            "beds": rng.integers(1, 6, 100),
        }
    )


class TestVisualizationRoutines:
    """Kiểm thử từng hàm tạo biểu đồ và xuất tệp ảnh."""

    def test_plot_price_distribution(self, sample_viz_df: pd.DataFrame, tmp_path: Path) -> None:
        """Kiểm tra vẽ phân phối giá xuất ảnh PNG hợp lệ."""
        out_png = tmp_path / "fig1_test.png"
        fig, axes = plot_price_distribution(sample_viz_df["price"], output_path=out_png)

        assert len(axes) == 2
        assert out_png.is_file()
        assert out_png.stat().st_size > 1000
        plt.close(fig)

    def test_plot_room_type_comparison(self, sample_viz_df: pd.DataFrame, tmp_path: Path) -> None:
        """Kiểm tra vẽ so sánh loại phòng xuất ảnh PNG hợp lệ."""
        out_png = tmp_path / "fig2_test.png"
        fig, axes = plot_room_type_comparison(sample_viz_df, output_path=out_png)

        assert len(axes) == 2
        assert out_png.is_file()
        assert out_png.stat().st_size > 1000
        plt.close(fig)

    def test_plot_size_correlation(self, sample_viz_df: pd.DataFrame, tmp_path: Path) -> None:
        """Kiểm tra vẽ ma trận scatter 2x2 quy mô chỗ ở."""
        out_png = tmp_path / "fig3_test.png"
        fig, axes = plot_size_correlation(sample_viz_df, output_path=out_png, sample_display_n=50)

        assert len(axes) == 4
        assert out_png.is_file()
        assert out_png.stat().st_size > 1000
        plt.close(fig)

    def test_plot_neighbourhood_analysis(self, sample_viz_df: pd.DataFrame, tmp_path: Path) -> None:
        """Kiểm tra vẽ heatmap và bar chart quận huyện."""
        out_heat = tmp_path / "fig4_heat.png"
        out_bar = tmp_path / "fig4_bar.png"
        fig_heat, fig_bar = plot_neighbourhood_analysis(
            sample_viz_df, output_path_heatmap=out_heat, output_path_bars=out_bar, top_n_districts=4
        )

        assert out_heat.is_file()
        assert out_bar.is_file()
        plt.close(fig_heat)
        plt.close(fig_bar)

    def test_generate_figures_catalog(self, tmp_path: Path, sample_viz_df: pd.DataFrame) -> None:
        """Kiểm tra tạo danh mục catalog đầy đủ cấu trúc."""
        cat_json = tmp_path / "catalog.json"
        cat_csv = tmp_path / "catalog.csv"

        df_cat = generate_figures_catalog(tmp_path, output_catalog_path=cat_json, df=sample_viz_df)
        generate_figures_catalog(tmp_path, output_catalog_path=cat_csv, df=sample_viz_df)

        assert cat_json.is_file()
        assert cat_csv.is_file()
        assert len(df_cat) == 5
        assert "figure_filename" in df_cat.columns
        assert "rq" in df_cat.columns
        assert "design_steps_summary" in df_cat.columns

    def test_run_all_visualizations_workflow(
        self, sample_viz_df: pd.DataFrame, tmp_path: Path
    ) -> None:
        """Kiểm tra toàn bộ quy trình xuất bản biểu đồ và catalog."""
        out_dir = tmp_path / "figures_all"
        res = run_all_visualizations(sample_viz_df, figures_dir=out_dir)

        assert len(res) == 7
        assert (out_dir / "fig1_price_distribution.png").is_file()
        assert (out_dir / "fig2_price_by_room_type.png").is_file()
        assert (out_dir / "fig3_price_vs_size_scatter.png").is_file()
        assert (out_dir / "fig4_price_by_neighbourhood_heatmap.png").is_file()
        assert (out_dir / "fig4_price_top_neighbourhoods_bar.png").is_file()
        assert (out_dir / "figures_catalog.json").is_file()
        assert (out_dir / "figures_catalog.csv").is_file()
        plt.close("all")
