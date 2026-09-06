# Shipsense: Delivery and Revenue Risk Intelligence Platform

**Live dashboard:** https://shipsense-drabkj3r4eatmwwnpryjg4.streamlit.app/

## The Business Question

Which e-commerce orders are at risk of arriving late, and what does that actually cost the business in lost repeat purchases and revenue at risk?

## What This Project Does

An end to end data pipeline built on the Olist Brazilian e-commerce dataset:

Raw order data leads to PostgreSQL, then SQL analytics, then feature engineering, then a LightGBM delay risk model, then a FastAPI serving endpoint, then a live Streamlit dashboard.

In one line: a system that predicts which orders are likely to arrive late, quantifies the revenue impact of that risk, and serves the prediction through a live API and dashboard rather than stopping at a notebook.

## Key Results

- 96,478 delivered orders analyzed across 27 Brazilian states
- Overall late delivery rate: 6.8 percent
- Hypothesis test: customers whose first order arrived late had a repeat purchase rate of 2.52 percent, versus 3.04 percent for customers whose first order arrived on time (two proportion z test, p = 0.0195, 95 percent confidence interval: negative 0.92 percent to negative 0.12 percent). The effect is statistically significant and directionally meaningful, though small in absolute size.
- Model: LightGBM, tuned with Optuna across 50 trials and 5 fold cross validation
- Cross validation ROC-AUC: 0.7624
- Held out test ROC-AUC: 0.7583, a gap of only 0.004 from cross validation, confirming low variance and no data leakage
- Held out test PR-AUC: 0.2246, roughly 3.3 times better than the 6.8 percent random baseline
- Top model drivers by SHAP: purchase month, customer state, and seller historical late rate

## Methodology and Debugging Notes

Two real data issues were found and fixed during this project, both worth calling out since they affected model validity.

**Right censoring bias.** An early version of the model showed test ROC-AUC collapsing to near random, around 0.52, despite a healthy cross validation score. The cause was that orders near the end of the dataset's time range had not had enough time to be marked delivered, which meant the test set's late rate was artificially low. This was fixed by computing a data driven cutoff based on the 99th percentile of observed delivery durations, and excluding orders too close to the end of the dataset for a fair evaluation.

**Overfitting caught with a learning curve.** An unconstrained hyperparameter search produced a model with a 0.09 gap between training and validation ROC-AUC, a clear overfitting signal. Constraining the search space toward simpler trees and stronger L1 and L2 regularization closed this gap to 0.004, at a cost of only 0.005 test AUC, a worthwhile trade for a trustworthy and generalizable model.

## Repository Structure

- `sql/` hand written SQL analytics, including window functions and CTEs
- `notebooks/` EDA, hypothesis testing, and modeling notebooks
- `api/` FastAPI serving layer and pytest tests
- `dashboard/` Streamlit dashboard app, deployed live
- `models/` versioned model metadata and category mappings
- `images/` final and in progress charts referenced in this README
- `data_quality_notes.md` notes from the Phase 1 data quality audit
- `MONITORING.md` production monitoring and retraining plan

## Tech Stack

PostgreSQL, Python (Pandas, NumPy, scikit-learn, LightGBM, SHAP, Optuna, statsmodels), FastAPI, Streamlit, Plotly, Git

## Running This Locally

1. Load the Olist dataset into PostgreSQL, see the `sql/` folder and `notebooks/01_eda_feature_engineering.ipynb` for the load script
2. Run the notebooks in order: EDA and feature engineering, hypothesis testing, modeling
3. Start the API: `cd api && uvicorn main:app --reload`
4. Start the dashboard: `cd dashboard && streamlit run app.py`

## What I Would Do With More Time

Add live carrier and weather signals to push model performance past its current ceiling, deploy the FastAPI service publicly alongside the dashboard, and automate the drift monitoring plan described in `MONITORING.md`.
