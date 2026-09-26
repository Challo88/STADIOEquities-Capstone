"""
pipeline_utils.py
=================
Shared helper functions used across the STADIOEquities SS2 modelling pipeline.

Centralising the data-loading, splitting and feature-engineering logic here
guarantees that every script (preprocessing, feature engineering, Model 1,
Model 2, performance and comparison) sees *exactly* the same data and the same
feature definitions. This avoids the subtle train/test-skew bugs that occur
when preprocessing is copy-pasted between scripts.

Author: STADIOEquities Capstone (SS2)
"""

from __future__ import annotations

import os
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# --------------------------------------------------------------------------- #
# Paths
# --------------------------------------------------------------------------- #
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_CSV = os.path.join(ROOT, "datasets", "raw", "bank-additional-full.csv")
PROCESSED_DIR = os.path.join(ROOT, "datasets", "processed")
MODELS_DIR = os.path.join(ROOT, "models")
RESULTS_DIR = os.path.join(ROOT, "experimental_results")
FIG_DIR = os.path.join(RESULTS_DIR, "figures")

TARGET = "y"
# `duration` is excluded to prevent target leakage: it is only known *after* a
# contact has taken place, so it cannot be used for a realistic pre-contact
# prediction (Moro et al., 2014; the UCI dataset documentation makes the same
# point). This mirrors the SS1 constraint that only signals available *within*
# the activation window may be used as model inputs.
LEAKAGE_COLS = ["duration"]

# Split proportions carried over from the SS1 experimental_setup/config.yaml
TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15
RANDOM_STATE = 42


# --------------------------------------------------------------------------- #
# Loading & cleaning
# --------------------------------------------------------------------------- #
def load_raw() -> pd.DataFrame:
    """Load the raw UCI Bank Marketing CSV (semicolon-delimited)."""
    if not os.path.exists(RAW_CSV):
        raise FileNotFoundError(
            f"Raw dataset not found at {RAW_CSV}. "
            "Download bank-additional-full.csv from the UCI Machine Learning "
            "Repository (dataset 222) and place it in datasets/raw/."
        )
    return pd.read_csv(RAW_CSV, sep=";")


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """
    Minimal, leakage-free cleaning applied to the *whole* frame:

    * Map the target y (yes/no) -> (1/0).
    * Drop the leakage column(s).
    * Leave the 'unknown' tokens in the categorical columns untouched so that
      'missingness' can be modelled explicitly as its own category.
    """
    df = df.copy()
    df[TARGET] = (df[TARGET].astype(str).str.strip().str.lower() == "yes").astype(int)
    df = df.drop(columns=[c for c in LEAKAGE_COLS if c in df.columns])
    return df


def stratified_split(df: pd.DataFrame):
    """
    Stratified 70 / 15 / 15 split that preserves the ~11.3% positive prevalence
    in every fold (matches `stratify_by: activated_30day_flag` from the SS1
    config, and is how the Part A reference papers evaluate on this dataset).

    Why not a pure chronological split?
    -----------------------------------
    The CSV is date-ordered (May 2008 -> Nov 2010). A purely time-ordered split
    exposes very strong *non-stationarity*: the term-deposit subscription rate
    rises from ~5% in the earliest period to ~38% in the latest, driven by the
    macro-economic collapse in the euribor rate over 2008-2010. That is exactly
    the "relationship between features and activation may not be stationary
    across time periods" risk logged in SS1. We therefore evaluate on a
    stratified split for a clean, comparable viability test, and flag time-aware
    validation as required future work once STADIOEquities' real (and more
    stationary) data is available. See docs/Preprocessing.MD for the full note.
    """
    from sklearn.model_selection import train_test_split
    y = df[TARGET]
    train, temp = train_test_split(
        df, test_size=(VAL_RATIO + TEST_RATIO),
        stratify=y, random_state=RANDOM_STATE)
    rel = TEST_RATIO / (VAL_RATIO + TEST_RATIO)
    val, test = train_test_split(
        temp, test_size=rel, stratify=temp[TARGET], random_state=RANDOM_STATE)
    return (train.reset_index(drop=True),
            val.reset_index(drop=True),
            test.reset_index(drop=True))


# --------------------------------------------------------------------------- #
# Feature engineering
# --------------------------------------------------------------------------- #
def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Derive additional features from the cleaned frame. Every transformation
    here is row-wise (depends only on the row itself), so it can be applied to
    train, validation and test independently with no risk of leakage.

    New features
    ------------
    was_contacted_before : 1 if the client was contacted in a previous campaign
                           (pdays != 999), else 0.
    prev_contact_success : 1 if the previous campaign outcome was 'success'.
    age_group            : coarse age bands (mirrors the SS1 'Age group' field).
    campaign_intensity   : banded number of contacts in the current campaign
                           (mirrors SS1 'Total nudges sent').
    contacted_and_success: interaction of was_contacted_before & poutcome.
    """
    df = df.copy()

    # pdays == 999 is the sentinel for "never previously contacted".
    df["was_contacted_before"] = (df["pdays"] != 999).astype(int)
    # Replace the 999 sentinel with 0 so the numeric column is not distorted;
    # the information it carried is preserved in was_contacted_before.
    df["pdays"] = df["pdays"].replace(999, 0)

    df["prev_contact_success"] = (df["poutcome"] == "success").astype(int)

    df["age_group"] = pd.cut(
        df["age"],
        bins=[17, 24, 34, 44, 54, 64, 200],
        labels=["18-24", "25-34", "35-44", "45-54", "55-64", "65+"],
    ).astype(str)

    df["campaign_intensity"] = pd.cut(
        df["campaign"],
        bins=[0, 1, 2, 3, 5, 1000],
        labels=["1", "2", "3", "4-5", "6+"],
    ).astype(str)

    # Simple, business-meaningful interaction feature.
    df["contacted_and_success"] = (
        df["was_contacted_before"] * df["prev_contact_success"]
    )

    return df


# Column groups AFTER feature engineering ----------------------------------- #
NUMERIC_FEATURES = [
    "age", "campaign", "pdays", "previous",
    "emp.var.rate", "cons.price.idx", "cons.conf.idx", "euribor3m", "nr.employed",
    "was_contacted_before", "prev_contact_success", "contacted_and_success",
]
CATEGORICAL_FEATURES = [
    "job", "marital", "education", "default", "housing", "loan",
    "contact", "month", "day_of_week", "poutcome",
    "age_group", "campaign_intensity",
]


def build_feature_pipeline(scale_numeric: bool = True) -> ColumnTransformer:
    """
    Build the sklearn ColumnTransformer that turns the engineered frame into a
    numeric matrix.

    * Categoricals -> one-hot encoding (unknown categories ignored at predict
      time so the pipeline never crashes on an unseen value).
    * Numerics    -> standard-scaled when `scale_numeric` is True (needed for
      Logistic Regression) and passed through untouched for tree models
      (XGBoost is scale-invariant).

    The transformer is *fit on the training fold only* by the calling model
    script, which is what prevents information from the validation/test folds
    leaking into the feature representation.
    """
    numeric_step = StandardScaler() if scale_numeric else "passthrough"
    return ColumnTransformer(
        transformers=[
            ("num", numeric_step, NUMERIC_FEATURES),
            ("cat",
             OneHotEncoder(handle_unknown="ignore", sparse_output=False),
             CATEGORICAL_FEATURES),
        ],
        remainder="drop",
    )


def get_feature_names(fitted_ct: ColumnTransformer) -> list[str]:
    """Return readable feature names from a fitted ColumnTransformer."""
    names = list(NUMERIC_FEATURES)
    ohe = fitted_ct.named_transformers_["cat"]
    names += list(ohe.get_feature_names_out(CATEGORICAL_FEATURES))
    return names


def load_split(split: str) -> pd.DataFrame:
    """Load a processed split ('train'/'val'/'test') produced by preprocessing.py."""
    path = os.path.join(PROCESSED_DIR, f"{split}.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"{path} not found. Run `python src/preprocessing.py` first."
        )
    return pd.read_csv(path)


def xy(df: pd.DataFrame):
    """Split an engineered frame into (X, y)."""
    y = df[TARGET].values
    X = df.drop(columns=[TARGET])
    return X, y
