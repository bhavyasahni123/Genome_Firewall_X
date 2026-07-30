import pandas as pd

from .explainer import GenomeExplainer

explainer = GenomeExplainer()

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

result = explainer.explain(
    "ampicillin",
    sample,
)

print()

print("Prediction")

print(result["prediction"])

print()

print("Probability")

print(result["probability"])

print()

print("Top Features")

for feature in result["top_features"]:

    print(
        f"{feature['Feature']:35}"
        f"{feature['SHAP']:.5f}"
    )