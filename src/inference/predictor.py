import pandas as pd

from .model_loader import ModelLoader
from .feature_validator import FeatureValidator


class Predictor:

    def __init__(self):

        self.loader = ModelLoader()

        self.models = self.loader.load_models()

        self.validator = FeatureValidator(
            self.loader.get_feature_names()
        )

    def predict(self, features: pd.DataFrame):

        validated, missing, extra = self.validator.validate(
            features
        )

        results = {}

        for antibiotic, model in self.models.items():

            probability = float(
                model.predict_proba(validated)[0][1]
            )

            threshold = self.loader.get_threshold(
                antibiotic
            )

            prediction = (
                "Resistant"
                if probability >= threshold
                else "Susceptible"
            )

            results[antibiotic] = {
                "prediction": prediction,
                "probability": round(probability, 4),
                "threshold": threshold,
            }

        return {
            "predictions": results,
            "missing_features": missing,
            "extra_features": extra,
        }