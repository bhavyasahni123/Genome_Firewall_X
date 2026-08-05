from pathlib import Path
import json


class ModelService:

    def __init__(self):

        self.model_dir = Path("models")

    def get_models(self):

        registry_file = self.model_dir / "model_registry.json"

        if not registry_file.exists():
            raise FileNotFoundError(registry_file)

        with open(registry_file) as f:
            registry = json.load(f)

        models = {}

        for metadata_file in self.model_dir.glob("*_metadata.json"):

            with open(metadata_file) as f:
                metadata = json.load(f)

            models[metadata["model_name"]] = metadata

        return {
            "registry": registry,
            "models": models,
        }

    def get_model(self, antibiotic):

        file = self.model_dir / f"{antibiotic}_metadata.json"

        if not file.exists():
            return None

        with open(file) as f:
            return json.load(f)
        