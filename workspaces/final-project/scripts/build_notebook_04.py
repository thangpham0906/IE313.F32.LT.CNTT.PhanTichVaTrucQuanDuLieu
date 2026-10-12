"""Khôi phục notebook 04 từ bản mẫu đã review; mặc định giữ tệp hiện có."""

import argparse
from pathlib import Path

import nbformat


def build_notebook_04(overwrite=False):
    """Không ghi đè notebook đã làm nếu chưa có --overwrite."""
    root = Path(__file__).resolve().parent.parent
    target = root / "notebooks/04_regression_modeling.ipynb"
    if target.exists() and not overwrite:
        print(f"Giữ notebook hiện có: {target}")
        return
    nbformat.write(
        nbformat.read(root / "scripts/notebook_templates" / target.name, as_version=4), target
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--overwrite", action="store_true")
    build_notebook_04(parser.parse_args().overwrite)
