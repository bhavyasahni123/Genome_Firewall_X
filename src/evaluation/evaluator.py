from pathlib import Path

import joblib
import pandas as pd

from sklearn.model_selection import train_test_split

from src.evaluation.metrics import compute_metrics


LABEL_DIR = Path("outputs/labels")
MODEL_DIR = Path("outputs/models")
OUTPUT_DIR = Path("outputs/evaluation")

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

DATASETS = [
    "ampicillin",
    "cefotaxime",
    "ciprofloxacin",
    "gentamicin",
    "meropenem",
]


def evaluate_dataset(name):

    df = pd.read_parquet(
        LABEL_DIR / f"{name}.parquet"
    )

    X = (
        df.drop(
            columns=[
                "Genome_ID",
                "Label",
            ]
        )
        .fillna(0)
        .astype("float32")
    )

    y = df["Label"]

    _, X_test, _, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    model = joblib.load(
        MODEL_DIR / f"{name}.pkl"
    )

    y_pred = model.predict(
        X_test
    )

    y_prob = model.predict_proba(
        X_test
    )[:, 1]

    metrics = compute_metrics(
        y_test,
        y_pred,
        y_prob,
    )

    return metrics


def main():

    all_metrics = []

    print("=" * 80)
    print("Genome Firewall X Evaluation")
    print("=" * 80)

    for antibiotic in DATASETS:

        print(f"\nEvaluating {antibiotic}")

        metrics = evaluate_dataset(
            antibiotic
        )

        metrics["Antibiotic"] = antibiotic

        all_metrics.append(metrics)

        for key, value in metrics.items():

            if key == "Antibiotic":
                continue

            print(
                f"{key:22}: {value:.4f}"
            )

    results = pd.DataFrame(
        all_metrics
    )

    results.to_csv(
        OUTPUT_DIR / "evaluation_metrics.csv",
        index=False,
    )

    print("\n")
    print("=" * 80)
    print("Evaluation Finished")
    print("=" * 80)

    print(results)


if __name__ == "__main__":
    main()