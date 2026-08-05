from pathlib import Path
import pandas as pd


class MetricsService:

    def __init__(self):

        self.metrics_file = Path(
            "outputs/evaluation/evaluation_metrics.csv"
        )

    def get_metrics(self):

        if not self.metrics_file.exists():
            raise FileNotFoundError(
                self.metrics_file
            )

        df = pd.read_csv(self.metrics_file)

        return df.to_dict(orient="records")

    def get_metric(self, antibiotic):

        metrics = self.get_metrics()

        for item in metrics:

            if item["Antibiotic"] == antibiotic:
                return item

        return None