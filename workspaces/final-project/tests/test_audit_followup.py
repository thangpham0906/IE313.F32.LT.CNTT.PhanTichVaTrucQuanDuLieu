"""Hồi quy các lỗ hổng còn sót trong lần review Bước 1 thứ hai."""

import io
import json
import subprocess
import sys
from unittest.mock import patch

import pandas as pd
import pytest

from src.data_audit import run_full_audit
from src.data_loader import compute_sha256, safe_acquire_raw_data


@pytest.mark.parametrize("content", [None, "{bad json", "{}", '{"sha256": ""}'])
def test_explicit_bad_manifest_fails_without_outputs(tmp_path, content):
    """Không hạ kiểm tra toàn vẹn về NOT_CHECKED nếu đã yêu cầu manifest."""
    raw = tmp_path / "raw.csv"
    raw.write_text("id,price\n1,$100\n")
    manifest = tmp_path / "manifest.json"
    if content is not None:
        manifest.write_text(content)
    out = tmp_path / "output"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "src.data_audit",
            "--input",
            str(raw),
            "--manifest",
            str(manifest),
            "--output-dir",
            str(out),
        ],
        capture_output=True,
    )
    assert result.returncode != 0
    assert not out.exists()


@pytest.mark.parametrize("prices", [["$100"], [None, None], ["$100", "$100"]])
def test_sparse_audit_json_and_markdown_have_no_invented_results(tmp_path, prices):
    """Mẫu thiếu bằng chứng không được kết luận khớp quote 100% hay bịa thống kê."""
    raw = tmp_path / "raw.csv"
    pd.DataFrame({"id": range(len(prices)), "price": prices}).to_csv(raw, index=False)
    output = tmp_path / "out"
    md = tmp_path / "audit.md"
    run_full_audit(raw, output, markdown_output_path=md)
    json.loads(
        (output / "bangkok_audit_summary.json").read_text(),
        parse_constant=lambda value: pytest.fail(value),
    )
    text = md.read_text()
    assert "Chưa đủ bằng chứng quote" in text
    assert "Toàn bộ cặp giá hữu hạn" not in text
    assert "90 cột" not in text
    if prices == [None, None]:
        assert "| Min | N/A |" in text


def test_download_race_preserves_competing_file(tmp_path):
    """Tệp xuất hiện trong khi tải không được thay thế bởi rename/replace."""
    source = tmp_path / "source"
    source.write_bytes(b"expected download")
    target = tmp_path / "raw" / "listings.csv"

    def open_response(*args, **kwargs):
        target.write_bytes(b"other process wrote this")
        return io.BytesIO(source.read_bytes())

    with patch("urllib.request.urlopen", side_effect=open_response):
        with pytest.raises(FileExistsError):
            safe_acquire_raw_data("http://example.invalid/data", target, compute_sha256(source))
    assert target.read_bytes() == b"other process wrote this"
    assert list(target.parent.iterdir()) == [target]


def test_download_success_is_verified(tmp_path):
    """Chỉ công bố file đã kiểm checksum, thư mục raw không chứa file tạm."""
    source = tmp_path / "source"
    source.write_bytes(b"expected download")
    target = tmp_path / "raw" / "listings.csv"
    with patch("urllib.request.urlopen", return_value=io.BytesIO(source.read_bytes())):
        result = safe_acquire_raw_data(
            "http://example.invalid/data", target, compute_sha256(source)
        )
    assert result["status"] == "DOWNLOADED_AND_VERIFIED"
    assert compute_sha256(target) == compute_sha256(source)
    assert list(target.parent.iterdir()) == [target]
