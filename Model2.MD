# Model 2 — XGBoost

**Related script:** [`src/train_model2_xgboost.py`](src/train_model2_xgboost.py)

Corresponds to **Part B – Model 2 details**.

## Why XGBoost

XGBoost (extreme gradient-boosted decision trees) is the strongest performer
reported across the Part A literature: Dias & Antonio (2025) find XGBoost their
best churn model, and Arifah et al. (2023) apply XGBoost to **this exact Bank
Marketing dataset**. It captures non-linear interactions between behavioural,
demographic and macro-economic features that a linear model cannot, at the cost
of interpretability. It is the natural "powerful ensemble" counterpart to the
Logistic Regression baseline, and both were shortlisted in the SS1 config.

## Technique & pipeline

```
engineered features
  -> ColumnTransformer (passthrough numerics + OneHot on categoricals, fit on TRAIN only)
    -> XGBClassifier(scale_pos_weight = n_neg / n_pos), early stopping on validation
```

Numerics are **not** scaled (trees are scale-invariant). The fitted transformer
is saved *with* the classifier as a bundle so evaluation reproduces the feature
space exactly.

## Hyper-parameters

| Hyper-parameter | Value | Reason |
|-----------------|-------|--------|
| `n_estimators` | `400` (early-stopped) | Upper bound; early stopping picks the real count. |
| `early_stopping_rounds` | `30` (on validation AUC) | Stops when val AUC stops improving → guards over-fitting. Best iteration: **80**. |
| `max_depth` | `5` | Moderate depth to model interactions without over-fitting. |
| `learning_rate` | `0.05` | Small step size for stable convergence with many trees. |
| `subsample` | `0.9` | Row subsampling for regularisation. |
| `colsample_bytree` | `0.9` | Column subsampling for regularisation. |
| `min_child_weight` | `2` | Discourages tiny, noisy leaves. |
| `reg_lambda` | `1.0` | L2 regularisation on leaf weights. |
| `scale_pos_weight` | `7.88` (= n_neg / n_pos) | XGBoost-native handling of the ~11% class imbalance. |
| `eval_metric` | `auc` | Aligns training objective with the SS1 primary metric. |
| `tree_method` | `hist` | Fast histogram-based training. |
| `random_state` | `42` | Reproducibility. |

## Decision threshold

Selected on the validation fold to maximise F1, then applied unchanged to test.
Selected threshold: **0.656**.

## How to run

```bash
cd src
python train_model2_xgboost.py   # run AFTER feature_engineering.py
```

Outputs: `models/model2_xgboost.joblib` and
`experimental_results/model2_val_threshold.json`.

## Validation performance (sanity check)

| Metric | Value (val) |
|--------|-------------|
| ROC-AUC | 0.817 |
| F1 | 0.516 |
| Recall | 0.573 |
| Top-decile lift | 4.62 |

Full held-out **test** results, feature importances and figures are in
[`Model2Performance.MD`](Model2Performance.MD).
