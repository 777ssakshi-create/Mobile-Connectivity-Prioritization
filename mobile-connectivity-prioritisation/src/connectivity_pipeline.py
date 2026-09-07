"""Reproducible pipeline for the Mobile Connectivity Prioritisation case study.

The notebook remains the narrative analysis. This module provides a cleaner,
scriptable version of the core data retrieval, quality checks and prioritisation
logic for portfolio/repository use.

Important: the 80% benchmark, score weights, priority bands and diagnostic rules
are project assumptions for an independent case study. They are not an official
GSMA scoring model or universal policy target.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd
import requests

BASE_URL = "https://api.worldbank.org/v2"
START_YEAR = 2015
END_YEAR = 2025
USAGE_BENCHMARK = 80.0

INDICATORS: Dict[str, str] = {
    "internet_usage_pct": "IT.NET.USER.ZS",
    "mobile_subscriptions_per_100": "IT.CEL.SETS.P2",
    "population": "SP.POP.TOTL",
    "gdp_per_capita": "NY.GDP.PCAP.CD",
    "rural_population_pct": "SP.RUR.TOTL.ZS",
}

REQUIRED_FOR_ANALYSIS = list(INDICATORS.keys())
YEAR_COLUMNS = [f"{x}_year" for x in REQUIRED_FOR_ANALYSIS]

WEIGHTS = {
    "gap_score": 0.35,
    "population_impact_score": 0.30,
    "rural_score": 0.15,
    "economic_vulnerability_score": 0.20,
}

ALT_WEIGHTS = {
    "gap_score": 0.25,
    "population_impact_score": 0.40,
    "rural_score": 0.15,
    "economic_vulnerability_score": 0.20,
}


def _get_json(url: str) -> list:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, list) or len(payload) < 2:
        raise ValueError(f"Unexpected World Bank API response: {url}")
    return payload


def fetch_country_catalogue() -> pd.DataFrame:
    """Return country/territory records and exclude World Bank aggregates."""
    payload = _get_json(f"{BASE_URL}/country?format=json&per_page=400")
    rows = []
    for item in payload[1]:
        region = item.get("region") or {}
        # World Bank aggregate rows are marked as Aggregates / region id NA.
        if region.get("value") == "Aggregates" or region.get("id") == "NA":
            continue
        rows.append(
            {
                "countryiso3code": str(item.get("id", "")).upper().strip(),
                "country_name": str(item.get("name", "")).strip(),
            }
        )
    return pd.DataFrame(rows).drop_duplicates("countryiso3code")


def fetch_world_bank_indicator(
    indicator_code: str,
    start_year: int = START_YEAR,
    end_year: int = END_YEAR,
    country: str = "all",
) -> pd.DataFrame:
    """Fetch one World Bank indicator for the requested date range."""
    url = (
        f"{BASE_URL}/country/{country}/indicator/{indicator_code}"
        f"?format=json&per_page=20000&date={start_year}:{end_year}"
    )
    payload = _get_json(url)
    df = pd.DataFrame(payload[1])
    if df.empty:
        return df

    keep = ["countryiso3code", "country", "date", "value", "indicator"]
    df = df[[c for c in keep if c in df.columns]].copy()
    df["date"] = pd.to_numeric(df["date"], errors="coerce")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    # The API returns country as a nested object. Parse it rather than casting
    # the dictionary itself to a string.
    if "country" in df.columns:
        df["country_name"] = df["country"].apply(
            lambda x: x.get("value") if isinstance(x, dict) else x
        )
    return df


def download_indicators() -> Dict[str, pd.DataFrame]:
    return {
        name: fetch_world_bank_indicator(code)
        for name, code in INDICATORS.items()
    }


def build_country_year_table(
    raw_data: Dict[str, pd.DataFrame],
    country_catalogue: pd.DataFrame,
) -> pd.DataFrame:
    """Build one country-year analytical table across all indicators."""
    valid_codes = set(country_catalogue["countryiso3code"].dropna())
    merged: pd.DataFrame | None = None

    for name, raw in raw_data.items():
        df = raw.copy().rename(columns={"value": name, "date": "year"})
        df["countryiso3code"] = (
            df["countryiso3code"].astype(str).str.upper().str.strip()
        )
        df = df[df["countryiso3code"].isin(valid_codes)].copy()
        df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
        df = df[["countryiso3code", "year", name]].drop_duplicates(
            ["countryiso3code", "year"]
        )
        merged = df if merged is None else merged.merge(
            df, on=["countryiso3code", "year"], how="outer", validate="one_to_one"
        )

    if merged is None:
        raise ValueError("No indicator data supplied")

    merged = merged.merge(
        country_catalogue, on="countryiso3code", how="left", validate="many_to_one"
    )
    return merged.sort_values(["countryiso3code", "year"]).reset_index(drop=True)


def latest_by_country(df: pd.DataFrame, value_column: str) -> pd.DataFrame:
    temp = df[["countryiso3code", "year", value_column]].dropna(
        subset=[value_column]
    )
    return (
        temp.sort_values(["countryiso3code", "year"])
        .groupby("countryiso3code", as_index=False)
        .tail(1)
        .rename(columns={"year": f"{value_column}_year"})
    )


def build_latest_table(
    analysis_df: pd.DataFrame, country_catalogue: pd.DataFrame
) -> pd.DataFrame:
    latest_df = country_catalogue.copy()
    for indicator in REQUIRED_FOR_ANALYSIS:
        latest = latest_by_country(analysis_df, indicator)
        latest_df = latest_df.merge(
            latest, on="countryiso3code", how="left", validate="one_to_one"
        )

    latest_df["latest_year"] = latest_df[YEAR_COLUMNS].max(axis=1)
    latest_df["earliest_year"] = latest_df[YEAR_COLUMNS].min(axis=1)
    latest_df["year_spread"] = latest_df["latest_year"] - latest_df["earliest_year"]
    latest_df["complete_core_data"] = latest_df[REQUIRED_FOR_ANALYSIS].notna().all(axis=1)
    return latest_df


def percentile_score(series: pd.Series, higher_is_worse: bool = True) -> pd.Series:
    ranks = series.rank(pct=True, method="average") * 100
    return ranks if higher_is_worse else 100 - ranks


def confidence_rating(row: pd.Series) -> str:
    years = row[YEAR_COLUMNS].dropna()
    completeness = row[REQUIRED_FOR_ANALYSIS].notna().mean()
    if len(years) == 0:
        return "Low"
    spread = years.max() - years.min()
    if completeness == 1 and spread <= 1:
        return "High"
    if completeness >= 0.8 and spread <= 3:
        return "Medium"
    return "Low"


def _diagnostic_segment_factory(df: pd.DataFrame):
    gap_median = df["usage_gap_pp"].median()
    rural_median = df["rural_population_pct"].median()
    gdp_median = df["gdp_per_capita"].median()
    mobile_median = df["mobile_subscriptions_per_100"].median()

    def diagnostic_segment(row: pd.Series) -> str:
        high_gap = row["usage_gap_pp"] >= gap_median
        high_rural = row["rural_population_pct"] >= rural_median
        low_gdp = row["gdp_per_capita"] <= gdp_median
        high_mobile = row["mobile_subscriptions_per_100"] >= mobile_median

        if high_gap and high_rural:
            return "Investigate rural/access barriers"
        if high_gap and low_gdp:
            return "Investigate affordability/economic barriers"
        if high_gap and high_mobile:
            return "Investigate usage/adoption barriers"
        if high_gap:
            return "Mixed barriers — investigate"
        return "Lower immediate gap"

    return diagnostic_segment


def add_priority_framework(latest_df: pd.DataFrame) -> pd.DataFrame:
    """Apply the case-study benchmark, scoring, confidence and sensitivity logic."""
    df = latest_df.dropna(subset=REQUIRED_FOR_ANALYSIS).copy()

    df["usage_gap_pp"] = (USAGE_BENCHMARK - df["internet_usage_pct"]).clip(lower=0)
    df["population_affected_est"] = df["population"] * df["usage_gap_pp"] / 100

    df["gap_score"] = percentile_score(df["usage_gap_pp"])
    df["population_impact_score"] = percentile_score(df["population_affected_est"])
    df["rural_score"] = percentile_score(df["rural_population_pct"])
    df["economic_vulnerability_score"] = percentile_score(
        df["gdp_per_capita"], higher_is_worse=False
    )

    df["priority_score"] = sum(df[col] * weight for col, weight in WEIGHTS.items())
    df["priority_band"] = pd.cut(
        df["priority_score"],
        bins=[-np.inf, 33.33, 66.67, np.inf],
        labels=["Lower", "Medium", "Higher"],
    )
    df["data_confidence"] = df.apply(confidence_rating, axis=1)

    df["priority_score_alt"] = sum(
        df[col] * weight for col, weight in ALT_WEIGHTS.items()
    )
    df["rank_base"] = df["priority_score"].rank(ascending=False, method="min")
    df["rank_alt"] = df["priority_score_alt"].rank(ascending=False, method="min")
    df["rank_change"] = df["rank_base"] - df["rank_alt"]

    df["diagnostic_segment"] = df.apply(_diagnostic_segment_factory(df), axis=1)
    df = df.sort_values("priority_score", ascending=False).reset_index(drop=True)
    df["display_rank"] = np.arange(1, len(df) + 1)
    return df


def run_pipeline(output_dir: str | Path = "data/processed") -> pd.DataFrame:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    countries = fetch_country_catalogue()
    raw_data = download_indicators()
    country_year = build_country_year_table(raw_data, countries)
    latest = build_latest_table(country_year, countries)
    priority = add_priority_framework(latest)

    priority.to_csv(output_dir / "connectivity_priority_market_only.csv", index=False)
    return priority


if __name__ == "__main__":
    result = run_pipeline()
    print(f"Exported {len(result):,} market records.")
