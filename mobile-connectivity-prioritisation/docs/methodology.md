# Methodology

## 1. Data source

The analysis retrieves five public indicators from the World Bank API, with underlying ITU definitions where applicable:

| Analytical field | World Bank indicator | Use in analysis |
|---|---|---|
| Internet usage | `IT.NET.USER.ZS` | Core connectivity/adoption measure |
| Mobile cellular subscriptions | `IT.CEL.SETS.P2` | Contextual mobile-market indicator |
| Population | `SP.POP.TOTL` | Scale / population-impact calculation |
| GDP per capita | `NY.GDP.PCAP.CD` | Economic vulnerability proxy |
| Rural population share | `SP.RUR.TOTL.ZS` | Rural/access context |

The notebook initially requests observations from 2015–2025, then selects the latest non-missing observation for each market and indicator.

## 2. Data quality and comparability

The workflow checks missingness, duplicates and plausible ranges. It retains the observation year for every indicator and calculates a `year_spread` between the earliest and latest observations used for each market.

The repository's refactored pipeline also filters the World Bank country catalogue so regional and income aggregates are not treated as individual markets.

## 3. Portfolio benchmark

The case study uses an **80% Internet usage benchmark**.

`usage_gap_pp = max(80 - internet_usage_pct, 0)`

This is a portfolio assumption for the case study. It is not presented as an official GSMA target or a universal policy benchmark.

## 4. Population-impact scenario

`population_affected_est = population × usage_gap_pp / 100`

This is a scenario estimate representing the population corresponding to the benchmark gap. It is not a deduplicated estimate of people without Internet access.

## 5. Priority-score framework

Each component is converted to a 0–100 percentile score before weighting, avoiding direct addition of incompatible raw units.

| Component | Weight | Direction |
|---|---:|---|
| Usage gap | 35% | Higher gap → higher priority |
| Population impact | 30% | Higher scale → higher priority |
| Rural population share | 15% | Higher rural share → higher priority |
| Economic vulnerability | 20% | Lower GDP per capita → higher priority |

`Priority Score = 0.35×Gap + 0.30×Population Impact + 0.15×Rural + 0.20×Economic Vulnerability`

Priority bands are defined as:

- Lower: score ≤ 33.33
- Medium: 33.33 < score ≤ 66.67
- Higher: score > 66.67

The score is a decision-support mechanism, not an objective measure of social need.

## 6. Data confidence

The confidence category is a governance aid rather than a statistical confidence interval.

- **High** — complete core indicators and observation-year spread ≤ 1 year
- **Medium** — ≥80% completeness and year spread ≤ 3 years
- **Low** — otherwise

## 7. Sensitivity analysis

An alternative weighting scenario tests whether rankings change when population impact receives greater emphasis:

| Component | Base | Alternative |
|---|---:|---:|
| Usage gap | 35% | 25% |
| Population impact | 30% | 40% |
| Rural | 15% | 15% |
| Economic vulnerability | 20% | 20% |

`rank_change` makes weight sensitivity visible to stakeholders.

## 8. Diagnostic segmentation

The diagnostic segment is a screening rule designed to direct further investigation toward rural/access, affordability/economic, usage/adoption or mixed barriers. It is explicitly **not a causal root-cause model**.
