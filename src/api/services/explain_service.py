import pandas as pd

from src.inference.predictor import Predictor
from src.explainability.explainer import GenomeExplainer


class ExplainService:

    def __init__(self):

        self.predictor = Predictor()
        self.explainer = GenomeExplainer()

    def explain(
        self,
        feature_file,
        genome_id,
        antibiotic,
    ):

        df = pd.read_parquet(feature_file)

        genome = df[
            df["Genome_ID"].astype(str) == str(genome_id)
        ]

        if genome.empty:
            raise ValueError(
                f"Genome {genome_id} not found."
            )

        features = genome.drop(
            columns=["Genome_ID"]
        )

        prediction = self.predictor.predict(
            features
        )

        explanation = self.explainer.explain(
            antibiotic=antibiotic,
            features=features,
        )

        return {
            "genome_id": genome_id,
            "prediction": prediction["predictions"][antibiotic],
            "explanation": explanation,
        }