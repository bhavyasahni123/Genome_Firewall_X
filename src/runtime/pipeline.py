from pathlib import Path

from src.runtime.amrfinder import RuntimeAMRFinder
from src.feature_engine import FeatureEngine
from src.api.services.prediction_service import PredictionService
from src.api.services.explain_service import ExplainService

class RuntimePipeline:
    """
    Runtime inference pipeline.

    Upload .fna
        ↓
    AMRFinderPlus
        ↓
    Feature Engineering
        ↓
    Prediction
    """

    def __init__(self):

        self.amrfinder = RuntimeAMRFinder()
        self.feature_engine = FeatureEngine()
        self.prediction_service = PredictionService()
        self.explain_service = ExplainService()

        self.amrfinder_output_dir = Path("outputs/amrfinder")
        self.feature_output_dir = Path("outputs/features")

        self.amrfinder_output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.feature_output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def run(self, genome_file: str | Path):

        genome_file = Path(genome_file)

        if not genome_file.exists():
            raise FileNotFoundError(genome_file)

       
        amr_parquet = self.amrfinder.run(
            genome_file=genome_file,
            output_directory=self.amrfinder_output_dir,
        )

        
        feature_file = self.feature_engine.build(
            amr_parquet,
        )

        
        predictions = self.prediction_service.predict_file(
            feature_file,
        )

        prediction_result = predictions[0]

        genome_id = prediction_result["summary"]["genome_id"]

        explanations = {}

        for antibiotic in prediction_result["predictions"]:

            explanations[antibiotic] = self.explain_service.explain(
                feature_file=feature_file,
                genome_id=genome_id,
                antibiotic=antibiotic,
            )

        return {
            "status": "completed",
            "genome_id": genome_id,
            "predictions": prediction_result,
            "explanations": explanations,
        }


if __name__ == "__main__":

    pipeline = RuntimePipeline()

    result = pipeline.run(
        "uploads/example.fna",
    )

    print(result)