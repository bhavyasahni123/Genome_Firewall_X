from pathlib import Path
import json

import joblib
import numpy as np
import pandas as pd

from xgboost import XGBClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
)

LABEL_DIR = Path("outputs/labels")
MODEL_DIR = Path("models")
REPORT_DIR = Path("outputs/reports")

MODEL_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def load_dataset(dataset_name):

    path = LABEL_DIR / f"{dataset_name}.parquet"

    df = pd.read_parquet(path)

    X = (
        df
        .drop(columns=["Genome_ID", "Label"])
        .fillna(0)
        .astype(np.float32)
    )

    y = df["Label"].astype(int)

    feature_names = X.columns.tolist()

    return X, y, feature_names


def compute_scale_pos_weight(y):

    positive = (y == 1).sum()

    negative = (y == 0).sum()

    if positive == 0:
        return 1.0

    return negative / positive


def build_model(weight):

    return XGBClassifier(

        objective="binary:logistic",

        eval_metric="logloss",

        n_estimators=300,

        learning_rate=0.05,

        max_depth=6,

        subsample=0.8,

        colsample_bytree=0.8,

        random_state=42,

        tree_method="hist",

        n_jobs=-1,

        scale_pos_weight=weight,

    )


def evaluate_model(model, X_test, y_test):

    predictions = model.predict(X_test)

    probabilities = model.predict_proba(X_test)[:, 1]

    metrics = {

        "accuracy": accuracy_score(
            y_test,
            predictions,
        ),

        "precision": precision_score(
            y_test,
            predictions,
            zero_division=0,
        ),

        "recall": recall_score(
            y_test,
            predictions,
            zero_division=0,
        ),

        "f1": f1_score(
            y_test,
            predictions,
            zero_division=0,
        ),

        "roc_auc": roc_auc_score(
            y_test,
            probabilities,
        ),

    }

    confusion = confusion_matrix(
        y_test,
        predictions,
    )

    report = classification_report(
        y_test,
        predictions,
        zero_division=0,
    )

    return metrics, confusion, report


def save_model(model, dataset_name):

    model_path = MODEL_DIR / f"{dataset_name}.pkl"

    joblib.dump(
        model,
        model_path,
    )

    return model_path


def save_metadata(dataset_name, metrics, feature_count, samples):

    metadata = {

        "model_name": dataset_name,

        "version": "1.0.0",

        "algorithm": "XGBoost",

        "feature_count": feature_count,

        "training_samples": samples,

        "accuracy": float(metrics["accuracy"]),

        "precision": float(metrics["precision"]),

        "recall": float(metrics["recall"]),

        "f1": float(metrics["f1"]),

        "roc_auc": float(metrics["roc_auc"]),

        "threshold": 0.50,

    }

    with open(
        MODEL_DIR / f"{dataset_name}_metadata.json",
        "w",
    ) as f:

        json.dump(
            metadata,
            f,
            indent=4,
        )


def save_reports(dataset_name, report, confusion, importance):

    with open(
        REPORT_DIR / f"{dataset_name}_classification_report.txt",
        "w",
    ) as f:

        f.write(report)

    confusion_df = pd.DataFrame(

        confusion,

        columns=[
            "Predicted_0",
            "Predicted_1",
        ],

        index=[
            "Actual_0",
            "Actual_1",
        ],

    )

    confusion_df.to_csv(
        REPORT_DIR / f"{dataset_name}_confusion_matrix.csv"
    )

    importance.to_csv(
        REPORT_DIR / f"{dataset_name}_feature_importance.csv",
        index=False,
    )


def save_feature_names(feature_names):

    with open(
        MODEL_DIR / "feature_names.json",
        "w",
    ) as f:

        json.dump(
            feature_names,
            f,
            indent=4,
        )


def save_registry(datasets, feature_count):

    registry = {

        "version": "1.0.0",

        "models": {},

    }

    for dataset in datasets:

        registry["models"][dataset] = {

            "model_path": str(
                MODEL_DIR / f"{dataset}.pkl"
            ),

            "feature_count": feature_count,

            "threshold": 0.50,

        }

    with open(
        MODEL_DIR / "model_registry.json",
        "w",
    ) as f:

        json.dump(
            registry,
            f,
            indent=4,
        )