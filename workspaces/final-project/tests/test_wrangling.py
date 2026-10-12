"""Kiểm thử chính sách làm sạch và chống rò rỉ dữ liệu qua sản phẩm bàn giao."""

import json

import numpy as np
import pandas as pd
import pytest

from src.data_loader import compute_sha256
from src.wrangling import MODEL_FEATURES, clean_listings, price_outlier_report, run_cleaning


@pytest.fixture
def listings():
    """Mẫu đủ schema có khuyết predictor và hai mức giá cực đoan dương."""
    return pd.DataFrame(
        {
            "id": range(1, 7),
            "host_id": [1, 1, 2, 3, 4, 4],
            "last_scraped": ["2026-06-29"] * 6,
            "price": ["$1", "$100", "$200", "$300", "$400", "$1,320,255"],
            "room_type": [" Private room "] * 6,
            "property_type": ["Room"] * 6,
            "neighbourhood_cleansed": ["District"] * 6,
            "accommodates": [1] * 6,
            "bedrooms": [0, None, 1, 1, 2, 2],
            "bathrooms": [0.5, 1, None, 1, 2, 2],
            "beds": [1, 1, 1, 1, 2, None],
            "minimum_nights": [1] * 6,
            "number_of_reviews": [0, 0, 3, 4, 5, 5],
            "review_scores_rating": [None, None, 4, 4, 5, 5],
            "host_is_superhost": ["t", "f", "t", "f", "t", "f"],
            "price_quote_price_per_night": [1, 100, 200, 300, 400, 1320255],
            "estimated_revenue_l365d": [1000] * 6,
        }
    )


def test_keeps_extremes_missing_predictors_and_input(listings):
    """Không cắt giá, không tự điền khuyết, không chạm DataFrame nguồn."""
    original = listings.copy(deep=True)
    clean, summary, excluded = clean_listings(listings)
    pd.testing.assert_frame_equal(original, listings)
    assert len(clean) == 6 and excluded.empty
    assert clean["price"].tolist() == [1, 100, 200, 300, 400, 1320255]
    assert clean["bedrooms"].isna().sum() == 1 and clean["bedrooms"].iloc[0] == 0
    assert clean["room_type"].unique().tolist() == ["Private room"]
    assert "price_quote_price_per_night" not in clean
    assert "estimated_revenue_l365d" not in clean
    assert not set(MODEL_FEATURES) & {"price", "price_raw", "id", "host_id", "last_scraped"}
    assert not summary["imputation_applied"]
    flagged, iqr = price_outlier_report(clean)
    assert flagged["id"].tolist() == [6]
    assert iqr["removed_count"] == 0 and len(clean) == 6


def test_exclusion_reasons_account_for_every_removed_row(listings):
    listings["price"] = [None, "1,2,3", "$0", "$-3", "inf", "$100"]
    clean, summary, excluded = clean_listings(listings)
    assert clean["id"].tolist() == [6]
    assert summary["rows_removed"] == 5
    assert excluded["reason"].value_counts().to_dict() == {
        "invalid_price_format": 2,
        "nonpositive_price": 2,
        "missing_price": 1,
    }


def test_duplicates_only_removed_if_identical(listings):
    duplicated = pd.concat([listings, listings.iloc[[0]]], ignore_index=True)
    clean, summary, _ = clean_listings(duplicated)
    assert len(clean) == 6 and summary["exact_duplicates_removed"] == 1
    duplicated.loc[6, "price"] = "$20"
    with pytest.raises(ValueError, match="ID thiếu hoặc trùng"):
        clean_listings(duplicated)


def test_invalid_predictors_become_missing_without_filling(listings):
    listings["accommodates"] = [0, 1.5, np.inf, 3, 4, 5]
    listings.loc[0, "host_is_superhost"] = "unknown"
    clean, summary, _ = clean_listings(listings)
    assert clean["accommodates"].isna().sum() == 3
    assert pd.isna(clean["host_is_superhost"].iloc[0])
    assert summary["predictor_changes"]["accommodates"]["invalid_observed_to_missing"] == 3


def test_schema_and_empty_results_fail(listings):
    with pytest.raises(ValueError, match="Thiếu cột"):
        clean_listings(listings.drop(columns="price"))
    listings["price"] = None
    with pytest.raises(ValueError, match="Không còn dòng"):
        clean_listings(listings)


def test_pipeline_reproducible_preserves_raw_and_rejects_bad_hash(tmp_path, listings):
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()
    raw = raw_dir / "fixture.csv"
    listings.to_csv(raw, index=False)
    original = (compute_sha256(raw), raw.stat().st_mtime_ns)
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({"sha256": original[0]}))
    output, reports = tmp_path / "processed", tmp_path / "reports"
    first = run_cleaning(raw, manifest, output, reports)
    csv = (output / "bangkok_cleaned.csv").read_bytes()
    assert run_cleaning(raw, manifest, output, reports) == first
    assert (output / "bangkok_cleaned.csv").read_bytes() == csv
    assert (compute_sha256(raw), raw.stat().st_mtime_ns) == original
    with pytest.raises(ValueError, match="raw"):
        run_cleaning(raw, manifest, raw_dir, reports)
    manifest.write_text(json.dumps({"sha256": "0" * 64}))
    with pytest.raises(ValueError, match="Checksum"):
        run_cleaning(raw, manifest, output, reports)
    assert (output / "bangkok_cleaned.csv").read_bytes() == csv
