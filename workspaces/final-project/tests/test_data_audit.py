"""Bộ kiểm thử đơn vị (Unit Tests) & Kiểm thử hồi quy (Regression Tests) cho data_loader và data_audit.

Bao gồm kiểm thử nghiêm ngặt các trường hợp biên:
- F1: Tính chính xác của các chỉ số cấu trúc, missing cells, và host clustering.
- F3: Thất bại khi sai checksum, không ghi đè báo cáo cũ, trạng thái NOT_CHECKED.
- F4: Thu thập dữ liệu an toàn, bảo toàn tính bất biến của file thô.
- F5: Parse giá chặt chẽ (loại trừ '1,2,3', '1,50', bool, inf), phân tách exact vs tolerance quote match,
      xử lý dataframe rỗng/all-null host không phát sinh ZeroDivisionError.
- F6: Sinh Markdown kiểm toán tự động đồng bộ số liệu máy đọc.

Đồ án môn học IE313 (UIT - VNU-HCM) - Nhóm 10.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd
import pytest

from src.data_audit import (
    CANDIDATE_FEATURES,
    audit_candidate_variables,
    audit_column_groups,
    audit_currency_and_pricing_granularity,
    audit_dataset_structure,
    audit_host_clustering,
    audit_price_field,
    audit_temporal_coverage,
    generate_columns_catalog,
    generate_data_audit_markdown,
    main,
    run_full_audit,
)
from src.data_loader import (
    compute_sha256,
    load_listings_data,
    parse_price_value,
    safe_acquire_raw_data,
    verify_file_checksum,
)


class TestPriceParsing:
    """Kiểm thử hàm parse_price_value với định dạng chuẩn và các trường hợp biên (F5)."""

    def test_parse_standard_currency_string(self) -> None:
        """Kiểm tra parse chuỗi tiền tệ chuẩn có ký hiệu $ và dấu phẩy."""
        assert parse_price_value("$1,148.24") == pytest.approx(1148.24)
        assert parse_price_value("$25,106.00") == pytest.approx(25106.00)
        assert parse_price_value("$807.00") == pytest.approx(807.00)

    def test_parse_baht_symbol_string(self) -> None:
        """Kiểm tra parse chuỗi có ký hiệu Thái Baht (฿)."""
        assert parse_price_value("฿5,741.18") == pytest.approx(5741.18)
        assert parse_price_value("฿723.25") == pytest.approx(723.25)

    def test_parse_numeric_types(self) -> None:
        """Kiểm tra khi giá trị đã là kiểu số int hoặc float."""
        assert parse_price_value(1500) == pytest.approx(1500.0)
        assert parse_price_value(99.99) == pytest.approx(99.99)

    def test_parse_negative_prices(self) -> None:
        """Kiểm tra parse giá âm để phục vụ kiểm toán phát hiện giá bất thường."""
        assert parse_price_value("-50.0") == pytest.approx(-50.0)
        assert parse_price_value("-$1,148.24") == pytest.approx(-1148.24)
        assert parse_price_value("$-50.00") == pytest.approx(-50.0)

    def test_parse_missing_and_empty_values(self) -> None:
        """Kiểm tra xử lý an toàn giá trị khuyết và chuỗi rỗng."""
        assert np.isnan(parse_price_value(np.nan))
        assert np.isnan(parse_price_value(None))
        assert np.isnan(parse_price_value(""))
        assert np.isnan(parse_price_value("   "))

    def test_parse_invalid_strings(self) -> None:
        """Kiểm tra khi gặp chuỗi không thể chuyển đổi thành số."""
        assert np.isnan(parse_price_value("free"))
        assert np.isnan(parse_price_value("contact_host"))
        assert np.isnan(parse_price_value("N/A"))

    def test_parse_invalid_groupings_and_locales(self) -> None:
        """Regression test F5: Từ chối các chuỗi phân cách sai quy chuẩn hoặc định dạng khác locale."""
        assert np.isnan(parse_price_value("1,2,3"))
        assert np.isnan(parse_price_value("1,50"))
        assert np.isnan(parse_price_value("1,23"))
        assert np.isnan(parse_price_value("1,2345.6"))

    def test_parse_booleans_and_infinities(self) -> None:
        """Regression test F5: Từ chối các giá trị boolean và vô cực."""
        assert np.isnan(parse_price_value(True))
        assert np.isnan(parse_price_value(False))
        assert np.isnan(parse_price_value("inf"))
        assert np.isnan(parse_price_value("-inf"))
        assert np.isnan(parse_price_value("+inf"))
        assert np.isnan(parse_price_value("infinity"))
        assert np.isnan(parse_price_value(float("inf")))
        assert np.isnan(parse_price_value(float("-inf")))


class TestChecksumAndIntegrity:
    """Kiểm thử hàm tính toán và xác thực mã băm SHA-256."""

    def test_compute_and_verify_sha256(self, tmp_path: Path) -> None:
        """Kiểm tra tính toán mã băm trên file mẫu."""
        test_file = tmp_path / "sample_data.txt"
        test_file.write_text("IE313 Data Analysis Bangkok Airbnb", encoding="utf-8")

        computed_hash = compute_sha256(test_file)
        assert isinstance(computed_hash, str)
        assert len(computed_hash) == 64

        # Xác thực đúng
        assert verify_file_checksum(test_file, computed_hash)
        assert verify_file_checksum(test_file, computed_hash.upper())

        # Xác thực sai khi hash không khớp
        assert not verify_file_checksum(test_file, "0" * 64)

    def test_compute_sha256_missing_file_raises_error(self) -> None:
        """Kiểm tra ném lỗi FileNotFoundError khi tệp tin không tồn tại."""
        with pytest.raises(FileNotFoundError):
            compute_sha256("non_existent_file_path_xyz.csv")


class TestAuditStructureLogic:
    """Kiểm thử logic kiểm toán cấu trúc, ô khuyết toàn bảng và trùng lặp (F1)."""

    @pytest.fixture
    def sample_listings_df(self) -> pd.DataFrame:
        """Tạo fixture DataFrame nhỏ đại diện cho dữ liệu chỗ ở."""
        return pd.DataFrame(
            {
                "id": [101, 102, 103, 104, 105],
                "last_scraped": [
                    "2026-06-29",
                    "2026-06-29",
                    "2026-06-30",
                    "2026-06-30",
                    "2026-07-01",
                ],
                "room_type": [
                    "Entire home/apt",
                    "Private room",
                    "Entire home/apt",
                    "Shared room",
                    "Entire home/apt",
                ],
                "property_type": ["Condo", "Apartment", "Condo", "Hostel", "Villa"],
                "neighbourhood_cleansed": [
                    "Watthana",
                    "Khlong Toei",
                    "Watthana",
                    "Bang Rak",
                    "Sathon",
                ],
                "accommodates": [2, 1, 4, 1, 6],
                "bedrooms": [1.0, 1.0, 2.0, np.nan, 3.0],
                "bathrooms": [1.0, 1.0, 2.0, 1.0, 3.5],
                "beds": [1.0, 1.0, 2.0, 1.0, np.nan],
                "minimum_nights": [1, 2, 3, 1, 5],
                "number_of_reviews": [10, 0, 45, 5, 2],
                "review_scores_rating": [4.85, np.nan, 4.90, 4.20, 5.0],
                "host_is_superhost": ["t", "f", "t", "f", "t"],
                "price": ["$1,200.00", "$800.00", "$2,500.00", "$300.00", "$15,000.00"],
            }
        )

    def test_audit_dataset_structure_unique_ids(self, sample_listings_df: pd.DataFrame) -> None:
        """Kiểm tra phát hiện chính xác khi không có trùng lặp ID và tính ô khuyết toàn bảng."""
        res = audit_dataset_structure(sample_listings_df)
        assert res["total_rows"] == 5
        assert res["total_columns"] == 14
        assert res["total_cells"] == 70
        assert (
            res["total_missing_cells"] == 3
        )  # bedrooms, beds, review_scores_rating mỗi cột khuyết 1
        assert res["total_missing_cells_pct"] == pytest.approx(4.29, abs=0.01)
        assert res["complete_duplicate_rows"] == 0
        assert res["unique_ids_count"] == 5
        assert res["duplicate_id_rows"] == 0
        assert res["is_one_row_per_listing"] is True
        assert "int64" in res["dtype_counts"] or "float64" in res["dtype_counts"]

    def test_audit_dataset_structure_with_duplicates(
        self, sample_listings_df: pd.DataFrame
    ) -> None:
        """Kiểm tra phát hiện khi có dòng trùng lặp ID và trùng lặp toàn bộ."""
        duplicated_df = pd.concat(
            [sample_listings_df, sample_listings_df.iloc[[0]]], ignore_index=True
        )
        res = audit_dataset_structure(duplicated_df)
        assert res["total_rows"] == 6
        assert res["unique_ids_count"] == 5
        assert res["duplicate_id_rows"] == 1
        assert res["complete_duplicate_rows"] == 1
        assert res["is_one_row_per_listing"] is False

    def test_audit_column_groups(self, sample_listings_df: pd.DataFrame) -> None:
        """Kiểm tra phân loại nhóm cột bảo đảm tổng đúng số cột."""
        res = audit_column_groups(sample_listings_df)
        assert res["total_columns_categorized"] == len(sample_listings_df.columns)
        assert "group_counts" in res


class TestPriceAuditCalculations:
    """Kiểm thử tính toán thống kê và ngưỡng ngoại lai cho biến giá."""

    def test_audit_price_field_descriptive_stats(self) -> None:
        """Kiểm tra thống kê mô tả 5 số, IQR và ngưỡng ngoại lai."""
        df = pd.DataFrame(
            {
                "price": [
                    "$100.00",
                    "$200.00",
                    "$300.00",
                    "$400.00",
                    "$500.00",
                    "$600.00",
                    "$700.00",
                    "$10,000.00",
                    None,
                ]
            }
        )
        res = audit_price_field(df)

        assert res["total_rows"] == 9
        assert res["raw_null_count"] == 1
        assert res["valid_count"] == 8
        assert res["zero_price_count"] == 0
        assert res["negative_price_count"] == 0

        stats_dict = res["descriptive_statistics"]
        assert stats_dict["min"] == 100.0
        assert stats_dict["max"] == 10000.0
        assert stats_dict["median"] == 450.0
        assert stats_dict["outliers_count_1_5_iqr"] >= 1
        assert stats_dict["skewness"] > 0

    def test_audit_price_field_empty_or_all_null(self) -> None:
        """Kiểm tra khi cột giá hoàn toàn khuyết hoặc rỗng."""
        df = pd.DataFrame({"price": [None, None, np.nan]})
        res = audit_price_field(df)
        assert res["valid_count"] == 0
        assert res["raw_null_count"] == 3
        assert res["error"] == "NO_VALID_PRICES_FOUND"


class TestCurrencyAndQuoteComparison:
    """Kiểm thử đối chiếu tiền tệ và tách biệt exact match vs tolerance match (F5)."""

    def test_exact_matches_vs_tolerance_matches(self) -> None:
        """Regression test F5: Phân biệt chính xác giữa diff == 0.0 và diff <= 0.05."""
        # Row 1: diff == 0.0 (exact match)
        # Row 2: 100.00 vs 100.04 (diff == 0.04 -> tolerance match, NOT exact match)
        # Row 3: 100.00 vs 100.10 (diff == 0.10 -> neither exact nor tolerance match)
        df = pd.DataFrame(
            {
                "price": ["$100.00", "$100.00", "$100.00"],
                "price_quote_price_per_night": [100.00, 100.04, 100.10],
                "price_quote_raw": [
                    '{"quote": {"raw_price_line_items": [{"description": "฿100.00"}]}}',
                    '{"quote": {"raw_price_line_items": [{"description": "฿100.04"}]}}',
                    '{"quote": {"raw_price_line_items": [{"description": "฿100.10"}]}}',
                ],
            }
        )
        res = audit_currency_and_pricing_granularity(df)
        comp = res["price_vs_quote_per_night_comparison"]

        assert comp["total_compared"] == 3
        assert comp["exact_matches"] == 1  # Chỉ row 1
        assert comp["tolerance_matches"] == 2  # Row 1 và Row 2
        assert comp["tolerance_threshold"] == 0.05
        assert comp["max_difference"] == pytest.approx(0.10, abs=1e-4)

    def test_quote_sample_less_than_100_and_json_errors(self) -> None:
        """Regression test F5: Mẫu quote < 100 không bị hardcode mẫu số 100, xử lý JSON lỗi an toàn."""
        df = pd.DataFrame(
            {
                "price_quote_raw": [
                    '{"quote": {"raw_price_line_items": [{"description": "฿100"}]}}',
                    "MALFORMED_JSON_STRING",
                    '{"quote": {"raw_price_line_items": []}}',
                ]
            }
        )
        res = audit_currency_and_pricing_granularity(df)
        assert res["quote_sample_evaluated_count"] == 3
        assert res["quote_sample_with_baht_symbol"] == 1
        assert res["quote_sample_json_errors"] == 1


class TestHostClustering:
    """Kiểm thử gom cụm chủ nhà và xử lý trường hợp biên rỗng/all-null (F5)."""

    def test_audit_host_clustering_standard(self) -> None:
        """Kiểm tra thống kê chủ nhà trên tập dữ liệu chuẩn."""
        df = pd.DataFrame({"host_id": [1, 1, 1, 2, 2, 3]})
        res = audit_host_clustering(df)
        assert res["unique_hosts_count"] == 3
        assert res["multi_listing_hosts_count"] == 2
        assert res["single_listing_hosts_count"] == 1
        assert res["multi_listing_hosts_pct"] == pytest.approx(66.67, abs=0.01)
        assert res["max_listings_single_host"] == 3
        assert res["top_5_hosts"]["1"] == 3

    def test_audit_host_clustering_empty_and_null_edge_cases(self) -> None:
        """Regression test F5: DataFrame rỗng hoặc all-null không gây ZeroDivisionError."""
        # DataFrame rỗng
        empty_df = pd.DataFrame({"host_id": []})
        res_empty = audit_host_clustering(empty_df)
        assert res_empty["unique_hosts_count"] == 0
        assert res_empty["multi_listing_hosts_count"] == 0
        assert res_empty["mean_listings_per_host"] is None

        # DataFrame all-null
        null_df = pd.DataFrame({"host_id": [np.nan, None]})
        res_null = audit_host_clustering(null_df)
        assert res_null["unique_hosts_count"] == 0
        assert res_null["mean_listings_per_host"] is None


class TestCandidateVariablesAndCatalog:
    """Kiểm thử kiểm toán 12 biến ứng viên và phát sinh danh mục cột."""

    def test_audit_candidate_variables(self) -> None:
        """Kiểm tra nhận diện đúng biến hiện diện và biến thiếu trên danh sách CANDIDATE_FEATURES."""
        df = pd.DataFrame(
            {
                "price": ["$100.00"],
                "room_type": ["Entire home/apt"],
                "accommodates": [2],
            }
        )
        res = audit_candidate_variables(df)
        assert len(res) == len(CANDIDATE_FEATURES)
        assert res["price"]["present"] is True
        assert res["room_type"]["present"] is True
        assert res["accommodates"]["present"] is True
        assert res["bedrooms"]["present"] is False

    def test_audit_temporal_coverage(self) -> None:
        """Kiểm tra phân tích phạm vi ngày cào dữ liệu qua last_scraped."""
        df = pd.DataFrame(
            {"last_scraped": ["2026-06-29", "2026-06-29", "2026-07-02", "2026-06-30"]}
        )
        res = audit_temporal_coverage(df)
        assert res["distinct_dates_count"] == 3
        assert res["earliest_date"] == "2026-06-29"
        assert res["latest_date"] == "2026-07-02"
        assert res["date_distribution"]["2026-06-29"] == 2

    def test_generate_columns_catalog_structure(self) -> None:
        """Kiểm tra cấu trúc và 10 cột trong catalog xuất ra."""
        df = pd.DataFrame(
            {
                "id": [1],
                "price": ["$100.00"],
                "room_type": ["Private room"],
                "host_id": [999],
            }
        )
        catalog = generate_columns_catalog(df)
        assert len(catalog) == 4
        expected_cols = [
            "stt",
            "column_name",
            "data_type",
            "null_count",
            "null_pct",
            "unique_values_count",
            "sample_value",
            "analytical_role",
            "dictionary_description",
            "source_status",
        ]
        assert list(catalog.columns) == expected_cols


class TestChecksumFailureAndIntegrity:
    """Kiểm thử hành vi khi sai lệch mã băm (F3)."""

    def test_run_full_audit_mismatch_raises_value_error(self, tmp_path: Path) -> None:
        """Regression test F3: Sai mã băm ném ValueError TRƯỚC KHI ghi/tạo báo cáo."""
        raw_csv = tmp_path / "test_data.csv"
        raw_csv.write_text("id,price\n1,$100.00\n", encoding="utf-8")
        out_dir = tmp_path / "audit_out"

        with pytest.raises(ValueError, match="Mã băm SHA-256 không khớp"):
            run_full_audit(raw_csv, out_dir, expected_sha256="0" * 64)

        # Đảm bảo thư mục đầu ra không được tạo hoặc không có file báo cáo mới
        assert not (out_dir / "bangkok_audit_summary.json").exists()

    def test_run_full_audit_mismatch_does_not_overwrite_existing_reports(
        self, tmp_path: Path
    ) -> None:
        """Regression test F3: Sai mã băm giữ nguyên file báo cáo cũ nếu đã tồn tại."""
        raw_csv = tmp_path / "test_data.csv"
        raw_csv.write_text("id,price\n1,$100.00\n", encoding="utf-8")
        out_dir = tmp_path / "audit_out"
        out_dir.mkdir(parents=True)
        old_file = out_dir / "bangkok_audit_summary.json"
        old_file.write_text('{"old_report": true}', encoding="utf-8")

        with pytest.raises(ValueError, match="Mã băm SHA-256 không khớp"):
            run_full_audit(raw_csv, out_dir, expected_sha256="0" * 64)

        # File cũ vẫn còn nguyên nội dung
        assert old_file.read_text(encoding="utf-8") == '{"old_report": true}'

    def test_run_full_audit_without_expected_sha256(self, tmp_path: Path) -> None:
        """Regression test F3: Không truyền expected_sha256 ghi nhận NOT_CHECKED, không báo Verified."""
        raw_csv = tmp_path / "test_data.csv"
        raw_csv.write_text("id,price\n1,$100.00\n", encoding="utf-8")
        out_dir = tmp_path / "audit_out"

        summary = run_full_audit(raw_csv, out_dir, expected_sha256=None)
        meta = summary["audit_metadata"]
        assert meta["checksum_status"] == "NOT_CHECKED"
        assert meta["checksum_verified"] is None

    def test_cli_checksum_mismatch_exits_code_1(self, tmp_path: Path) -> None:
        """Regression test F3: CLI main() khi sai mã băm thoát với exit code 1."""
        raw_csv = tmp_path / "test_data.csv"
        raw_csv.write_text("id,price\n1,$100.00\n", encoding="utf-8")
        out_dir = tmp_path / "audit_out"

        test_args = [
            "data_audit.py",
            "--input",
            str(raw_csv),
            "--output-dir",
            str(out_dir),
            "--expected-sha256",
            "0" * 64,
        ]
        with patch.object(sys, "argv", test_args):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1


class TestSafeAcquisitionAndImmutability:
    """Kiểm thử tính bất biến của dữ liệu thô và quy trình thu thập không phá hủy (F4)."""

    def test_loader_does_not_modify_source_file(self, tmp_path: Path) -> None:
        """Đảm bảo việc nạp dữ liệu không làm thay đổi checksum hay mtime của file gốc."""
        raw_csv = tmp_path / "raw_test_data.csv"
        content = "id,price,room_type\n1,$100.00,Private room\n2,$200.00,Entire home/apt\n"
        raw_csv.write_text(content, encoding="utf-8")

        initial_hash = compute_sha256(raw_csv)
        initial_mtime = raw_csv.stat().st_mtime_ns

        df = load_listings_data(raw_csv, parse_prices=True)
        assert len(df) == 2

        after_hash = compute_sha256(raw_csv)
        after_mtime = raw_csv.stat().st_mtime_ns

        assert after_hash == initial_hash, "Mã băm file thô bị thay đổi sau khi nạp!"
        assert after_mtime == initial_mtime, "Thời gian sửa đổi file thô bị thay đổi!"

    def test_safe_acquire_raw_data_already_exists(self, tmp_path: Path) -> None:
        """Regression test F4: Nếu tệp đích đã tồn tại và khớp mã băm thì tái sử dụng, không tải đè."""
        dest_file = tmp_path / "listings.csv"
        dest_file.write_text("id,price\n1,$10.0\n", encoding="utf-8")
        dest_hash = compute_sha256(dest_file)
        mtime_before = dest_file.stat().st_mtime_ns

        res = safe_acquire_raw_data(
            source_url="http://mock-url.invalid/file",
            target_filepath=dest_file,
            expected_sha256=dest_hash,
        )
        assert res["status"] == "ALREADY_EXISTS_VERIFIED"
        assert dest_file.stat().st_mtime_ns == mtime_before

    def test_safe_acquire_raw_data_existing_mismatch_preserves_file(self, tmp_path: Path) -> None:
        """Regression test F4: Tệp đích có sẵn sai hash thì ném lỗi và GIỮ NGUYÊN tệp, không xóa."""
        dest_file = tmp_path / "listings.csv"
        dest_file.write_text("existing_content", encoding="utf-8")

        with pytest.raises(ValueError, match="không khớp mã băm kỳ vọng"):
            safe_acquire_raw_data(
                source_url="http://mock-url.invalid/file",
                target_filepath=dest_file,
                expected_sha256="0" * 64,
            )

        assert dest_file.is_file(), "Tệp đích bị xóa trái quy định!"
        assert dest_file.read_text(encoding="utf-8") == "existing_content"

    def test_safe_acquire_raw_data_download_mismatch_cleans_tmp_and_preserves_dest(
        self, tmp_path: Path
    ) -> None:
        """Regression test F4: Khi tải về sai mã băm, hủy file tạm và không tạo tệp đích."""
        dest_file = tmp_path / "listings_new.csv"

        # Mock urllib.request.urlopen để trả về nội dung giả lập
        mock_response = MagicMock()
        mock_response.read.side_effect = [b"downloaded_bytes", b""]
        mock_response.__enter__.return_value = mock_response

        with patch("urllib.request.urlopen", return_value=mock_response):
            with pytest.raises(ValueError, match="Mã băm của tệp tải về không khớp"):
                safe_acquire_raw_data(
                    source_url="http://mock-url.invalid/file",
                    target_filepath=dest_file,
                    expected_sha256="0" * 64,
                    temp_dir=tmp_path,
                )

        assert not dest_file.exists(), "Tệp đích không được tạo khi sai hash!"
        # Đảm bảo không còn tệp tạm nào sót lại
        tmp_files = list(tmp_path.glob(".tmp_*"))
        assert len(tmp_files) == 0, "Tệp tạm chưa được dọn dẹp!"


class TestMarkdownSync:
    """Kiểm thử cơ chế tự động đồng bộ Markdown từ dữ liệu máy đọc (F6)."""

    def test_generate_data_audit_markdown(self, tmp_path: Path) -> None:
        """Regression test F6: Phiếu kiểm toán Markdown được tạo với số liệu chính xác từ JSON summary."""
        raw_csv = tmp_path / "test_listings.csv"
        df = pd.DataFrame(
            {
                "id": [1, 2],
                "price": ["$100.00", "$200.00"],
                "room_type": ["Entire home/apt", "Private room"],
                "last_scraped": ["2026-06-29", "2026-06-29"],
                "host_id": [10, 20],
            }
        )
        df.to_csv(raw_csv, index=False)

        out_dir = tmp_path / "audit_reports"
        summary = run_full_audit(raw_csv, out_dir)
        catalog = generate_columns_catalog(df)

        md_path = tmp_path / "DATA_AUDIT_TEST.md"
        md_text = generate_data_audit_markdown(summary, catalog, output_markdown_path=md_path)

        assert md_path.is_file()
        assert "**Tổng số dòng (quan trắc)**: `2` dòng." in md_text
        assert "Listing Snapshot" in md_text
        assert "Thái Baht (THB)" in md_text
