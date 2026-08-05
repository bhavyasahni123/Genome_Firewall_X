from pathlib import Path
import json
import joblib


class ModelLoader:

    def __init__(self):

        self.model_dir = Path("models")

        with open(self.model_dir / "model_registry.json") as f:
            self.registry = json.load(f)

        with open(self.model_dir / "feature_names.json") as f:
            self.feature_names = json.load(f)

        self.models = {}

    def load_models(self):

        if self.models:
            return self.models

        for antibiotic, info in self.registry["models"].items():

            model_path = Path(info["model_path"])

            self.models[antibiotic] = joblib.load(model_path)

        return self.models

    def get_feature_names(self):

        return self.feature_names

    def get_threshold(self, antibiotic):

        return self.registry["models"][antibiotic]["threshold"]

    def get_antibiotics(self):

        return list(self.registry["models"].keys())