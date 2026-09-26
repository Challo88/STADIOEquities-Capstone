"""
feature_engineering.py
======================
Step 2 of the STADIOEquities SS2 pipeline.

Applies the row-wise feature engineering defined in `pipeline_utils.engineer_features`
to each processed split and writes the engineered frames back to
`datasets/processed/`. It also fits the encoding/scaling ColumnTransformer on the
TRAIN split only and reports the resulting feature-space dimensionality, so the
exact feature list used by the models is reproducible and auditable.

Because every engineered feature depends only on the values within its own row,
the transformation is identical whether applied to train, validation or test —
there is no cross-row aggregation and therefore no leakage.

Run
---
    python src/feature_engineering.py   (run AFTER preprocessing.py)

Outputs
-------
    datasets/processed/train_fe.csv
    datasets/processed/val_fe.csv
    datasets/processed/test_fe.csv
    experimental_results/feature_list.txt
"""

import os
import pandas as pd

import pipeline_utils as pu


def main() -> None:
    os.makedirs(pu.RESULTS_DIR, exist_ok=True)

    engineered = {}
    for split in ["train", "val", "test"]:
        df = pu.load_split(split)
        fe = pu.engineer_features(df)
        out = os.path.join(pu.PROCESSED_DIR, f"{split}_fe.csv")
        fe.to_csv(out, index=False)
        engineered[split] = fe
        new_cols = ["was_contacted_before", "prev_contact_success", "age_group",
                    "campaign_intensity", "contacted_and_success"]
        print(f"{split:5s}: {fe.shape[0]:>6d} rows, {fe.shape[1]:>2d} columns "
              f"(added {len(new_cols)} engineered features) -> {out}")

    # Fit the encoder/scaler on the TRAIN fold and report the feature space.
    train_fe = engineered["train"]
    X_train, _ = pu.xy(train_fe)
    ct = pu.build_feature_pipeline(scale_numeric=True)
    ct.fit(X_train)
    feature_names = pu.get_feature_names(ct)

    fl_path = os.path.join(pu.RESULTS_DIR, "feature_list.txt")
    with open(fl_path, "w") as fh:
        fh.write(f"Total model features after encoding: {len(feature_names)}\n\n")
        fh.write(f"Numeric features ({len(pu.NUMERIC_FEATURES)}):\n")
        for c in pu.NUMERIC_FEATURES:
            fh.write(f"  - {c}\n")
        fh.write(f"\nCategorical features ({len(pu.CATEGORICAL_FEATURES)}), "
                 f"one-hot encoded:\n")
        for c in pu.CATEGORICAL_FEATURES:
            fh.write(f"  - {c}\n")
        fh.write("\nFull expanded feature vector:\n")
        for n in feature_names:
            fh.write(f"  {n}\n")

    print(f"\nFeature space after one-hot encoding: {len(feature_names)} features")
    print(f"Feature list written to {fl_path}")
    print("Feature engineering complete.")


if __name__ == "__main__":
    main()
