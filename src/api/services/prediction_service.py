from pathlib import Path
import pandas as pd

from src.inference.predictor import Predictor
from src.results.aggregator import ResultAggregator


class PredictionService:

    def __init__(self):

        self.predictor = Predictor()
        self.aggregator = ResultAggregator()

    def predict_file(self, feature_file):

        feature_file = Path(feature_file)

        if not feature_file.exists():
            raise FileNotFoundError(feature_file)

        df = pd.read_parquet(feature_file)

        if "Genome_ID" not in df.columns:
            raise ValueError("Genome_ID column not found.")

        results = []

        for _, row in df.iterrows():

            genome_id = str(row["Genome_ID"])

            feature_summary = {
                "Total_AMR_Hits": row.get("Total_AMR_Hits"),
                "Unique_AMR_Genes": row.get("Unique_AMR_Genes"),
                "Unique_Classes": row.get("Unique_Classes"),
                "Unique_Subclasses": row.get("Unique_Subclasses"),
                "Unique_Types": row.get("Unique_Types"),
                "Unique_Methods": row.get("Unique_Methods"),
            }

            features = pd.DataFrame(
                [row.drop(labels=["Genome_ID"])]
            )

            prediction = self.predictor.predict(features)

            results.append(
                self.aggregator.aggregate(
                    genome_id=genome_id,
                    predictions=prediction["predictions"],
                    feature_summary=feature_summary,
                )
            )

        return results