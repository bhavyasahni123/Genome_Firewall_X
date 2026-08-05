from pathlib import Path
import pandas as pd

from .predictor import Predictor


class GenomePipeline:

    def __init__(self):

        self.predictor = Predictor()

    def predict_file(self, feature_file):

        feature_file = Path(feature_file)

        df = pd.read_parquet(feature_file)

        if "Genome_ID" not in df.columns:
            raise ValueError("Genome_ID column not found.")

        results = []

        for _, row in df.iterrows():

            genome_id = row["Genome_ID"]

            features = row.drop(labels=["Genome_ID"])

            features = pd.DataFrame([features])

            prediction = self.predictor.predict(features)

            results.append(
                {
                    "Genome_ID": genome_id,
                    **prediction,
                }
            )

        return results


if __name__ == "__main__":

    pipeline = GenomePipeline()

    feature_file = "outputs/features/genome_1_features.parquet"

    results = pipeline.predict_file(feature_file)

    print("=" * 80)
    print("Genome Firewall X - Predictions")
    print("=" * 80)

    for genome in results[:5]:

        print(f"\nGenome : {genome['Genome_ID']}")

        for antibiotic, info in genome["predictions"].items():

            print(
                f"{antibiotic:15}"
                f"{info['prediction']:12}"
                f"{info['probability']:.4f}"
            )