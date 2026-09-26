"""
train_model1_logreg.py
======================
Model 1 (of 2): Logistic Regression.

Logistic Regression is the interpretable linear baseline recommended in the
SS1 experimental_setup/config.yaml and used as the reference classifier across
the Part A literature (Moro et al., 2014; Dias & Antonio, 2025). It produces a
calibrated-ish probability and transparent coefficients, which is valuable for a
client who wants to understand *why* an account is flagged.

Pipeline
--------
    engineer features (via feature-engineered CSV)
        -> ColumnTransformer (StandardScaler on numerics + OneHot on categoricals)
            -> LogisticRegression(class_weight="balanced")

Class imbalance (~11% positive) is handled with `class_weight="balanced"`,
which re-weights the loss inversely to class frequency.

Run
---
    python src/train_model1_logreg.py   (run AFTER feature_engineering.py)

Outputs
-------
    models/model1_logreg.joblib
    experimental_results/model1_val_threshold.json
"""

import os
import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

import pipeline_utils as pu
import eval_utils as ev


def build_model() -> Pipeline:
    return Pipeline([
        ("features", pu.build_feature_pipeline(scale_numeric=True)),
        ("clf", LogisticRegression(
            max_iter=1000,
            class_weight="balanced",
            C=1.0,
            solver="lbfgs",
            random_state=pu.RANDOM_STATE,
        )),
    ])


def main() -> None:
    os.makedirs(pu.MODELS_DIR, exist_ok=True)

    train = pu.load_split("train_fe")
    val = pu.load_split("val_fe")
    X_train, y_train = pu.xy(train)
    X_val, y_val = pu.xy(val)

    print("Training Model 1: Logistic Regression (class_weight=balanced) ...")
    model = build_model()
    model.fit(X_train, y_train)

    # Choose an operating threshold on the VALIDATION set (never on test).
    val_prob = model.predict_proba(X_val)[:, 1]
    thr = ev.best_f1_threshold(y_val, val_prob)
    val_metrics = ev.core_metrics(y_val, val_prob, thr)
    val_metrics["lift_top_decile"] = ev.lift_top_decile(y_val, val_prob)
    val_metrics["selected_threshold"] = thr

    joblib.dump(model, os.path.join(pu.MODELS_DIR, "model1_logreg.joblib"))
    ev.save_json(val_metrics,
                 os.path.join(pu.RESULTS_DIR, "model1_val_threshold.json"))

    print(f"  Selected threshold (max F1 on val): {thr:.3f}")
    print(f"  Val ROC-AUC: {val_metrics['roc_auc']:.4f} | "
          f"Val F1: {val_metrics['f1']:.4f} | "
          f"Val recall: {val_metrics['recall']:.4f}")
    print("Model 1 saved to models/model1_logreg.joblib")


if __name__ == "__main__":
    main()
