# Model Comparison — Logistic Regression vs XGBoost

**Related script:** [`src/compare_models.py`](src/compare_models.py)

Corresponds to **Part C – Comparison of Model 1 and Model 2**.

## How to run

```bash
cd src
python compare_models.py   # run AFTER both models are trained
```

Outputs: `experimental_results/comparison_metrics.json`,
`experimental_results/comparison_table.csv`, and figures
`experimental_results/figures/comparison_{roc,pr,gains}.png`.

## Head-to-head on the test set

| Metric | Logistic Regression | XGBoost | Winner |
|--------|--------------------:|--------:|--------|
| Accuracy | 0.873 | **0.878** | XGBoost |
| Precision | 0.451 | **0.468** | XGBoost |
| Recall | 0.575 | **0.595** | XGBoost |
| F1 | 0.505 | **0.524** | XGBoost |
| ROC-AUC | 0.800 | **0.812** | XGBoost |
| PR-AUC | 0.461 | **0.485** | XGBoost |
| Top-decile lift | 4.49× | **4.58×** | XGBoost |

XGBoost wins on every headline metric. The question is whether the margin is
**statistically significant** or within noise — tested three ways below.

## Statistical significance tests

**1. McNemar's test** on paired test-set predictions (do the models make
*different* errors?):
* Discordant pairs: b = 46 (LR right / XGB wrong), c = 76 (LR wrong / XGB right).
* χ² = 6.893, **p = 0.0087** → **significant** at α = 0.05. XGBoost corrects
  substantially more of LR's mistakes than vice-versa.

**2. Bootstrap 95% CI for the AUC difference** (XGB − LR, 1,000 resamples of the
test set):
* Mean difference = **+0.0122**, 95% CI **[+0.0041, +0.0198]**.
* The interval **excludes zero** → XGBoost's AUC advantage on this test set is
  statistically significant.

**3. Stratified 5-fold cross-validation on the training data + paired t-test**
(the procedure sketched in the SS1 `model_comparison.py`):
* CV ROC-AUC — Logistic Regression: **0.788 ± 0.010**
* CV ROC-AUC — XGBoost: **0.792 ± 0.014**
* Paired t-test across folds: t = 1.525, **p = 0.202** → **not significant**.

## Interpretation (insight)

The three tests tell a **consistent but nuanced** story. XGBoost is uniformly
ahead and its advantage is significant on the held-out test set (McNemar and the
bootstrap AUC CI both agree). However, across cross-validation folds the gap is
small (≈ 0.005 AUC) and **not** significant, i.e. the size of the improvement is
modest and somewhat sample-dependent.

**Conclusion:** XGBoost is the better model and is the recommended choice, but the
margin over a well-tuned Logistic Regression is small. For a first production
release where transparency and easy governance matter, Logistic Regression
remains a defensible, near-equivalent option. This trade-off — a real but modest
ensemble advantage — is discussed further in the Part D recommendations report.
