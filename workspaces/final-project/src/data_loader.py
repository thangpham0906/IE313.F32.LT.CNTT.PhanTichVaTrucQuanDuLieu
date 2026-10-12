"""Module nạp và xác thực tính toàn vẹn dữ liệu Inside Airbnb Bangkok.

Cung cấp các hàm kiểm tra mã băm SHA-256, chuyển đổi định dạng giá nghiêm ngặt và
nạp dữ liệu an toàn phục vụ đồ án môn học IE313 (UIT - VNU-HCM).
"""

from __future__ import annotations

import hashlib
import os
import re
import shutil
import tempfile
import urllib.request
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


def compute_sha256(filepath: str | Path, chunk_size: int = 65536) -> str:
    """Tính toán mã băm SHA-256 của tệp tin theo từng khối nhị phân.

    Parameters
    ----------
    filepath : str | Path
        Đường dẫn đến tệp tin cần tính mã băm.
    chunk_size : int, default=65536
        Kích thước khối đọc nhị phân (bytes).

    Returns
    -------
    str
        Chuỗi mã băm SHA-256 dạng thập lục phân (hexadecimal).
    """
    path = Path(filepath)
    if not path.is_file():
        raise FileNotFoundError(f"Không tìm thấy tệp tin: {filepath}")

    hasher = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(chunk_size):
            hasher.update(chunk)
    return hasher.hexdigest()


def verify_file_checksum(filepath: str | Path, expected_sha256: str) -> bool:
    """Xác thực tính toàn vẹn của tệp tin so với mã băm SHA-256 kỳ vọng.

    Parameters
    ----------
    filepath : str | Path
        Đường dẫn đến tệp tin cần kiểm tra.
    expected_sha256 : str
        Mã băm SHA-256 kỳ vọng (không phân biệt hoa/thường).

    Returns
    -------
    bool
        True nếu mã băm trùng khớp, False nếu có sự sai lệch.
    """
    actual_hash = compute_sha256(filepath)
    return actual_hash.lower() == expected_sha256.strip().lower()


def parse_price_value(value: Any) -> float:
    """Chuyển đổi chuỗi giá tiền tệ sang số thực (float) với kiểm tra định dạng nghiêm ngặt.

    Xử lý an toàn các ký tự '$', '฿', dấu phân cách hàng nghìn chuẩn và giá trị khuyết.
    Từ chối các kiểu boolean, vô cực (inf/-inf), chuỗi phân cách sai quy chuẩn (ví dụ '1,2,3', '1,50').

    Parameters
    ----------
    value : Any
        Giá trị thô đầu vào (chuỗi ký tự, số, hoặc NaN).

    Returns
    -------
    float
        Giá trị số thực hữu hạn sau khi xử lý, hoặc np.nan nếu không hợp lệ.
    """
    if isinstance(value, bool) or pd.isna(value):
        return np.nan

    if isinstance(value, (int, float)):
        return float(value) if np.isfinite(value) else np.nan

    val_str = str(value).strip()
    if not val_str:
        return np.nan

    # Loại bỏ các giá trị vô cực
    if val_str.lower() in ("inf", "-inf", "+inf", "infinity", "-infinity"):
        return np.nan

    # Xử lý ký hiệu tiền tệ và dấu âm/dương đứng trước hoặc sau ký hiệu
    cleaned = re.sub(r"^([+-]?)\s*[$฿]\s*", r"\1", val_str)
    cleaned = re.sub(r"^[$฿]\s*([+-]?)", r"\1", cleaned).strip()

    # Định dạng 1: Số nguyên hoặc số thập phân chuẩn không có dấu phân cách hàng nghìn (ví dụ: 807, 807.00, -50.5)
    if re.match(r"^[+-]?\d+(\.\d+)?$", cleaned):
        try:
            parsed = float(cleaned)
            return parsed if np.isfinite(parsed) else np.nan
        except (ValueError, TypeError):
            return np.nan

    # Định dạng 2: Số có dấu phẩy phân cách hàng nghìn hợp lệ (ví dụ: 1,148.24, 25,106.00, 1,320,255)
    if re.match(r"^[+-]?\d{1,3}(,\d{3})+(\.\d+)?$", cleaned):
        try:
            parsed = float(cleaned.replace(",", ""))
            return parsed if np.isfinite(parsed) else np.nan
        except (ValueError, TypeError):
            return np.nan

    # Không đúng định dạng tiền tệ hợp lệ (ví dụ '1,2,3', '1,50', 'free')
    return np.nan


def load_listings_data(
    filepath: str | Path,
    parse_prices: bool = True,
    price_col: str = "price",
    parsed_col: str = "price_numeric",
) -> pd.DataFrame:
    """Đọc dữ liệu chi tiết chỗ ở Inside Airbnb từ file nén .csv.gz hoặc .csv.

    Parameters
    ----------
    filepath : str | Path
        Đường dẫn đến tệp dữ liệu thô.
    parse_prices : bool, default=True
        Nếu True, tạo thêm cột số thực parsed_col từ cột price_col.
    price_col : str, default='price'
        Tên cột giá gốc dạng chuỗi.
    parsed_col : str, default='price_numeric'
        Tên cột giá số thực sau khi parse.

    Returns
    -------
    pd.DataFrame
        DataFrame chứa dữ liệu chỗ ở đã nạp.
    """
    path = Path(filepath)
    if not path.is_file():
        raise FileNotFoundError(f"Không tìm thấy tệp dữ liệu: {filepath}")

    # Đọc dữ liệu chỉ đọc, giữ nguyên các cột gốc
    df = pd.read_csv(path, compression="infer", low_memory=False)

    if parse_prices and price_col in df.columns:
        df[parsed_col] = df[price_col].apply(parse_price_value)

    return df


def safe_acquire_raw_data(
    source_url: str,
    target_filepath: str | Path,
    expected_sha256: str,
    temp_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Quy trình thu thập dữ liệu an toàn, tuân thủ nghiêm ngặt tính bất biến của dữ liệu thô.

    - Nếu tệp đích đã tồn tại và mã băm khớp: Sử dụng lại tệp hiện có, không tải đè.
    - Nếu tệp đích đã tồn tại nhưng sai mã băm: Báo lỗi và giữ nguyên tệp hiện có (không xóa/sửa).
    - Nếu tệp chưa tồn tại: Tải về tệp tạm, kiểm tra mã băm trước khi di chuyển vào đích.

    Parameters
    ----------
    source_url : str
        URL tải dữ liệu trực tiếp.
    target_filepath : str | Path
        Đường dẫn tệp đích lưu dữ liệu thô.
    expected_sha256 : str
        Mã băm SHA-256 kỳ vọng để xác thực toàn vẹn.
    temp_dir : str | Path | None, default=None
        Thư mục chứa tệp tạm thời trong quá trình tải.

    Returns
    -------
    dict[str, Any]
        Thông tin trạng thái thu thập và đường dẫn tệp.
    """
    target = Path(target_filepath)
    if target.is_symlink():
        raise ValueError(f"Từ chối ghi vào liên kết tượng trưng: {target}")
    if target.is_file():
        actual_hash = compute_sha256(target)
        if actual_hash.lower() == expected_sha256.strip().lower():
            return {
                "status": "ALREADY_EXISTS_VERIFIED",
                "message": "Tệp dữ liệu đã tồn tại và khớp mã băm SHA-256.",
                "path": str(target),
                "sha256": actual_hash,
            }
        else:
            raise ValueError(
                f"Tệp hiện có tại {target} không khớp mã băm kỳ vọng!\n"
                f"  Kỳ vọng: {expected_sha256}\n"
                f"  Thực tế: {actual_hash}\n"
                f"Tuyệt đối không xóa hoặc ghi đè tệp hiện có theo quy chuẩn bất biến."
            )

    target.parent.mkdir(parents=True, exist_ok=True)
    tmp_dir = Path(temp_dir) if temp_dir else target.parent.parent / ".downloads"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".tmp_download_", dir=tmp_dir) as staging:
        temp_file = Path(staging) / "download"
        # Tải tệp về đường dẫn tạm
        req = urllib.request.Request(
            source_url, headers={"User-Agent": "Mozilla/5.0 (DataAudit/1.0; IE313)"}
        )
        with urllib.request.urlopen(req, timeout=60) as response, temp_file.open("xb") as out_file:
            shutil.copyfileobj(response, out_file)

        # Kiểm tra mã băm tệp tạm trước khi di chuyển vào đích
        downloaded_hash = compute_sha256(temp_file)
        if downloaded_hash.lower() != expected_sha256.strip().lower():
            raise ValueError(
                f"Mã băm của tệp tải về không khớp!\n"
                f"  Kỳ vọng: {expected_sha256}\n"
                f"  Thực tế: {downloaded_hash}\n"
                f"Tệp tạm đã bị hủy, không có tệp nào được ghi vào đích {target}."
            )

        # Tạo đích nguyên tử, không ghi đè kể cả khi tiến trình khác vừa tạo tệp.
        # Thư mục tạm cần ở cùng filesystem; nếu khác, báo lỗi và giữ nguyên đích.
        os.link(temp_file, target)
        return {
            "status": "DOWNLOADED_AND_VERIFIED",
            "message": "Tải dữ liệu và xác thực mã băm thành công.",
            "path": str(target),
            "sha256": downloaded_hash,
        }
