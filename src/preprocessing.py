"""
preprocessing.py
================
Step 1 of the STADIOEquities SS2 pipeline.

Loads the raw UCI Bank Marketing dataset, applies leakage-free cleaning
(target encoding, dropping the `duration` leakage column, keeping 'unknown'
as an explicit category) and produces a chronological train / validation /
test split saved to `datasets/processed/`.

Run
---
    python src/preprocessing.py

Outputs
-------
    datasets/processed/train.csv
    datasets/processed/val.csv
    datasets/processed/test.csv
    experimental_results/class_balance.csv
"""

import os
import pandas as pd

import pipeline_utils as pu


def main() -> None:
    os.makedirs(pu.PROCESSED_DIR, exist_ok=True)
    os.makedirs(pu.RESULTS_DIR, exist_ok=True)

    print("Loading raw dataset ...")
    raw = pu.load_raw()
    print(f"  raw shape: {raw.shape}")

    print("Cleaning (encode target, drop leakage columns) ...")
    clean_df = pu.clean(raw)
    print(f"  dropped leakage columns: {pu.LEAKAGE_COLS}")
    print(f"  overall positive rate:   {clean_df[pu.TARGET].mean():.4f}")

    print("Stratified split (70 / 15 / 15, preserving prevalence) ...")
    train, val, test = pu.stratified_split(clean_df)

    for name, part in [("train", train), ("val", val), ("test", test)]:
        out = os.path.join(pu.PROCESSED_DIR, f"{name}.csv")
        part.to_csv(out, index=False)
        print(f"  {name:5s}: {part.shape[0]:>6d} rows | "
              f"positive rate {part[pu.TARGET].mean():.4f} | -> {out}")

    # Persist the class balance per split for the reporting layer.
    balance = pd.DataFrame({
        "split": ["train", "val", "test", "overall"],
        "n": [len(train), len(val), len(test), len(clean_df)],
        "n_positive": [int(train[pu.TARGET].sum()), int(val[pu.TARGET].sum()),
                       int(test[pu.TARGET].sum()), int(clean_df[pu.TARGET].sum())],
        "positive_rate": [train[pu.TARGET].mean(), val[pu.TARGET].mean(),
                          test[pu.TARGET].mean(), clean_df[pu.TARGET].mean()],
    })
    balance.to_csv(os.path.join(pu.RESULTS_DIR, "class_balance.csv"), index=False)
    print("Saved class balance summary to experimental_results/class_balance.csv")
    print("Preprocessing complete.")


if __name__ == "__main__":
    main()
