# Model 1 — Logistic Regression

**Related script:** [`src/train_model1_logreg.py`](src/train_model1_logreg.py)

Corresponds to **Part B – Model 1 details**.

## Why Logistic Regression

Logistic Regression is the interpretable **linear baseline** recommended in the
SS1 `experimental_setup/config.yaml` and used as the reference classifier across
the Part A literature (Moro et al., 2014; Dias & Antonio, 2025). Its coefficients
are directly interpretable as log-odds contributions, which matters for a client
who wants to understand *why* an account is flagged as at-risk. It also gives a
well-behaved probability that can be thresholded for targeted interventions.

## Technique & pipeline

```
engineered features
  -> ColumnTransformer (StandardScaler on numerics + OneHot on categoricals, fit on TRAIN only)
    -> LogisticRegression(class_weight="balanced")
```

The whole thing is a single scikit-learn `Pipeline`, so the fitted scaler/encoder
travels with the classifier and evaluation reproduces the exact feature space.

## Hyper-parameters

| Hyper-parameter | Value | Reason |
|-----------------|-------|--------|
| `solver` | `lbfgs` | Efficient for this size; supports L2. |
| `penalty` | L2 (default) | Regularisation to control variance across 77 features. |
| `C` | `1.0` | Default regularisation strength (no evidence of over-fit; train/val AUC are close). |
| `class_weight` | `balanced` | Re-weights the loss inversely to class frequency to counter the ~11% positive rate. |
| `max_iter` | `1000` | Ensures convergence. |
| `random_state` | `42` | Reproducibility. |

## Decision threshold

Rather than the naïve 0.5 cut-off, the operating **threshold is selected on the
validation fold** to maximise F1, and then applied unchanged to the test fold.
Selected threshold: **0.666**.

## How to run

```bash
cd src
python train_model1_logreg.py   # run AFTER feature_engineering.py
```

Outputs: `models/model1_logreg.joblib` and
`experimental_results/model1_val_threshold.json`.

## Validation performance (sanity check)

| Metric | Value (val) |
|--------|-------------|
| ROC-AUC | 0.801 |
| F1 | 0.499 |
| Recall | 0.555 |
| Top-decile lift | 4.43 |

Full held-out **test** results and figures are in
[`Model1Performance.MD`](Model1Performance.MD).
