# Mobile Connectivity Prioritisation

### Independent Business Analyst portfolio case study using public World Bank / ITU indicators

This project builds a reproducible decision-support framework for identifying markets that may warrant deeper connectivity investigation. It combines public data engineering, quality controls, exploratory analysis, transparent prioritisation logic, sensitivity analysis, Business Analysis artefacts and a stakeholder-facing dashboard.

> **Portfolio disclosure:** This is an independent case study. Public data are real. The 80% benchmark, priority-score weights, diagnostic rules, requirements, user stories, As-Is/To-Be process and UAT artefacts are project assumptions/proposals for demonstration. They are not presented as an official GSMA scoring model, internal workflow or universal target.

---

## Business problem

Connectivity decisions can become inconsistent when analysts rely on different sources, assumptions and manual country comparisons. A low Internet-usage percentage alone also does not tell decision-makers whether a gap is large in absolute population terms, whether the evidence is current, or whether the ranking is robust to alternative priorities.

The case study therefore asks:

**How can public connectivity indicators be translated into a transparent, auditable and stakeholder-friendly market prioritisation process?**

## What the solution does

1. Retrieves recent World Bank / ITU indicators through the World Bank API.
2. Audits missingness, duplicates, ranges and observation-year comparability.
3. Selects the latest available observation for each market and indicator.
4. Calculates the positive gap to an explicit 80% portfolio benchmark.
5. Estimates the population represented by that benchmark gap.
6. Creates a percentile-normalised weighted Priority Score.
7. Adds a High / Medium / Low data-confidence category.
8. Runs an alternative-weight sensitivity scenario.
9. Assigns a screening-level diagnostic / next-investigation category.
10. Translates the analysis into BA requirements, user stories, process redesign, UAT and traceability artefacts.
11. Presents the results in an executive stakeholder dashboard.

## Current stakeholder dataset

The enhanced presentation dataset contains **204 country/territory markets** after excluding regional and income aggregates from the market-ranking population.

- **65** markets fall in the proposed Higher-priority band.
- **143 / 204 (~70%)** are classified High confidence under the case-study freshness rule.
- The sum of positive benchmark-gap population scenarios is approximately **1.05 billion**. This is *not* a count of unique offline people.

These figures are derived from the included cleaned dataset and will change when the public source data are refreshed or assumptions change.

---

## Priority framework

All components are converted to percentile scores before weighting.

| Component | Weight | Interpretation |
|---|---:|---|
| Usage gap | 35% | Larger gap to the 80% benchmark increases priority |
| Population impact | 30% | Larger population represented by the gap increases priority |
| Rural context | 15% | Higher rural share increases the contextual priority signal |
| Economic vulnerability | 20% | Lower GDP per capita increases the vulnerability score |

**Priority Score**

`0.35 × Gap Score + 0.30 × Population Impact Score + 0.15 × Rural Score + 0.20 × Economic Vulnerability Score`

The alternative sensitivity scenario changes the first two weights to **25% gap / 40% population impact** while keeping rural and economic weights unchanged.

See [`docs/methodology.md`](docs/methodology.md) for the full method.

---

## Dashboard

The primary portfolio dashboard is:

[`dashboard/stakeholder_dashboard.html`](dashboard/stakeholder_dashboard.html)

Open it locally in a browser. Plotly is loaded from a CDN, so the interactive charts require an internet connection.

The dashboard is organised around executive questions rather than chart types:

- Where are the highest-priority markets?
- How severe and how large is the gap?
- How confident are we in the evidence?
- Is the ranking sensitive to different stakeholder weights?
- What should analysts investigate next?

The earlier prototype is retained as [`dashboard/legacy_dashboard_preview.html`](dashboard/legacy_dashboard_preview.html) to show the design evolution.

For the recommended production Power BI structure, see [`docs/dashboard_design.md`](docs/dashboard_design.md).

---

## Repository structure

```text
mobile-connectivity-prioritisation/
├── README.md
├── CHANGELOG.md
├── KNOWN_ISSUES.md
├── requirements.txt
├── requirements-dev.txt
├── notebooks/
│   └── mobile_connectivity_prioritisation_analysis.ipynb
├── src/
│   └── connectivity_pipeline.py
├── tests/
│   └── test_scoring.py
├── dashboard/
│   ├── stakeholder_dashboard.html
│   ├── legacy_dashboard_preview.html
│   └── README.md
├── data/
│   ├── README.md
│   ├── raw/
│   │   └── .gitkeep
│   └── processed/
│       ├── connectivity_priority_market_only.csv
│       ├── connectivity_priority_dataset_original.csv
│       └── stakeholder_priority_table_original.csv
├── docs/
│   ├── methodology.md
│   ├── assumptions_and_limitations.md
│   ├── business_analysis.md
│   ├── dashboard_design.md
│   ├── data_dictionary.md
│   └── ba_artifacts/
│       ├── requirements.csv
│       ├── user_stories.csv
│       ├── uat_test_cases.csv
│       ├── requirements_traceability_matrix.csv
│       ├── as_is_to_be_process.csv
│       └── data_dictionary.csv
└── .github/
    └── workflows/
        └── python-tests.yml
```

---

## Quick start

### Option A — Run the narrative notebook

```bash
git clone <your-repository-url>
cd mobile-connectivity-prioritisation
python -m venv .venv
```

Activate the environment, then install dependencies:

```bash
pip install -r requirements.txt
jupyter notebook notebooks/mobile_connectivity_prioritisation_analysis.ipynb
```

The notebook retrieves public data from the World Bank API at runtime.

### Option B — Run the refactored pipeline

```bash
python -m src.connectivity_pipeline
```

This refreshes the market-only processed dataset under `data/processed/`.

### Run tests

```bash
pip install -r requirements-dev.txt
pytest -q
```

---

## Data sources

The project uses the following World Bank indicator codes:

- `IT.NET.USER.ZS` — Individuals using the Internet (% of population)
- `IT.CEL.SETS.P2` — Mobile cellular subscriptions (per 100 people)
- `SP.POP.TOTL` — Population, total
- `NY.GDP.PCAP.CD` — GDP per capita (current US$)
- `SP.RUR.TOTL.ZS` — Rural population (% of total population)

The retrieval window in the notebook is **2015–2025**, after which the latest available non-missing observation is selected for each indicator/market.

---

## Business Analysis deliverables

This repository intentionally includes the delivery/governance side of the case study, not only Python analysis:

- Business and functional requirements
- User stories and acceptance criteria
- Hypothetical As-Is process
- Proposed To-Be process
- UAT test cases
- Requirements Traceability Matrix
- Data dictionary
- Stakeholder priority table
- Decision-support dashboard

See [`docs/business_analysis.md`](docs/business_analysis.md).

---

## Key analytical safeguards

- Observation years are retained instead of implying every market has the same-year data.
- Mobile subscriptions are not labelled as network coverage.
- The population-impact metric is explicitly described as a scenario estimate.
- Every score component is normalised before weighting.
- Confidence and sensitivity are surfaced alongside priority.
- Regional/income aggregates are excluded from the enhanced market-ranking population.
- Assumptions are documented rather than hidden in code.

See [`docs/assumptions_and_limitations.md`](docs/assumptions_and_limitations.md) and [`KNOWN_ISSUES.md`](KNOWN_ISSUES.md).

---

## Skills demonstrated

**Business Analysis** — problem framing, requirements, user stories, acceptance criteria, As-Is/To-Be process, UAT, RTM, decision governance.

**Data Analysis** — API ingestion, pandas, quality checks, descriptive statistics, correlation analysis, percentile normalisation, composite scoring, sensitivity analysis.

**BI / Stakeholder Communication** — KPI design, executive prioritisation, data-confidence communication, interactive filtering, management-focused dashboard design.

**Engineering / Reproducibility** — modular Python pipeline, environment requirements, provenance-preserving outputs, automated tests and GitHub Actions workflow.

---

## Future enhancements

- Build the full three-page Power BI implementation described in `docs/dashboard_design.md`.
- Add time-series trend views instead of relying only on latest observations.
- Add more direct infrastructure/coverage indicators where an appropriate public source is available.
- Validate benchmark, weights, band thresholds and diagnostic rules with real domain stakeholders.
- Add outcome tracking so prioritisation can be compared with intervention results over time.
- Formalise data refresh metadata, source timestamps and release versioning.

---

## Disclaimer

This repository is for portfolio and educational demonstration. The prioritisation model should not be used as a substitute for stakeholder validation, domain-specific due diligence or operational programme decisions.
