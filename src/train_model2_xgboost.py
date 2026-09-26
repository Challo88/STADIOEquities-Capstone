"""
train_model2_xgboost.py
=======================
Model 2 (of 2): XGBoost (extreme gradient-boosted decision trees).

XGBoost is the strongest performer reported across the Part A literature
(Dias & Antonio, 2025 report XGBoost as their best model; Arifah et al., 2025
apply XGBoost to this exact Bank Marketing dataset). It captures non-linear
interactions between behavioural and demographic features that a linear model
cannot, at the cost of interpretability.

Pipeline
--------
    engineer features (via feature-engineered CSV)
        -> ColumnTransformer (passthrough numerics + OneHot on categoricals)
            -> XGBClassifier(scale_pos_weight = n_neg / n_pos)

Numerics are NOT scaled: gradient-boosted trees are invariant to monotone
feature transforms, so scaling would add nothing. Class imbalance is handled
with `scale_pos_weight`, the XGBoost-native equivalent of class weighting.
Early stopping on the validation fold guards against over-fitting.

Run
---
    python src/train_model2_xgboost.py   (run AFTER feature_engineering.py)

Outputs
-------
    models/model2_xgboost.joblib
    experimental_results/model2_val_threshold.json
"""

import os
import joblib
import numpy as np
from xgboost import XGBClassifier

import pipeline_utils as pu
import eval_utils as ev


def main() -> None:
    os.makedirs(pu.MODELS_DIR, exist_ok=True)

    train = pu.load_split("train_fe")
    val = pu.load_split("val_fe")
    X_train, y_train = pu.xy(train)
    X_val, y_val = pu.xy(val)

    # Fit the shared feature transformer on TRAIN only (no scaling for trees).
    ct = pu.build_feature_pipeline(scale_numeric=False)
    Xt_train = ct.fit_transform(X_train)
    Xt_val = ct.transform(X_val)

    n_pos = int(y_train.sum())
    n_neg = int(len(y_train) - n_pos)
    spw = n_neg / max(1, n_pos)

    print("Training Model 2: XGBoost (scale_pos_weight={:.2f}) ...".format(spw))
    clf = XGBClassifier(
        n_estimators=400,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.9,
        colsample_bytree=0.9,
        reg_lambda=1.0,
        min_child_weight=2,
        scale_pos_weight=spw,
        objective="binary:logistic",
        eval_metric="auc",
        early_stopping_rounds=30,
        random_state=pu.RANDOM_STATE,
        n_jobs=4,
        tree_method="hist",
    )
    clf.fit(Xt_train, y_train, eval_set=[(Xt_val, y_val)], verbose=False)

    # Persist the fitted transformer together with the classifier so that
    # evaluation/comparison reproduce the exact same feature space.
    bundle = {"column_transformer": ct, "classifier": clf,
              "best_iteration": int(getattr(clf, "best_iteration", clf.n_estimators))}
    joblib.dump(bundle, os.path.join(pu.MODELS_DIR, "model2_xgboost.joblib"))

    val_prob = clf.predict_proba(Xt_val)[:, 1]
    thr = ev.best_f1_threshold(y_val, val_prob)
    val_metrics = ev.core_metrics(y_val, val_prob, thr)
    val_metrics["lift_top_decile"] = ev.lift_top_decile(y_val, val_prob)
    val_metrics["selected_threshold"] = thr
    val_metrics["best_iteration"] = bundle["best_iteration"]
    ev.save_json(val_metrics,
                 os.path.join(pu.RESULTS_DIR, "model2_val_threshold.json"))

    print(f"  Best boosting iteration (early stopping): {bundle['best_iteration']}")
    print(f"  Selected threshold (max F1 on val): {thr:.3f}")
    print(f"  Val ROC-AUC: {val_metrics['roc_auc']:.4f} | "
          f"Val F1: {val_metrics['f1']:.4f} | "
          f"Val recall: {val_metrics['recall']:.4f}")
    print("Model 2 saved to models/model2_xgboost.joblib")


if __name__ == "__main__":
    main()
