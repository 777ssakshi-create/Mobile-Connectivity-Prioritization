# Known Issues and Provenance Notes

The repository retains the original notebook exports for transparency and also contains a cleaned market-only presentation dataset.

## Original export provenance

The original World Bank API response stores the `country` label as a nested object. In the original notebook, casting this field directly to text can produce labels such as dictionary-like strings in exported CSV files.

The original notebook also assumes aggregate records will be removed by missing ISO3 codes. Some World Bank aggregate records can still enter the analytical population, which affects percentile-based ranking because the comparison set changes.

## Repository treatment

To avoid silently overwriting the original artefacts:

- Original exports are preserved under `data/processed/*_original.csv`.
- The enhanced dashboard uses `connectivity_priority_market_only.csv`, where market labels are normalised and aggregate rows are excluded before percentile-based scores are recalculated.
- `src/connectivity_pipeline.py` implements robust country-name parsing and country-catalogue filtering for future reruns.

## Diagnostic segmentation

The diagnostic rule is a portfolio screening framework, not a causal model. A production version should validate segment thresholds with domain stakeholders and may wish to distinguish zero-gap markets explicitly from positive-gap markets.
