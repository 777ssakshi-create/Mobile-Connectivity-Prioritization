# Business Analysis Artefacts

The project deliberately goes beyond exploratory analysis. It demonstrates how evidence can be translated into a controlled decision process.

## Requirements

The proposed requirements cover consistent market prioritisation, population-impact visibility, contextual indicators, rank/filter functionality, source-year visibility, data-confidence display and documented calculation rules.

Source: `ba_artifacts/requirements.csv`.

## User stories

The user stories represent programme-analyst and programme-manager needs, including priority ranking, scale interpretation, data freshness/confidence and diagnostic context.

Source: `ba_artifacts/user_stories.csv`.

## As-Is → To-Be process

**Hypothetical As-Is:** request-driven analysis, manual source searching, manual country comparison and inconsistent assumptions.

**Proposed To-Be:** controlled refresh, automated QA, standard scoring, analyst validation, stakeholder review, prioritisation decision and outcome tracking.

Source: `ba_artifacts/as_is_to_be_process.csv`.

## UAT and traceability

The UAT artefacts test ranking, indicator-year visibility, data-confidence visibility, population-impact calculations and methodology documentation. The requirements traceability matrix links requirements to user stories and UAT coverage.

Sources:

- `ba_artifacts/uat_test_cases.csv`
- `ba_artifacts/requirements_traceability_matrix.csv`

## Why this matters

For a BA portfolio, the value is not only the score. The stronger story is the end-to-end chain:

**Business problem → evidence → data-quality controls → prioritisation logic → requirements → process redesign → dashboard → UAT → governance**
