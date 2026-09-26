# Preprocessing

**Related script:** [`src/preprocessing.py`](src/preprocessing.py) (shared helpers in [`src/pipeline_utils.py`](src/pipeline_utils.py))

This document describes how the raw public dataset is turned into clean, split
data ready for feature engineering and modelling. It corresponds to **Part B –
Data preprocessing techniques**.

## Dataset

We prove the viability of the SS1 account-activation approach on the **UCI Bank
Marketing dataset** (`bank-additional-full.csv`, Moro, Cortez & Rita, 2014). The
task is a direct public analogue of the SS1 problem: a **binary classification**
predicting whether a bank client will make a **term-deposit** (`y = yes/no`)
after a marketing campaign, using demographic, campaign-engagement and
macro-economic features, with strong class imbalance. "Subscribing a deposit"
here plays the role of "making a first deposit / activating" in SS1.

* Instances: **41,188**
* Input columns: **20** (+ 1 target `y`)
* Positive rate (`y = yes`): **11.27%** (class imbalance)

The raw file lives at `datasets/raw/bank-additional-full.csv` and is
semicolon-delimited.

## How to run

```bash
pip install -r experimental_setup/requirements.txt
cd src
python preprocessing.py
```

Outputs written to `datasets/processed/`: `train.csv`, `val.csv`, `test.csv`
(and `experimental_results/class_balance.csv`).

## Preprocessing steps

1. **Load** the semicolon-delimited CSV.
2. **Target encoding** – map `y` from `yes/no` to `1/0`.
3. **Leakage removal** – drop the `duration` column. `duration` (length of the
   contact call) is only known *after* a contact has happened, so using it would
   leak the outcome. This mirrors the SS1 rule that only signals available
   *within the activation window* may be used, and is the standard treatment of
   this dataset in the literature (Moro et al., 2014).
4. **Missingness handling** – categorical "missing" values are recorded as the
   token `unknown` in the source data. Rather than dropping or blindly imputing
   them, we **keep `unknown` as an explicit category**. Whether a client withheld
   information can itself be predictive, and this avoids discarding rows. There
   are **no** literal `NaN` values in the dataset.
5. **Split** – a **stratified 70 / 15 / 15** train / validation / test split that
   preserves the ~11.3% positive prevalence in every fold. All encoders and
   scalers are fit on the **training fold only** (done downstream in feature
   engineering and the model pipelines) to prevent information leaking from
   validation/test into training.

| Split | Rows | Positive rate |
|-------|------|---------------|
| train | 28,831 | 11.27% |
| val   | 6,178  | 11.27% |
| test  | 6,179  | 11.26% |

## Note on non-stationarity (a documented SS1 risk)

The CSV is ordered by contact date (May 2008 → Nov 2010). We initially tried a
**chronological** split, which revealed very strong non-stationarity: the
subscription rate rises from ~5% in the earliest period to ~38% in the latest,
driven by the collapse of the euribor rate over the 2008–2010 crisis. This is
exactly the *"relationship between features and activation may not be stationary
across time periods"* risk logged in SS1. Because such a large distribution
shift makes a clean viability comparison hard to read — and because the Part A
reference papers evaluate on stratified splits — we use a stratified split here
and **flag time-aware (rolling-origin) validation as required future work** once
STADIOEquities' real data is available.
