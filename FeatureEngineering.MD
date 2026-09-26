# Feature Engineering

**Related script:** [`src/feature_engineering.py`](src/feature_engineering.py) (feature definitions and the encoding pipeline live in [`src/pipeline_utils.py`](src/pipeline_utils.py))

This document describes the feature engineering applied before modelling. It
corresponds to **Part B – Feature engineering**.

## How to run

```bash
cd src
python feature_engineering.py   # run AFTER preprocessing.py
```

Outputs: `datasets/processed/{train,val,test}_fe.csv` and
`experimental_results/feature_list.txt`.

## Design principle: no leakage

Every engineered feature is **row-wise** — it depends only on the values within
its own row, never on any cross-row aggregate. This means the transformation can
be applied to the train, validation and test folds independently and is
guaranteed not to leak information between them. The one-hot encoder and scaler
(below) *are* fitted, and they are fitted **on the training fold only**.

## Derived features

| New feature | Definition | Rationale (SS1 analogue) |
|-------------|------------|--------------------------|
| `was_contacted_before` | `1` if `pdays != 999`, else `0` | The `999` sentinel means "never previously contacted". Turning it into an explicit flag lets the model use the signal cleanly. Analogue of SS1 prior-engagement signals. |
| `prev_contact_success` | `1` if `poutcome == "success"` | A prior successful outcome is a strong positive prior — analogue of SS1 onboarding-completion depth. |
| `contacted_and_success` | `was_contacted_before × prev_contact_success` | Interaction term: distinguishes clients with a *successful* prior campaign from those merely contacted before. |
| `age_group` | `age` binned into 18-24 / 25-34 / 35-44 / 45-54 / 55-64 / 65+ | Mirrors the SS1 "Age group" demographic field; captures non-linear age effects for the linear model. |
| `campaign_intensity` | `campaign` (contacts this campaign) binned into 1 / 2 / 3 / 4-5 / 6+ | Analogue of SS1 "Total nudges sent"; over-contacting can depress response. |

In addition, the `pdays` `999` sentinel is replaced with `0` so the raw numeric
column is not distorted (its information is preserved in `was_contacted_before`).

## Encoding & scaling pipeline

Built by `pipeline_utils.build_feature_pipeline()` as a scikit-learn
`ColumnTransformer`:

* **Categorical features** (`job`, `marital`, `education`, `default`, `housing`,
  `loan`, `contact`, `month`, `day_of_week`, `poutcome`, `age_group`,
  `campaign_intensity`) → **one-hot encoding** with `handle_unknown="ignore"`
  (so an unseen category at inference never crashes the pipeline).
* **Numeric features** (`age`, `campaign`, `pdays`, `previous`, the five
  macro-economic indicators, and the three engineered binary/interaction
  features) → **standard-scaled for Logistic Regression** (Model 1) and
  **passed through unscaled for XGBoost** (Model 2), because gradient-boosted
  trees are invariant to monotone transforms.

After one-hot encoding the model input has **77 features** (from the original 20
inputs + 5 engineered features). The complete expanded list is written to
`experimental_results/feature_list.txt`.

## Class imbalance

Imbalance (~11% positive) is **not** resampled at the data level here; instead it
is handled inside each model via cost-sensitive learning
(`class_weight="balanced"` for Logistic Regression, `scale_pos_weight` for
XGBoost). This keeps the feature-engineering stage deterministic and leakage-free.
SMOTE-style oversampling — used by Arifah et al. (2023) on this same dataset — is
noted as an alternative in the recommendations.
