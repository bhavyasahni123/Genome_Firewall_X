import pandas as pd

from .predictor import Predictor

predictor = Predictor()

sample = pd.DataFrame(
    {
        "Total_AMR_Hits": [12],
        "Unique_AMR_Genes": [8],
        "Unique_Classes": [6],
        "Unique_Subclasses": [7],
        "Unique_Types": [2],
        "Unique_Subtypes": [2],
        "Unique_Methods": [3],
        "Unique_Contigs": [4],
    }
)

result = predictor.predict(sample)

print()

print("Prediction Results")

print("=" * 60)

for antibiotic, info in result["predictions"].items():

    print(
        f"{antibiotic:15}"
        f"{info['prediction']:12}"
        f"{info['probability']:.4f}"
    )

print()

print(
    "Missing Features :",
    len(result["missing_features"]),
)

print(
    "Extra Features :",
    len(result["extra_features"]),
)
