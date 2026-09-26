"""
eval_utils.py
=============
Shared evaluation helpers (metrics, bootstrap confidence intervals, lift, and
plotting) used by the Part C performance and comparison scripts.
"""

from __future__ import annotations

import json
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")  # headless backend
import matplotlib.pyplot as plt

from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score, confusion_matrix,
    roc_curve, precision_recall_curve,
)

RNG = np.random.default_rng(42)


def core_metrics(y_true, y_prob, threshold: float) -> dict:
    """Return the headline classification metrics at a given threshold."""
    y_pred = (y_prob >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    return {
        "threshold": float(threshold),
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_true, y_prob)),
        "pr_auc": float(average_precision_score(y_true, y_prob)),
        "tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp),
    }


def lift_top_decile(y_true, y_prob) -> float:
    """
    Lift in the top-decile: how many times more positives the model finds in the
    top 10% of ranked scores than random targeting would. This is one of the
    SS1 success criteria (target: >= 2x).
    """
    y_true = np.asarray(y_true)
    order = np.argsort(y_prob)[::-1]
    k = max(1, int(0.10 * len(y_true)))
    top_rate = y_true[order[:k]].mean()
    base_rate = y_true.mean()
    return float(top_rate / base_rate) if base_rate > 0 else float("nan")


def bootstrap_auc_ci(y_true, y_prob, n_boot: int = 1000, alpha: float = 0.05):
    """Percentile bootstrap confidence interval for ROC-AUC."""
    y_true = np.asarray(y_true)
    y_prob = np.asarray(y_prob)
    n = len(y_true)
    aucs = []
    for _ in range(n_boot):
        idx = RNG.integers(0, n, n)
        if len(np.unique(y_true[idx])) < 2:
            continue
        aucs.append(roc_auc_score(y_true[idx], y_prob[idx]))
    lo, hi = np.percentile(aucs, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return float(lo), float(hi)


def best_f1_threshold(y_true, y_prob):
    """Pick the probability threshold that maximises F1 on the given set."""
    prec, rec, thr = precision_recall_curve(y_true, y_prob)
    f1 = 2 * prec * rec / (prec + rec + 1e-12)
    # thr has len = len(prec) - 1
    best_idx = int(np.nanargmax(f1[:-1])) if len(thr) else 0
    return float(thr[best_idx]) if len(thr) else 0.5


def save_json(obj: dict, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fh:
        json.dump(obj, fh, indent=2)


# --------------------------------------------------------------------------- #
# Plots
# --------------------------------------------------------------------------- #
def plot_confusion(y_true, y_prob, threshold, title, path):
    y_pred = (y_prob >= threshold).astype(int)
    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots(figsize=(4.2, 3.8))
    im = ax.imshow(cm, cmap="Blues")
    for (i, j), v in np.ndenumerate(cm):
        ax.text(j, i, f"{v:,}", ha="center", va="center",
                color="white" if v > cm.max() / 2 else "black", fontsize=11)
    ax.set_xticks([0, 1]); ax.set_yticks([0, 1])
    ax.set_xticklabels(["No (0)", "Yes (1)"])
    ax.set_yticklabels(["No (0)", "Yes (1)"])
    ax.set_xlabel("Predicted"); ax.set_ylabel("Actual")
    ax.set_title(title)
    fig.colorbar(im, fraction=0.046, pad=0.04)
    fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig)


def plot_roc(curves: dict, path, title="ROC curves"):
    fig, ax = plt.subplots(figsize=(5, 4.2))
    for label, (y_true, y_prob) in curves.items():
        fpr, tpr, _ = roc_curve(y_true, y_prob)
        auc = roc_auc_score(y_true, y_prob)
        ax.plot(fpr, tpr, label=f"{label} (AUC={auc:.3f})")
    ax.plot([0, 1], [0, 1], "k--", alpha=0.5, label="Random")
    ax.set_xlabel("False positive rate"); ax.set_ylabel("True positive rate")
    ax.set_title(title); ax.legend(loc="lower right", fontsize=9)
    fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig)


def plot_pr(curves: dict, path, title="Precision-Recall curves"):
    fig, ax = plt.subplots(figsize=(5, 4.2))
    for label, (y_true, y_prob) in curves.items():
        prec, rec, _ = precision_recall_curve(y_true, y_prob)
        ap = average_precision_score(y_true, y_prob)
        ax.plot(rec, prec, label=f"{label} (AP={ap:.3f})")
    base = np.asarray(list(curves.values())[0][0]).mean()
    ax.axhline(base, ls="--", color="k", alpha=0.5, label=f"Baseline ({base:.3f})")
    ax.set_xlabel("Recall"); ax.set_ylabel("Precision")
    ax.set_title(title); ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig)


def plot_lift(curves: dict, path, title="Cumulative gains"):
    fig, ax = plt.subplots(figsize=(5, 4.2))
    for label, (y_true, y_prob) in curves.items():
        y_true = np.asarray(y_true)
        order = np.argsort(y_prob)[::-1]
        gains = np.cumsum(y_true[order]) / y_true.sum()
        pct = np.arange(1, len(y_true) + 1) / len(y_true)
        ax.plot(pct, gains, label=label)
    ax.plot([0, 1], [0, 1], "k--", alpha=0.5, label="Random")
    ax.set_xlabel("Proportion of accounts targeted (ranked)")
    ax.set_ylabel("Proportion of activators captured")
    ax.set_title(title); ax.legend(loc="lower right", fontsize=9)
    fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig)
