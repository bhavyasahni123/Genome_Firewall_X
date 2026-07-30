from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class FeatureExplanation:
    feature: str
    shap_value: float
    direction: str


@dataclass
class AntibioticPrediction:
    antibiotic: str
    prediction: str
    probability: float
    threshold: float
    top_features: List[FeatureExplanation] = field(default_factory=list)


@dataclass
class GenomeSummary:
    genome_id: str
    total_amr_hits: int
    unique_amr_genes: int
    unique_classes: int
    resistant_predictions: int
    susceptible_predictions: int
    overall_risk_score: float
    overall_risk_level: str


@dataclass
class PredictionResult:
    genome_summary: GenomeSummary
    predictions: Dict[str, AntibioticPrediction]
    model_version: str = "1.0.0"
    