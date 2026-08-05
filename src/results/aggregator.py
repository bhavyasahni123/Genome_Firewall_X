from typing import Dict

from .risk_score import RiskScorer


class ResultAggregator:

    def __init__(self):

        self.risk = RiskScorer()

    def aggregate(
        self,
        genome_id: str,
        predictions: Dict,
        feature_summary: Dict = None,
    ):

        risk = self.risk.compute(predictions)

        if feature_summary is None:
            feature_summary = {}

        summary = {

            "genome_id": genome_id,

            "total_amr_hits":
                feature_summary.get(
                    "Total_AMR_Hits",
                    None,
                ),

            "unique_amr_genes":
                feature_summary.get(
                    "Unique_AMR_Genes",
                    None,
                ),

            "unique_classes":
                feature_summary.get(
                    "Unique_Classes",
                    None,
                ),

            "unique_subclasses":
                feature_summary.get(
                    "Unique_Subclasses",
                    None,
                ),

            "unique_types":
                feature_summary.get(
                    "Unique_Types",
                    None,
                ),

            "unique_methods":
                feature_summary.get(
                    "Unique_Methods",
                    None,
                ),

            "overall_risk": risk,

        }

        return {

            "summary": summary,

            "predictions": predictions,

        }
    