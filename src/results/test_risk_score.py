from .risk_score import RiskScorer

predictions = {

    "ampicillin": {
        "prediction": "Resistant",
        "probability": 0.94,
    },

    "cefotaxime": {
        "prediction": "Susceptible",
        "probability": 0.21,
    },

    "ciprofloxacin": {
        "prediction": "Resistant",
        "probability": 0.88,
    },

    "gentamicin": {
        "prediction": "Susceptible",
        "probability": 0.11,
    },

    "meropenem": {
        "prediction": "Susceptible",
        "probability": 0.03,
    },

}

scorer = RiskScorer()

result = scorer.compute(predictions)

print()

for key, value in result.items():
    print(f"{key:35} {value}")