# Model 2 Performance — XGBoost

**Related script:** [`src/evaluate_model2.py`](src/evaluate_model2.py)

Corresponds to **Part C – Performance of Model 2**. All numbers below are on the
**held-out test split** (6,179 accounts).

## How to run

```bash
cd src
python evaluate_model2.py   # run AFTER train_model2_xgboost.py
```

Outputs: `experimental_results/model2_test_metrics.json`,
`experimental_results/model2_feature_importance.csv`, and figures
`experimental_results/figures/model2_{roc,pr,confusion,gains}.png`.

## Headline metrics (test set)

| Metric | Value |
|--------|-------|
| Accuracy | 0.878 |
| Precision | 0.468 |
| Recall | 0.595 |
| F1 | 0.524 |
| **ROC-AUC** | **0.812** |
| PR-AUC (average precision) | 0.485 |
| Top-decile lift | **4.58×** |
| ROC-AUC 95% CI (bootstrap, 1,000 resamples) | **[0.793, 0.832]** |

Decision threshold = 0.656 (selected on validation).

## Confusion matrix (test)

|  | Predicted No | Predicted Yes |
|--|--------------|---------------|
| **Actual No**  | TN = 5,012 | FP = 471 |
| **Actual Yes** | FN = 282 | TP = 414 |

## Top predictive features (by XGBoost gain)

| Rank | Feature | Gain |
|------|---------|------|
| 1 | `nr.employed` (macro: employment level) | 0.344 |
| 2 | `emp.var.rate` (macro: employment variation) | 0.076 |
| 3 | `cons.conf.idx` (macro: consumer confidence) | 0.037 |
| 4 | `was_contacted_before` *(engineered)* | 0.036 |
| 5 | `month_oct` | 0.029 |
| 6 | `contacted_and_success` *(engineered)* | 0.022 |
| 7 | `prev_contact_success` *(engineered)* | 0.018 |
| 8 | `pdays` | 0.017 |
| 9 | `euribor3m` (macro: interest rate) | 0.017 |
| 10 | `age_group_35-44` *(engineered)* | 0.016 |

Full ranking in `experimental_results/model2_feature_importance.csv`.

## Statistical measures & interpretation

* **ROC-AUC = 0.812** clears the **SS1 ≥ 0.75 criterion**; the bootstrap 95% CI
  **[0.793, 0.832]** is entirely above the threshold.
* **Top-decile lift = 4.58×** clears the **SS1 ≥ 2× criterion**.
* XGBoost improves on Model 1 across **every** metric (accuracy, precision,
  recall, F1, ROC-AUC, PR-AUC, lift). Whether that gap is statistically
  meaningful is tested in [`Comparison.MD`](Comparison.MD).
* **Three of the top-ten features are engineered** (`was_contacted_before`,
  `contacted_and_success`, `prev_contact_success`), which validates the
  feature-engineering stage. The dominance of macro-economic indicators
  (`nr.employed`, `emp.var.rate`, `euribor3m`) is consistent with Moro et al.
  (2014), who added these social/economic context variables precisely because
  they lift predictive power.

## Figures

* `figures/model2_roc.png`, `figures/model2_pr.png`,
  `figures/model2_confusion.png`, `figures/model2_gains.png`.
