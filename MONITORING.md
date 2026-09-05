# Monitoring & Retraining Plan

**Data drift**: Track weekly the distribution of `ship_distance_km`, 
`seller_hist_late_rate`, and `purchase_month` against training-time 
distributions (e.g., via population stability index). A shift beyond 
0.2 PSI on any top-3 SHAP feature triggers a review.

**Performance drift**: Once ground truth (actual delivery outcome) is 
available for served predictions, recompute ROC-AUC weekly on a rolling 
30-day window. A drop below 0.70 (vs. baseline 0.7583) triggers retraining.

**Retraining trigger**: Retrain monthly on a rolling 12-month window, or 
immediately if performance drift is detected. Category mappings must be 
regenerated each retrain since seller/state sets can grow.
