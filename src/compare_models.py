"""
compare_models.py
=================
Part C model comparison for Model 1 (Logistic Regression) vs Model 2 (XGBoost).

Produces a side-by-side metric table on the held-out TEST split and applies two
statistical procedures to decide whether any performance gap is real rather than
noise:

1. McNemar's test on the paired test-set predictions (are the two models'
   error patterns significantly different?).
2. A bootstrap 95% confidence interval for the *difference* in ROC-AUC.
3. Stratified 5-fold cross-validation ROC-AUC on the training data with a paired
   t-test across folds (the procedure sketched in the SS1 model_comparison.py).

Overlaid ROC, PR and cumulative-gains curves are saved for both models.

Run
---
    python src/compare_models.py   (run AFTER both models are trained)

Outputs
-------
    experimental_results/comparison_metrics.json
    experimental_results/comparison_table.csv
    experimental_results/figures/comparison_*.png
"""

import json
import os
import joblib
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.base import clone
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier

import pipeline_utils as pu
import eval_utils as ev


def mcnemar_test(y_true, pred_a, pred_b):
    """McNemar's test (with continuity correction) on paired predictions."""
    correct_a = (pred_a == y_true)
    correct_b = (pred_b == y_true)
    b = int(np.sum(correct_a & ~correct_b))   # A right, B wrong
    c = int(np.sum(~correct_a & correct_b))   # A wrong, B right
    if (b + c) == 0:
        return {"b": b, "c": c, "statistic": 0.0, "p_value": 1.0}
    stat = (abs(b - c) - 1) ** 2 / (b + c)
    p = float(stats.chi2.sf(stat, df=1))
    return {"b": b, "c": c, "statistic": float(stat), "p_value": p}


def bootstrap_auc_diff_ci(y_true, prob_a, prob_b, n_boot=1000, alpha=0.05):
    """Bootstrap CI for AUC(model B) - AUC(model A)."""
    y_true = np.asarray(y_true); prob_a = np.asarray(prob_a); prob_b = np.asarray(prob_b)
    n = len(y_true); diffs = []
    rng = np.random.default_rng(7)
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        if len(np.unique(y_true[idx])) < 2:
            continue
        diffs.append(roc_auc_score(y_true[idx], prob_b[idx]) -
                     roc_auc_score(y_true[idx], prob_a[idx]))
    lo, hi = np.percentile(diffs, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return float(np.mean(diffs)), float(lo), float(hi)


def cv_paired_ttest():
    """5-fold stratified CV ROC-AUC for both models + paired t-test across folds."""
    train = pu.load_split("train_fe")
    X, y = pu.xy(train)

    lr = Pipeline([
        ("features", pu.build_feature_pipeline(scale_numeric=True)),
        ("clf", LogisticRegression(max_iter=1000, class_weight="balanced",
                                   random_state=pu.RANDOM_STATE)),
    ])
    spw = (len(y) - y.sum()) / max(1, y.sum())
    xgb_ct = pu.build_feature_pipeline(scale_numeric=False)
    xgb = XGBClassifier(n_estimators=300, max_depth=5, learning_rate=0.05,
                        subsample=0.9, colsample_bytree=0.9, reg_lambda=1.0,
                        min_child_weight=2, scale_pos_weight=spw,
                        objective="binary:logistic", eval_metric="auc",
                        tree_method="hist", random_state=pu.RANDOM_STATE, n_jobs=4)

    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=pu.RANDOM_STATE)
    auc_lr, auc_xgb = [], []
    for tr, te in skf.split(X, y):
        Xtr, Xte = X.iloc[tr], X.iloc[te]
        ytr, yte = y[tr], y[te]

        lr_f = clone(lr); lr_f.fit(Xtr, ytr)
        auc_lr.append(roc_auc_score(yte, lr_f.predict_proba(Xte)[:, 1]))

        ct_f = clone(xgb_ct); Xt_tr = ct_f.fit_transform(Xtr); Xt_te = ct_f.transform(Xte)
        xgb_f = clone(xgb); xgb_f.fit(Xt_tr, ytr)
        auc_xgb.append(roc_auc_score(yte, xgb_f.predict_proba(Xt_te)[:, 1]))

    t_stat, p_val = stats.ttest_rel(auc_xgb, auc_lr)
    return {
        "cv_auc_logreg_mean": float(np.mean(auc_lr)),
        "cv_auc_logreg_std": float(np.std(auc_lr)),
        "cv_auc_xgboost_mean": float(np.mean(auc_xgb)),
        "cv_auc_xgboost_std": float(np.std(auc_xgb)),
        "paired_ttest_statistic": float(t_stat),
        "paired_ttest_p_value": float(p_val),
        "folds_auc_logreg": [float(a) for a in auc_lr],
        "folds_auc_xgboost": [float(a) for a in auc_xgb],
    }


def main() -> None:
    os.makedirs(pu.FIG_DIR, exist_ok=True)

    # ---- load models & test data -----------------------------------------
    m1 = joblib.load(os.path.join(pu.MODELS_DIR, "model1_logreg.joblib"))
    b2 = joblib.load(os.path.join(pu.MODELS_DIR, "model2_xgboost.joblib"))
    thr1 = json.load(open(os.path.join(pu.RESULTS_DIR, "model1_val_threshold.json")))["selected_threshold"]
    thr2 = json.load(open(os.path.join(pu.RESULTS_DIR, "model2_val_threshold.json")))["selected_threshold"]

    test = pu.load_split("test_fe")
    X_test, y_test = pu.xy(test)

    p1 = m1.predict_proba(X_test)[:, 1]
    p2 = b2["classifier"].predict_proba(b2["column_transformer"].transform(X_test))[:, 1]
    pred1 = (p1 >= thr1).astype(int)
    pred2 = (p2 >= thr2).astype(int)

    met1 = ev.core_metrics(y_test, p1, thr1); met1["lift_top_decile"] = ev.lift_top_decile(y_test, p1)
    met2 = ev.core_metrics(y_test, p2, thr2); met2["lift_top_decile"] = ev.lift_top_decile(y_test, p2)

    # ---- comparison table -------------------------------------------------
    rows = []
    for name, m in [("Logistic Regression", met1), ("XGBoost", met2)]:
        rows.append({
            "model": name, "accuracy": m["accuracy"], "precision": m["precision"],
            "recall": m["recall"], "f1": m["f1"], "roc_auc": m["roc_auc"],
            "pr_auc": m["pr_auc"], "lift_top_decile": m["lift_top_decile"],
        })
    table = pd.DataFrame(rows)
    table.to_csv(os.path.join(pu.RESULTS_DIR, "comparison_table.csv"), index=False)

    # ---- statistical tests ------------------------------------------------
    mcn = mcnemar_test(y_test, pred1, pred2)
    diff_mean, diff_lo, diff_hi = bootstrap_auc_diff_ci(y_test, p1, p2)
    print("Running 5-fold CV + paired t-test (this takes a moment) ...")
    cv = cv_paired_ttest()

    comparison = {
        "test_metrics": {"logistic_regression": met1, "xgboost": met2},
        "mcnemar_test": mcn,
        "auc_difference_xgb_minus_lr": {
            "mean": diff_mean, "ci95": [diff_lo, diff_hi]},
        "cross_validation": cv,
    }
    ev.save_json(comparison, os.path.join(pu.RESULTS_DIR, "comparison_metrics.json"))

    # ---- overlaid plots ---------------------------------------------------
    curves = {"Logistic Regression": (y_test, p1), "XGBoost": (y_test, p2)}
    ev.plot_roc(curves, os.path.join(pu.FIG_DIR, "comparison_roc.png"),
                "Model comparison - ROC (test)")
    ev.plot_pr(curves, os.path.join(pu.FIG_DIR, "comparison_pr.png"),
               "Model comparison - Precision-Recall (test)")
    ev.plot_lift(curves, os.path.join(pu.FIG_DIR, "comparison_gains.png"),
                 "Model comparison - cumulative gains (test)")

    # ---- console summary --------------------------------------------------
    print("\n=== TEST-SET COMPARISON ===")
    print(table.to_string(index=False,
          formatters={c: "{:.4f}".format for c in table.columns if c != "model"}))
    print("\nMcNemar's test: chi2={:.3f}, p={:.4g} "
          "(b=A-right/B-wrong={}, c=A-wrong/B-right={})".format(
              mcn["statistic"], mcn["p_value"], mcn["b"], mcn["c"]))
    print("AUC(XGB)-AUC(LR): {:+.4f}  95% CI [{:+.4f}, {:+.4f}]".format(
        diff_mean, diff_lo, diff_hi))
    print("CV ROC-AUC  LR : {:.4f} +/- {:.4f}".format(
        cv["cv_auc_logreg_mean"], cv["cv_auc_logreg_std"]))
    print("CV ROC-AUC  XGB: {:.4f} +/- {:.4f}".format(
        cv["cv_auc_xgboost_mean"], cv["cv_auc_xgboost_std"]))
    print("Paired t-test across folds: t={:.3f}, p={:.4g}".format(
        cv["paired_ttest_statistic"], cv["paired_ttest_p_value"]))
    print("\nSaved comparison metrics + figures.")


if __name__ == "__main__":
    main()
