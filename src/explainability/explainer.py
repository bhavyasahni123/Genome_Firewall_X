from pathlib import Path

import numpy as np
import pandas as pd
import shap

from src.inference.model_loader import ModelLoader
from src.inference.feature_validator import FeatureValidator
from src.explainability.feature_descriptions import FEATURE_DESCRIPTIONS


class GenomeExplainer:

    def __init__(self):

        self.loader = ModelLoader()

        self.models = self.loader.load_models()

        self.validator = FeatureValidator(
            self.loader.get_feature_names()
        )

    def build_interpretation(
        self,
        prediction,
        probability,
        top_features,
    ):

        confidence = (
            "very high"
            if probability >= 0.95
            else "high"
            if probability >= 0.80
            else "moderate"
            if probability >= 0.60
            else "low"
        )

        descriptions = [
            feature.get("Description", feature["Feature"])
            for feature in top_features[:3]
        ]

        readable = ", ".join(descriptions)

        return (
            f"The model predicts {prediction.lower()} "
            f"with {confidence} confidence "
            f"({probability * 100:.1f}%). "
            f"The strongest contributing biological factors are "
            f"{readable}."
        )

    def explain(
        self,
        antibiotic,
        features,
        top_k=10,
    ):

        if antibiotic not in self.models:
            raise ValueError(
                f"Unknown antibiotic: {antibiotic}"
            )

        validated, _, _ = self.validator.validate(
            features
        )

        model = self.models[antibiotic]

        explainer = shap.TreeExplainer(model)

        shap_values = explainer.shap_values(validated)

        if isinstance(shap_values, list):
            shap_values = shap_values[1]

        values = shap_values[0]

        feature_names = validated.columns

        importance = pd.DataFrame(
            {
                "Feature": feature_names,
                "SHAP": values,
                "ABS_SHAP": np.abs(values),
            }
        )

        importance = (
            importance
            .sort_values(
                by="ABS_SHAP",
                ascending=False,
            )
            .head(top_k)
        )

        importance["Description"] = (
            importance["Feature"]
            .map(FEATURE_DESCRIPTIONS)
            .fillna("Feature used by the prediction model.")
        )

        probability = float(
            model.predict_proba(validated)[0][1]
        )

        prediction = (
            "Resistant"
            if probability >= 0.5
            else "Susceptible"
        )

        top_features = importance.to_dict(
            orient="records"
        )

        return {
            "antibiotic": antibiotic,
            "prediction": prediction,
            "probability": probability,
            "clinical_interpretation": self.build_interpretation(
                prediction,
                probability,
                top_features,
            ),
            "top_features": top_features,
        }