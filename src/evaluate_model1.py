"""
evaluate_model1.py
==================
Part C performance evaluation for Model 1 (Logistic Regression).

Loads the trained Model 1, applies it to the held-out TEST split, and reports
the full metric suite (accuracy, precision, recall, F1, ROC-AUC, PR-AUC,
confusion matrix, top-decile lift) together with a bootstrap 95% confidence
interval for ROC-AUC. Figures (ROC, PR, confusion, gains) are saved to
experimental_results/figures/.

Run
---
    python src/evaluate_model1.py   (run AFTER train_model1_logreg.py)

Outputs
-------
    experimental_results/model1_test_metrics.json
    experimental_results/figures/model1_*.png
"""

import json
import os
import joblib

import pipeline_utils as pu
import eval_utils as ev


def main() -> None:
    os.makedirs(pu.FIG_DIR, exist_ok=True)

    model = joblib.load(os.path.join(pu.MODELS_DIR, "model1_logreg.joblib"))
    thr = json.load(open(os.path.join(
        pu.RESULTS_DIR, "model1_val_threshold.json")))["selected_threshold"]

    test = pu.load_split("test_fe")
    X_test, y_test = pu.xy(test)
    y_prob = model.predict_proba(X_test)[:, 1]

    metrics = ev.core_metrics(y_test, y_prob, thr)
    metrics["lift_top_decile"] = ev.lift_top_decile(y_test, y_prob)
    lo, hi = ev.bootstrap_auc_ci(y_test, y_prob)
    metrics["roc_auc_ci95"] = [lo, hi]
    metrics["model"] = "Logistic Regression"

    ev.save_json(metrics, os.path.join(pu.RESULTS_DIR, "model1_test_metrics.json"))
    ev.plot_confusion(y_test, y_prob, thr, "Model 1 - Logistic Regression",
                      os.path.join(pu.FIG_DIR, "model1_confusion.png"))
    ev.plot_roc({"Logistic Regression": (y_test, y_prob)},
                os.path.join(pu.FIG_DIR, "model1_roc.png"),
                "Model 1 ROC (test)")
    ev.plot_pr({"Logistic Regression": (y_test, y_prob)},
               os.path.join(pu.FIG_DIR, "model1_pr.png"),
               "Model 1 Precision-Recall (test)")
    ev.plot_lift({"Logistic Regression": (y_test, y_prob)},
                 os.path.join(pu.FIG_DIR, "model1_gains.png"),
                 "Model 1 cumulative gains (test)")

    print("=== Model 1 (Logistic Regression) - TEST ===")
    for k in ["accuracy", "precision", "recall", "f1", "roc_auc", "pr_auc",
              "lift_top_decile"]:
        print(f"  {k:16s}: {metrics[k]:.4f}")
    print(f"  ROC-AUC 95% CI  : [{lo:.4f}, {hi:.4f}]")
    print("Saved metrics + figures for Model 1.")


if __name__ == "__main__":
    main()
