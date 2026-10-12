"""Khởi tạo notebook 02–03 từ mẫu đã review; giữ notebook hiện có nếu chưa yêu cầu ghi đè."""

import argparse
from pathlib import Path

import nbformat


def main():
    """Chỉ ghi đè notebook hiện có khi truyền --overwrite rõ ràng."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    for template in (root / "scripts/notebook_templates").glob("*.ipynb"):
        target = root / "notebooks" / template.name
        if target.exists() and not args.overwrite:
            print(f"Giữ notebook hiện có: {target.name}")
            continue
        nbformat.write(nbformat.read(template, as_version=4), target)


if __name__ == "__main__":
    main()
