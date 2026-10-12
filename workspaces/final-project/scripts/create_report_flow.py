"""Vẽ quy trình thực tế của đồ án cho báo cáo, không dùng hình mẫu của GV."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


def main():
    """Xuất sơ đồ vector dựng bằng Matplotlib OO API ở 300 DPI."""
    output = Path(__file__).resolve().parent.parent / "reports/figures/report_analysis_flow.png"
    with plt.rc_context({"font.sans-serif": ["DejaVu Sans"]}):
        fig, ax = plt.subplots(figsize=(9, 2.1), layout="constrained")
        ax.set(xlim=(0, 9), ylim=(0, 2))
        ax.axis("off")
        labels = [
            "Nguồn và\nkiểm toán",
            "Làm sạch\n28.987 dòng",
            "EDA\n4 câu hỏi",
            "Trực quan\n5 biểu đồ",
            "Train/CV\nchọn biến",
            "Tổng hợp\nvà giới hạn",
        ]
        for i, label in enumerate(labels):
            x = i * 1.5 + 0.03
            ax.add_patch(
                FancyBboxPatch(
                    (x, 0.55),
                    1.3,
                    1.0,
                    boxstyle="round,pad=0.025",
                    facecolor="#EDF4F8",
                    edgecolor="#164760",
                )
            )
            ax.text(x + 0.65, 1.05, label, ha="center", va="center", fontsize=12, color="#123449")
            if i < 5:
                ax.annotate(
                    "",
                    xy=(x + 1.48, 1.05),
                    xytext=(x + 1.31, 1.05),
                    arrowprops={"arrowstyle": "->", "color": "#164760"},
                )
        ax.text(
            4.5,
            0.18,
            "Raw bất biến • Giá gốc THB/đêm • Seed 42 • Kết quả truy về notebook",
            ha="center",
            fontsize=11,
        )
        fig.savefig(output, dpi=300)
        plt.close(fig)


if __name__ == "__main__":
    main()
