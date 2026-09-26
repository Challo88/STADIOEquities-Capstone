# STADIOEquities Capstone Project

**Module:** CAP182 — Capstone (School of Information Technology)
**Client:** STADIOEquities (Retail Investing & Fintech)
**Project Title:** Predicting Account Activation to Reduce the Registration-to-Deposit Funnel Leakage
**Repository:** https://github.com/Challo88/STADIOEquities-Capstone

This repository contains both submissions:

* **SS1** — Motivation, problem statement, data request and RAAIDD log (below).
* **SS2** — A viability proof of the SS1 approach on a **public** dataset, with
  full modelling code, results and recommendations
  ([jump to SS2](#ss2--viability-proof-on-a-public-dataset)).

---

# SS2 — Viability Proof on a Public Dataset

The client was not yet ready to release sensitive internal data, so SS2 proves
the SS1 modelling approach on a publicly available analogue: the **UCI Bank
Marketing dataset** (Moro, Cortez & Rita, 2014). Predicting whether a bank client
**subscribes a term deposit** after a campaign is a direct public stand-in for
predicting whether a STADIOEquities account **makes its first deposit
(activates)** — both are imbalanced binary-classification problems driven by
demographic, engagement and campaign features.

## Deliverables & document map

| Part | Deliverable | Link |
|------|-------------|------|
| A | Related work & dataset description (4 tables) | [`literature_review/Part_A_Related_Work_and_Data.docx`](literature_review/Part_A_Related_Work_and_Data.docx) · [PDF](literature_review/Part_A_Related_Work_and_Data.pdf) |
| B | Preprocessing | [`Preprocessing.MD`](Preprocessing.MD) → [`src/preprocessing.py`](src/preprocessing.py) |
| B | Feature engineering | [`FeatureEngineering.MD`](FeatureEngineering.MD) → [`src/feature_engineering.py`](src/feature_engineering.py) |
| B | Model 1 (Logistic Regression) | [`Model1.MD`](Model1.MD) → [`src/train_model1_logreg.py`](src/train_model1_logreg.py) |
| B | Model 2 (XGBoost) | [`Model2.MD`](Model2.MD) → [`src/train_model2_xgboost.py`](src/train_model2_xgboost.py) |
| C | Model 1 performance | [`Model1Performance.MD`](Model1Performance.MD) → [`src/evaluate_model1.py`](src/evaluate_model1.py) |
| C | Model 2 performance | [`Model2Performance.MD`](Model2Performance.MD) → [`src/evaluate_model2.py`](src/evaluate_model2.py) |
| C | Model comparison | [`Comparison.MD`](Comparison.MD) → [`src/compare_models.py`](src/compare_models.py) |
| D | Recommendations report (~900 words) | [`reports/Part_D_Recommendations.docx`](reports/Part_D_Recommendations.docx) · [PDF](reports/Part_D_Recommendations.pdf) |

## Public dataset

* **Name:** UCI Bank Marketing (`bank-additional-full.csv`)
* **Instances:** 41,188 · **Input features:** 20 (+1 target) · **Classes:** 2
* **Positive rate:** 11.27% (class imbalance)
* **Source:** UCI Machine Learning Repository, dataset 222 — https://archive.ics.uci.edu/dataset/222/bank+marketing
* Place the CSV at `datasets/raw/bank-additional-full.csv` (already included).

## How to reproduce

```bash
pip install -r experimental_setup/requirements.txt
cd src
python preprocessing.py            # 1. clean + stratified 70/15/15 split
python feature_engineering.py      # 2. derive features + encode
python train_model1_logreg.py      # 3. train Model 1
python train_model2_xgboost.py     # 4. train Model 2
python evaluate_model1.py          # 5. Model 1 test performance
python evaluate_model2.py          # 6. Model 2 test performance
python compare_models.py           # 7. head-to-head + statistical tests
```

To regenerate the reports:
* Word: `node reports/build_part_a_docx.js` and `node reports/build_part_d_docx.js`
* PDF: `python reports/build_part_a_pdf.py` and `python reports/build_part_d_pdf.py`

## Headline results (held-out test set, 6,179 accounts)

| Metric | Logistic Regression | XGBoost |
|--------|--------------------:|--------:|
| ROC-AUC | 0.800 | **0.812** |
| PR-AUC | 0.461 | **0.485** |
| F1 | 0.505 | **0.524** |
| Recall | 0.575 | **0.595** |
| Top-decile lift | 4.49× | **4.58×** |

Both models clear the SS1 success criteria (ROC-AUC ≥ 0.75 and top-decile
lift ≥ 2×). XGBoost is significantly better on the test set (McNemar p = 0.009;
bootstrap AUC-difference 95% CI [+0.004, +0.020]), though the margin is modest and
not significant under 5-fold cross-validation (paired t-test p = 0.20). See
[`Comparison.MD`](Comparison.MD).

---

# SS1 — Motivation, Problem Statement & Data Request

## Part A — Motivation

STADIOEquities has achieved remarkable growth in customer acquisition, with 2.3 million registered accounts and revenue up 22% year-on-year. However, this growth masks a critical inefficiency that is eroding the return on every marketing rand spent: **41% of registered accounts never deposit funds**, and the sign-up-to-first-deposit conversion rate has declined from 64% to 59% over the past two years. With a customer acquisition cost of R180 per account, each account that registers but never activates represents a direct loss. Scaling this across the full registration base, STADIOEquities is spending millions acquiring accounts that generate zero revenue.

The root cause is not a lack of data — it is a lack of insight. STADIOEquities currently sends onboarding emails and nudges on a fixed schedule to every new registrant, regardless of whether they are about to activate or about to disappear. The company already observes that drop-off clusters by acquisition channel, onboarding completion depth, first-session behaviour, and time-to-first-deposit. Yet no model exists to exploit these signals and act on them.

This project will build a supervised machine learning classification model that predicts, for each newly registered account, the probability that the account will make its first deposit within a defined activation window. By identifying accounts that are likely to stall, STADIOEquities can re-target its onboarding interventions — sending more intensive nudges to high-risk accounts and reducing unnecessary outreach to those who are likely to activate naturally. This directly supports two of the company's 2030 strategic priorities:

1. **"Activate the accounts we already have"** — Convert far more registrations into funded, trading clients by spotting who is likely to activate or stall and intervening at the right moment.
2. **"Understand every client's investing style"** — Group clients by how they actually behave so content, nudges, and product suggestions finally fit the person receiving them.

Beyond the immediate activation benefit, the same modelling framework can be extended to predict long-term engagement, churn, and premium subscription uptake — forming a foundation for a data-led growth strategy that turns STADIOEquities' behavioural data into a sustained competitive advantage.

## Part B — Problem Statement

### Business Problem

STADIOEquities faces a critical funnel-leakage problem: 41% of registered accounts never deposit funds, and the conversion rate from registration to first deposit has declined from 64% to 59% in the past two years. At an acquisition cost of R180 per account, this represents significant wasted marketing spend and unrealized revenue potential. Current onboarding strategies use a one-size-fits-all approach, sending identical nudges and emails on a fixed schedule to all new registrants, which is both inefficient and ineffective.

### Data Science Problem

This project aims to develop a binary classification model that predicts whether a newly registered account will make its first deposit within a 30-day activation window, using features extracted from the account's early behaviour and demographics. The model will produce a probability score for each registrant that can be used to segment accounts into high-risk (unlikely to activate) and low-risk (likely to activate) groups, enabling targeted onboarding interventions.

### Key Research Questions

1. Which behavioural, demographic, and acquisition-channel features are the strongest predictors of account activation?
2. How accurately can a classification model predict activation status within the first 30 days of registration?
3. What is the optimal threshold for classifying accounts as "at risk" to maximize the business impact of targeted interventions?
4. How much improvement in activation rate can be achieved by redirecting the onboarding budget toward high-risk accounts?

### Success Criteria

The model is considered successful if it achieves:
- An AUC-ROC of at least 0.75 on a held-out test set
- A lift of at least 2x in the top decile compared to random targeting
- Actionable feature importance rankings that align with business intuition

---

## Repository Structure

```
STADIOEquities-Capstone/
├── README.md                       # This file (SS1 + SS2)
├── data_request.pdf                # SS1 Part C — data requested from the client
│
├── Preprocessing.MD                # SS2 Part B docs (link to src/)
├── FeatureEngineering.MD
├── Model1.MD
├── Model2.MD
├── Model1Performance.MD            # SS2 Part C docs
├── Model2Performance.MD
├── Comparison.MD
│
├── datasets/
│   ├── raw/bank-additional-full.csv    # public dataset (SS2)
│   └── processed/                      # generated splits (train/val/test [+ _fe])
├── src/                            # SS2 pipeline scripts
│   ├── pipeline_utils.py           #   shared loading / split / feature defs
│   ├── eval_utils.py               #   shared metrics + plotting
│   ├── preprocessing.py
│   ├── feature_engineering.py
│   ├── train_model1_logreg.py
│   ├── train_model2_xgboost.py
│   ├── evaluate_model1.py
│   ├── evaluate_model2.py
│   └── compare_models.py
├── models/                         # saved model artifacts (.joblib)
├── experimental_setup/
│   ├── requirements.txt
│   └── config.yaml
├── experimental_results/           # metrics (.json/.csv) + figures/
├── literature_review/
│   └── Part_A_Related_Work_and_Data.pdf
├── reports/
│   ├── Part_D_Recommendations.pdf
│   ├── build_part_a_pdf.py
│   └── build_part_d_pdf.py
├── statistical_scripts/            # SS1 placeholders (eda.py, model_comparison.py)
└── visualization_scripts/          # SS1 placeholder (plots.py)
```

---

## Part E — RAAIDD Log

| RAAIDD | Description |
|--------|-------------|
| **Risk** | The behavioural data (app sessions, onboarding steps) may have missing timestamps or incomplete records, reducing model input quality. |
| **Risk** | Class imbalance — since 59% activate and 41% do not, the model may be biased toward the majority class if not properly handled. |
| **Risk** | The data available covers four years of app behaviour but registration-to-deposit conversion has been declining, so the relationship between features and activation may not be stationary across time periods. |
| **Risk** | STADIOEquities' data platform is still being assembled; the joined data required for modelling may not be immediately available in the expected format. |
| **Risk** | Feature drift: if STADIOEquities changes its onboarding flow or acquisition channels during the project, previously trained models may degrade in performance. |
| **Action** | Obtain and explore the full dataset from STADIOEquities, performing data quality checks on completeness, consistency, and missingness. |
| **Action** | Conduct Exploratory Data Analysis (EDA) to understand feature distributions, correlations, and class balance before modelling. |
| **Action** | Implement and compare multiple classification models (e.g., Logistic Regression, Random Forest, Gradient Boosting, XGBoost) using cross-validation. |
| **Action** | Evaluate models using metrics appropriate for the business context (AUC-ROC, precision-recall, lift charts) and select the best performer. |
| **Action** | Produce feature importance analysis and interpret results in consultation with STADIOEquities' growth team to ensure business alignment. |
| **Assumption** | STADIOEquities will provide the datasets described in the Data Request (Part C) in a usable format and within the project timeline. |
| **Assumption** | The historical data (4 years of app behaviour, 6 years of account data) contains sufficient signal to train a meaningful activation prediction model. |
| **Assumption** | A 30-day activation window is an appropriate business metric — accounts that do not deposit within 30 days are unlikely to activate later without intervention. |
| **Assumption** | STADIOEquities' onboarding flow and acquisition channels have remained relatively stable over the past two years, so historical patterns are predictive of future behaviour. |
| **Assumption** | The client's unified client-data platform will allow joining of behavioural, financial, and demographic data at the account level. |
| **Issue** | Currently no issues have been identified. This section will be updated as the project progresses and any blockers or challenges arise. |
| **Decision** | The primary modelling task is binary classification (will activate within 30 days: yes/no) rather than survival analysis or regression, to keep the problem scope manageable and aligned with actionable business interventions. |
| **Decision** | The project will use Python as the primary programming language, with scikit-learn and XGBoost as the modelling libraries. |
| **Dependency** | Data must be received from STADIOEquities before any modelling work can begin. |
| **Dependency** | EDA and feature engineering must be completed before model training can commence. |
| **Dependency** | Model training and cross-validation must be completed before evaluation metrics can be finalized. |
| **Dependency** | Model evaluation results are needed before the final interpretation and business recommendations can be written. |
| **Dependency** | Feature importance analysis depends on the selection of a final model, which depends on model comparison results. |

---

*SS1 submission created 2026-09-05. SS2 submission adds the public-dataset viability proof.*
