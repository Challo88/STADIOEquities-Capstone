# Model 1 Performance — Logistic Regression

**Related script:** [`src/evaluate_model1.py`](src/evaluate_model1.py)

Corresponds to **Part C – Performance of Model 1**. All numbers below are on the
**held-out test split** (6,179 accounts, never seen during training or threshold
selection).

## How to run

```bash
cd src
python evaluate_model1.py   # run AFTER train_model1_logreg.py
```

Outputs: `experimental_results/model1_test_metrics.json` and figures
`experimental_results/figures/model1_{roc,pr,confusion,gains}.png`.

## Headline metrics (test set)

| Metric | Value |
|--------|-------|
| Accuracy | 0.873 |
| Precision | 0.451 |
| Recall | 0.575 |
| F1 | 0.505 |
| **ROC-AUC** | **0.800** |
| PR-AUC (average precision) | 0.461 |
| Top-decile lift | **4.49×** |
| ROC-AUC 95% CI (bootstrap, 1,000 resamples) | **[0.779, 0.822]** |

Decision threshold = 0.666 (selected on validation).

## Confusion matrix (test)

|  | Predicted No | Predicted Yes |
|--|--------------|---------------|
| **Actual No**  | TN = 4,996 | FP = 487 |
| **Actual Yes** | FN = 296 | TP = 400 |

## Statistical measures & interpretation

* **ROC-AUC = 0.800** comfortably clears the **SS1 success criterion of ≥ 0.75**.
  The bootstrap 95% CI **[0.779, 0.822]** lies entirely above 0.75, so the model's
  ranking ability is significantly better than the threshold, not a lucky sample.
* **Top-decile lift = 4.49×** far exceeds the **SS1 criterion of ≥ 2×**: targeting
  the top 10% of ranked accounts finds ~4.5× more activators than random outreach.
* Because the classes are imbalanced, **accuracy (0.873) is a weak signal** — a
  model that predicted "No" for everyone would score ~0.887. **PR-AUC (0.461)**
  against a 0.113 base rate, and the recall/precision balance, are the honest
  measures, and both show the model finds a meaningful share of activators.
* At the chosen threshold the model recovers **57.5% of true subscribers** while
  keeping most non-subscribers correctly classified — a sensible operating point
  for a "who needs an intervention" use case where missing an activator is costly.

## Figures

* `figures/model1_roc.png` — ROC curve
* `figures/model1_pr.png` — Precision-Recall curve
* `figures/model1_confusion.png` — confusion matrix
* `figures/model1_gains.png` — cumulative gains
