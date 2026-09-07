# STADIOEquities Capstone Project — SS1 Submission

**Module:** CAP182 — Capstone (School of Information Technology)

**Client:** STADIOEquities (Retail Investing & Fintech)

**Project Title:** Predicting Account Activation to Reduce the Registration-to-Deposit Funnel Leakage

**Student:** Charlton Allen (26305072)


---

## Part A — Motivation

STADIOEquities has achieved remarkable growth in customer acquisition, with 2.3 million registered accounts and revenue up 22% year-on-year. However, this growth masks a critical inefficiency that is eroding the return on every marketing rand spent: **41% of registered accounts never deposit funds**, and the sign-up-to-first-deposit conversion rate has declined from 64% to 59% over the past two years. With a customer acquisition cost of R180 per account, each account that registers but never activates represents a direct loss. Scaling this across the full registration base, STADIOEquities is spending millions acquiring accounts that generate zero revenue.

The root cause is not a lack of data — it is a lack of insight. STADIOEquities currently sends onboarding emails and nudges on a fixed schedule to every new registrant, regardless of whether they are about to activate or about to disappear. The company already observes that drop-off clusters by acquisition channel, onboarding completion depth, first-session behaviour, and time-to-first-deposit. Yet no model exists to exploit these signals and act on them.

This project will build a supervised machine learning classification model that predicts, for each newly registered account, the probability that the account will make its first deposit within a defined activation window. By identifying accounts that are likely to stall, STADIOEquities can re-target its onboarding interventions — sending more intensive nudges to high-risk accounts and reducing unnecessary outreach to those who are likely to activate naturally. This directly supports two of the company's 2030 strategic priorities:

1. **"Activate the accounts we already have"** — Convert far more registrations into funded, trading clients by spotting who is likely to activate or stall and intervening at the right moment.
2. **"Understand every client's investing style"** — Group clients by how they actually behave so content, nudges, and product suggestions finally fit the person receiving them.

Beyond the immediate activation benefit, the same modelling framework can be extended to predict long-term engagement, churn, and premium subscription uptake — forming a foundation for a data-led growth strategy that turns STADIOEquities' behavioural data into a sustained competitive advantage.

---

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

This repository contains all code, data, models, and results for the STADIOEquities account activation prediction project.

```
STADIOEquities-Capstone/
├── README.md                     # This file — project overview, motivation, problem statement, RAAIDD log
├── datasets/                     # Raw and processed data files
│   ├── raw/                      # Original data as received from client
│   └── processed/                # Cleaned, transformed data ready for modelling
├── models/                       # Trained model artifacts and model metadata
├── experimental_setup/           # Environment configuration, requirements, and experiment tracking
│   ├── requirements.txt          # Python package dependencies
│   └── config.yaml               # Experiment parameters (train/test split, model hyperparameters)
├── experimental_results/         # Model evaluation outputs, metrics, and comparison reports
├── statistical_scripts/          # Statistical analysis, EDA, and comparison scripts
│   ├── eda.py                    # Exploratory Data Analysis
│   └── model_comparison.py       # Model comparison and statistical tests
└── visualization_scripts/        # Visualization and dashboard generation scripts
    └── plots.py                  # Feature importance, ROC curves, confusion matrices
```

---

## Part E — RAAIDD Log

### RAAIDD Log

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

*Repository created for SS1 Capstone Project submission.*
