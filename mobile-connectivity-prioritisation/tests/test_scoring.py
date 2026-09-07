import pandas as pd

from src.connectivity_pipeline import (
    REQUIRED_FOR_ANALYSIS,
    YEAR_COLUMNS,
    add_priority_framework,
    percentile_score,
)


def _sample_latest_table():
    rows = [
        {
            "countryiso3code": "AAA",
            "country_name": "Alpha",
            "internet_usage_pct": 20.0,
            "mobile_subscriptions_per_100": 50.0,
            "population": 10_000_000,
            "gdp_per_capita": 1_000.0,
            "rural_population_pct": 70.0,
        },
        {
            "countryiso3code": "BBB",
            "country_name": "Beta",
            "internet_usage_pct": 70.0,
            "mobile_subscriptions_per_100": 90.0,
            "population": 5_000_000,
            "gdp_per_capita": 5_000.0,
            "rural_population_pct": 40.0,
        },
        {
            "countryiso3code": "CCC",
            "country_name": "Gamma",
            "internet_usage_pct": 95.0,
            "mobile_subscriptions_per_100": 120.0,
            "population": 2_000_000,
            "gdp_per_capita": 30_000.0,
            "rural_population_pct": 10.0,
        },
    ]
    df = pd.DataFrame(rows)
    for col in YEAR_COLUMNS:
        df[col] = 2024
    df["latest_year"] = 2024
    df["earliest_year"] = 2024
    df["year_spread"] = 0
    df["complete_core_data"] = True
    return df


def test_percentile_score_direction():
    s = pd.Series([1, 2, 3])
    assert percentile_score(s).iloc[2] > percentile_score(s).iloc[0]
    assert percentile_score(s, higher_is_worse=False).iloc[0] > percentile_score(
        s, higher_is_worse=False
    ).iloc[2]


def test_priority_pipeline_orders_severe_case_first():
    result = add_priority_framework(_sample_latest_table())
    assert result.iloc[0]["country_name"] == "Alpha"
    assert result.iloc[-1]["country_name"] == "Gamma"
    assert set(REQUIRED_FOR_ANALYSIS).issubset(result.columns)


def test_benchmark_gap_is_capped_at_zero():
    result = add_priority_framework(_sample_latest_table())
    gamma = result.loc[result["country_name"] == "Gamma"].iloc[0]
    assert gamma["usage_gap_pp"] == 0
