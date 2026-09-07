# Data

This project uses public World Bank / ITU indicators retrieved through the World Bank API.

## Folders

- `raw/` — intentionally empty in Git. The notebook/pipeline retrieves source data directly from the API for reproducibility and auditability.
- `processed/connectivity_priority_dataset_original.csv` — original notebook export, retained for provenance.
- `processed/stakeholder_priority_table_original.csv` — original stakeholder table export.
- `processed/connectivity_priority_market_only.csv` — cleaned market-only dataset used by the enhanced stakeholder dashboard. It removes regional/income aggregates and normalises country labels before recalculating percentile-based scores.

## Important data interpretation

`population_affected_est` is a scenario estimate calculated as population multiplied by the positive gap to the 80% portfolio benchmark. It is **not** a count of unique offline people.

Mobile cellular subscriptions per 100 people are used only as contextual information. They are **not** labelled as network coverage.
