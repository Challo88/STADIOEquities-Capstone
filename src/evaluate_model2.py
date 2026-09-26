"""
evaluate_model2.py
==================
Part C performance evaluation for Model 2 (XGBoost).

Loads the trained Model 2 bundle (fitted ColumnTransformer + XGBClassifier),
applies it to the held-out TEST split, and reports the full metric suite plus a
bootstrap 95% confidence interval for ROC-AUC. It also writes the top-15 feature
importances (gain) for interpretation. Figures are saved to
experimental_results/figures/.

Run
---
    python src/evaluate_model2.py   (run AFTER train_model2_xgboost.py)

Outputs
-------
    experimental_results/model2_test_metrics.json
    experimental_results/model2_feature_importance.csv
    experimental_results/figures/model2_*.png
"""

import json
import os
import joblib
import numpy as np
import pandas as pd

import pipeline_utils as pu
import eval_utils as ev


def main() -> None:
    os.makedirs(pu.FIG_DIR, exist_ok=True)

    bundle = joblib.load(os.path.join(pu.MODELS_DIR, "model2_xgboost.joblib"))
    ct = bundle["column_transformer"]
    clf = bundle["classifier"]
    thr = json.load(open(os.path.join(
        pu.RESULTS_DIR, "model2_val_threshold.json")))["selected_threshold"]

    test = pu.load_split("test_fe")
    X_test, y_test = pu.xy(test)
    Xt_test = ct.transform(X_test)
    y_prob = clf.predict_proba(Xt_test)[:, 1]

    metrics = ev.core_metrics(y_test, y_prob, thr)
    metrics["lift_top_decile"] = ev.lift_top_decile(y_test, y_prob)
    lo, hi = ev.bootstrap_auc_ci(y_test, y_prob)
    metrics["roc_auc_ci95"] = [lo, hi]
    metrics["model"] = "XGBoost"

    ev.save_json(metrics, os.path.join(pu.RESULTS_DIR, "model2_test_metrics.json"))

    # Feature importance (gain) with readable names.
    names = pu.get_feature_names(ct)
    importances = clf.feature_importances_
    fi = (pd.DataFrame({"feature": names, "importance": importances})
          .sort_values("importance", ascending=False))
    fi.to_csv(os.path.join(pu.RESULTS_DIR, "model2_feature_importance.csv"),
              index=False)

    ev.plot_confusion(y_test, y_prob, thr, "Model 2 - XGBoost",
                      os.path.join(pu.FIG_DIR, "model2_confusion.png"))
    ev.plot_roc({"XGBoost": (y_test, y_prob)},
                os.path.join(pu.FIG_DIR, "model2_roc.png"),
                "Model 2 ROC (test)")
    ev.plot_pr({"XGBoost": (y_test, y_prob)},
               os.path.join(pu.FIG_DIR, "model2_pr.png"),
               "Model 2 Precision-Recall (test)")
    ev.plot_lift({"XGBoost": (y_test, y_prob)},
                 os.path.join(pu.FIG_DIR, "model2_gains.png"),
                 "Model 2 cumulative gains (test)")

    print("=== Model 2 (XGBoost) - TEST ===")
    for k in ["accuracy", "precision", "recall", "f1", "roc_auc", "pr_auc",
              "lift_top_decile"]:
        print(f"  {k:16s}: {metrics[k]:.4f}")
    print(f"  ROC-AUC 95% CI  : [{lo:.4f}, {hi:.4f}]")
    print("\nTop 10 features by gain:")
    print(fi.head(10).to_string(index=False))
    print("Saved metrics + figures for Model 2.")


if __name__ == "__main__":
    main()
