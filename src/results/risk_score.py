from typing import Dict


class RiskScorer:

    def __init__(self):

        self.low_threshold = 0.25
        self.medium_threshold = 0.50
        self.high_threshold = 0.75

    def compute(self, predictions: Dict):

        probabilities = []

        resistant = 0
        susceptible = 0

        highest_antibiotic = None
        highest_probability = -1.0

        for antibiotic, result in predictions.items():

            probability = float(result["probability"])

            probabilities.append(probability)

            if result["prediction"] == "Resistant":
                resistant += 1
            else:
                susceptible += 1

            if probability > highest_probability:
                highest_probability = probability
                highest_antibiotic = antibiotic

        if len(probabilities) == 0:
            overall_score = 0.0
        else:
            overall_score = sum(probabilities) / len(probabilities)

        if overall_score < self.low_threshold:
            level = "Low"

        elif overall_score < self.medium_threshold:
            level = "Moderate"

        elif overall_score < self.high_threshold:
            level = "High"

        else:
            level = "Critical"

        return {

            "overall_risk_score": round(overall_score, 4),

            "overall_risk_percent": round(
                overall_score * 100,
                2,
            ),

            "overall_risk_level": level,

            "resistant_predictions": resistant,

            "susceptible_predictions": susceptible,

            "highest_probability_antibiotic": highest_antibiotic,

            "highest_probability": round(
                highest_probability,
                4,
            ),
        }