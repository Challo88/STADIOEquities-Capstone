# SS3 Part B — Applying the Final Method to Client Data

**Module:** CAP182 Capstone · **Student:** Allen Charlton · **Student number:** `[ADD STUDENT NUMBER]`
**Project:** StadioEquities — predicting 30-day account activation

This folder applies the **final method selected in SS2 — XGBoost (gradient-boosted trees)** — to the full
client data extract supplied by StadioEquities, as required for SS3 Part B.

## What is here

```
SS3_PartB.ipynb        # the graded notebook (run top-to-bottom; outputs are saved)
data/                  # the client data extract (5 CSV tables) + client README
outputs/               # model + metrics saved by the notebook (created on run)
requirements.txt       # Python dependencies
README.md              # this file
```

## The notebook and where each graded component is

Open `SS3_PartB.ipynb`. Each required component has its own clearly-labelled header:

| # | Component | Header in the notebook |
|---|-----------|------------------------|
| 1 | Dataset loading | `## Component 1 — Dataset loading` |
| 2 | Dataset preprocessing (incl. train/validation/test split) | `## Component 2 — Dataset preprocessing` |
| 3 | Model training (justified hyper-parameters) | `## Component 3 — Model training` |
| 4 | Model validation (metrics on unseen data) | `## Component 4 — Model validation` |
| 5 | Results visualisation | `## Component 5 — Results visualisation` |

## The data

Five tables, all joined on `account_id` (see `data/CLIENT_DATA_README.md` for the client's own dictionary):

| File | Grain | Key content |
|---|---|---|
| `01_account_registration.csv` | account | registration, KYC, **target `activated_30day_flag`** |
| `02_behavioural_events.csv` | event | app/web sessions + account-level behavioural aggregates |
| `03_client_demographics.csv` | account | age, province, employment, investor profile |
| `04_marketing_engagement.csv` | event | emails/push/nudges sent + open/click engagement |
| `05_product_subscription.csv` | account | premium offer / value-added product interaction |

- **1,877 accounts** after de-duplication · **binary** target · **≈ 44% positive** (mild imbalance ≈ 1.27 : 1).

## Method and headline result

XGBoost, trained exactly as in SS2 (stratified 70/15/15 split, `scale_pos_weight` for imbalance, early
stopping on validation AUC, `random_state=42`). On the **held-out test set**:

| Metric | Test (unseen) |
|---|---|
| ROC-AUC | **0.965** |
| PR-AUC | 0.943 |
| F1 | 0.913 |
| Recall | 0.968 |
| Precision | 0.863 |
| Accuracy | 0.918 |
| Top-decile lift | 2.19× |
| 5-fold CV ROC-AUC | 0.968 ± 0.002 |

This clears the SS1 success criteria (ROC-AUC ≥ 0.75, top-decile lift ≥ 2×) and reproduces the SS2 finding on
the client's own data. The dominant, **actionable** drivers are KYC completion and deposit-funnel engagement.

## How to run

```bash
pip install -r requirements.txt
jupyter notebook SS3_PartB.ipynb     # then Run All
# or headless:
jupyter nbconvert --to notebook --execute --inplace SS3_PartB.ipynb
```

The notebook writes the fitted model (`outputs/xgboost_activation_model.json`) and all metrics
(`outputs/metrics.json`) for later analysis.

## Video presentation (Part C)

> **Add your video link here:** `[LINK TO 10–12 MIN VIDEO PRESENTATION]`
