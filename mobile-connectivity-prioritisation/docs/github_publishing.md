# GitHub Publishing Guide

## Recommended repository name

`mobile-connectivity-prioritisation`

## Recommended GitHub description

> Independent Business Analyst case study using World Bank/ITU data to prioritise connectivity markets with transparent scoring, data confidence, sensitivity analysis, BA artefacts and a stakeholder dashboard.

## Suggested topics

`business-analysis` · `data-analysis` · `python` · `pandas` · `world-bank` · `connectivity` · `decision-support` · `business-intelligence` · `dashboard` · `requirements` · `uat` · `data-quality`

## Publish from your local machine

Create an empty repository on GitHub, then from this project folder run:

```bash
git init
git add .
git commit -m "Initial release: mobile connectivity prioritisation case study"
git branch -M main
git remote add origin <your-repository-url>
git push -u origin main
```

## Before making the repository public

1. Confirm the portfolio disclosure in `README.md` reflects how you want to present the project.
2. Open `dashboard/stakeholder_dashboard.html` locally and verify all charts render.
3. Run the notebook once in your intended environment if you want outputs regenerated from the latest source data.
4. Run `pytest -q` and confirm tests pass.
5. Decide whether you want to add an open-source licence. No licence has been selected automatically in this package.
6. Replace `<your-repository-url>` examples in the README after publishing if desired.

## Suggested pinned-repository positioning

When pinning this project on your GitHub profile, position it as an **end-to-end Business Analysis + Data/BI decision-support case study**, not simply a Python notebook. The strongest differentiator is the chain from data quality and scoring through requirements, process redesign, UAT, traceability and executive communication.
