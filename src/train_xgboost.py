from pathlib import Path
import warnings

import pandas as pd

from sklearn.model_selection import train_test_split

from utils import (
    load_dataset,
    compute_scale_pos_weight,
    build_model,
    evaluate_model,
    save_model,
    save_metadata,
    save_reports,
    save_feature_names,
    save_registry,
)

warnings.filterwarnings("ignore")

REPORT_DIR = Path("outputs/reports")

DATASETS = [
    "ampicillin",
    "cefotaxime",
    "ciprofloxacin",
    "gentamicin",
    "meropenem",
]

metrics_summary = []
feature_names = None

print("=" * 80)
print("Genome Firewall X - XGBoost Training")
print("=" * 80)

for dataset_name in DATASETS:

    print(f"\nTraining {dataset_name}")

    X, y, feature_names = load_dataset(dataset_name)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    weight = compute_scale_pos_weight(y_train)

    print(f"Samples           : {len(X)}")
    print(f"Features          : {X.shape[1]}")
    print(f"Scale Pos Weight  : {weight:.2f}")

    model = build_model(weight)

    model.fit(
        X_train,
        y_train,
    )

    metrics, confusion, report = evaluate_model(
        model,
        X_test,
        y_test,
    )

    print(f"Accuracy  : {metrics['accuracy']:.4f}")
    print(f"Precision : {metrics['precision']:.4f}")
    print(f"Recall    : {metrics['recall']:.4f}")
    print(f"F1 Score  : {metrics['f1']:.4f}")
    print(f"ROC AUC   : {metrics['roc_auc']:.4f}")

    save_model(
        model,
        dataset_name,
    )

    save_metadata(
        dataset_name,
        metrics,
        X.shape[1],
        len(X),
    )

    importance = (
        pd.DataFrame(
            {
                "Feature": X.columns,
                "Importance": model.feature_importances_,
            }
        )
        .sort_values(
            by="Importance",
            ascending=False,
        )
    )

    save_reports(
        dataset_name,
        report,
        confusion,
        importance,
    )

    metrics_summary.append(
        {
            "Antibiotic": dataset_name,
            "Samples": len(X),
            "Features": X.shape[1],
            "Accuracy": metrics["accuracy"],
            "Precision": metrics["precision"],
            "Recall": metrics["recall"],
            "F1": metrics["f1"],
            "ROC_AUC": metrics["roc_auc"],
        }
    )

metrics_df = pd.DataFrame(metrics_summary)

metrics_df.to_csv(
    REPORT_DIR / "metrics.csv",
    index=False,
)

save_feature_names(feature_names)

save_registry(
    DATASETS,
    len(feature_names),
)

print("\n")
print("=" * 80)
print("Training Complete")
print("=" * 80)

print(metrics_df)

print("\nFeature names saved.")
print("Model registry saved.")
print("Models saved.")
print("Reports generated.")