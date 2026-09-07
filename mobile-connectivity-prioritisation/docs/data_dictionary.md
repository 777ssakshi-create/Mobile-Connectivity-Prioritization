# Data Dictionary

| Field | Definition | Business use |
|---|---|---|
| `countryiso3code` | Three-letter market/country code supplied through the World Bank country catalogue | Stable identifier |
| `country_name` | Human-readable country/territory name | Display / reporting |
| `internet_usage_pct` | Individuals using the Internet (% of population) | Core adoption/connectivity metric |
| `mobile_subscriptions_per_100` | Mobile cellular subscriptions per 100 people | Mobile-market context; not coverage |
| `population` | Total population | Scale and impact calculation |
| `gdp_per_capita` | GDP per capita, current US$ | Economic vulnerability proxy |
| `rural_population_pct` | Rural population (% of total) | Rural/access context |
| `*_year` | Latest observation year used for the corresponding indicator | Freshness / auditability |
| `year_spread` | Difference between the newest and oldest indicator year used for a market | Comparability control |
| `usage_gap_pp` | Positive percentage-point gap to the 80% project benchmark | Severity component |
| `population_affected_est` | Population × positive usage gap / 100 | Scenario scale measure |
| `gap_score` | Percentile-normalised usage-gap score | Priority component |
| `population_impact_score` | Percentile-normalised population-impact score | Priority component |
| `rural_score` | Percentile-normalised rural-share score | Priority component |
| `economic_vulnerability_score` | Inverted percentile score of GDP per capita | Priority component |
| `priority_score` | Weighted composite decision-support score | Ranking |
| `priority_band` | Lower / Medium / Higher | Executive segmentation |
| `data_confidence` | High / Medium / Low governance category | Decision assurance |
| `priority_score_alt` | Alternative-weight scenario score | Sensitivity analysis |
| `rank_base` | Rank under base weights | Sensitivity analysis |
| `rank_alt` | Rank under alternative weights | Sensitivity analysis |
| `rank_change` | Difference between base and alternative rank | Sensitivity flag |
| `diagnostic_segment` | Screening category for the next investigation | BA diagnostic routing |
| `display_rank` | Sequential presentation rank in the cleaned market-only dataset | Dashboard display |
